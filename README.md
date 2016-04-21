# UPenn CIS Development Portal
CIS 599 - Independent Study

## Technology Used

* Docker: environment replication and deployment
* Nginx: web server
* Django: application server
* Shibboleth: Penn SSO
* Redis: in memory DB
* Postgres: SQL backend for Django

## TODO

See [Issues](https://github.com/sachabest/cis599/issues)

## Deployment and Building Instructions

Assuming you have Docker installed on your machine as well as a DigitalOcean account, deployment is a breeze. Run the following command to create a droplet configured by Docker:

```bash
docker-machine create \
-d digitalocean \
--digitalocean-access-token=ADD_YOUR_TOKEN_HERE \
production
```

Now, to build and deploy directly to production, do the following from the root of the repository:

```bash
docker-machine env production
eval $(docker-machine env production)
./full-rebuild.sh
./makenmigrate.sh
```

You now have a fully built, deployed instance of the site complete with configured PostgreSQL. 

Now that you're up and running, I've included a useful tool to help rapid building. You can manually run ``` ./soft-rebuild.sh ``` or do the following

``` ./watcher.py soft-rebuild.sh . ```

to auto rebuild the site on any saved file inside the root directory. This is the equivalent of ``` rake watch ``` in Ruby. 

## Repository Organization

* ```nginx/```: holds configuration files for nginx
  * ```attribute-map.xml```: the shibboleth attributes to map (basically default)
  * ```default.conf```: nginx site configuration (directives for SSL, shib, etc.)
  * ```Dockerfile```: the file run by docker-compose to build nginx and copy necessary config files
  * ```nginx.conf```: nginx global configuration
  * ```private.key``` (NOT INCLUDED): SSL pkey
  * ```sachabest.com.crt``` (NOT INCLUDED): SSL cert
  * ```shibboleth2.xml```: The shibboleth SP config file (see Shibboleth setup)
  * ```upenn-metadata.xml```: UPenn specific Shibboleth metadata
* ```web/```: holds web server files and django configuration
  * ```cis_dev_portal/```: the main project folder for django
  * ```dashbaord/```: the first application under the main project
* ```docker-compose.yml```: the docker-compose specification file
* ```production.yml```: a docker-compose file for production deployment (currently same as docker-compose.yml)
* ```prod.sh```: runs and deploys to the production machine in docker-machine
* ```dev.sh```: runs locally on the default machine in docker-machine
* ```makenmigrate.sh```: make and deploys database migrations for Django
* ```.env```: holds environment variables for shibboleth configuration


## Shibboleth Setup

Shibboleth is a monster with very little relevant documentation as it pertains to UPenn specifically. I will now attempt to go through the process I followed to get it working.

Shibboleth operates on three levels: 

First, the IdP (Identity Provider) is ocnfigured specifically to respond to  a set number of SPs (Service Providers) like this site. You will need to contact Penn ISC for their metadata information to configure your SP to use Penn's IdP. 

Second, the local SP is configured on the web server level to add metadata and information to header files in requests. You will see things like

```
    # FastCGI responder
    location ${SHIBBOLETH_RESPONDER_PATH:-/saml} {
        include fastcgi_params;
        fastcgi_param  HTTPS on;
        fastcgi_param  SERVER_PORT 443;
        fastcgi_param  SERVER_PROTOCOL https;
        fastcgi_param  X_FORWARDED_PROTO https;
        fastcgi_param  X_FORWARDED_PORT 443;
        fastcgi_pass unix:/tmp/shibresponder.sock;
    }
```

that instruct nginx to create a shibboleth responder socket at the given location provided in an environment variable (or /saml by default). Further, you will see 

```
        proxy_set_header        Accept-Encoding   "";
        proxy_set_header        Host            $host;
        proxy_set_header        X-Real-IP       $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
```

passed as headers in all requests. This is VITAL to your server responding appropriately to shibboleth authentications. 

Also on the web server level is the actual shibboleth configuration (independent of nginx or apache). The file instructing the local shibboleth responder is nginx/shibboleth2.xml. 

The included shibboleth2.xml file is standard with the exception of two XML blocks:

```
        <MetadataProvider type="XML" path="upenn-metadata.xml"/>
```

and 

```
        <ApplicationOverride id="client" entityID="${CLIENT_APP_SCHEME:-https}://${CLIENT_APP_HOSTNAME:-your-app.localdomain.com}${SHIBBOLETH_RESPONDER_PATH:-/saml}/metadata">
            <Sessions lifetime="28800" timeout="3600" relayState="ss:mem"
                      handlerURL="${SHIBBOLETH_RESPONDER_PATH:-/saml}"
                      handlerSSL="true"
                      checkAddress="false"
                      cookieProps="https">

                <!-- DEFAULT to OpenIdP -->
                <SSO entityID="https://idp.net.isc.upenn.edu/idp/shibboleth">
                    SAML2 SAML1
                </SSO>

                <!-- Extension service that generates "approximate" metadata based on SP configuration. -->
                <Handler type="MetadataGenerator" Location="/metadata" signing="false"/>
```

The first block instructs the local chib responder to pull the UPenn specific IdP configuration from a file "upenn-metadata.xml". The second block overrides the default configuratoin (which is essentially useless) with proper config specifc to UPenn. You'll notice a few things: 

* ```CLIENT_APP_SCHEME```: https or http (usually the former)
* ```CLIENT_APP_HOSTNAME```: your webhost
* ```handlerSSL=true```: iff you use https above
* ```cookieProps="https"```: iff you use https above, else http
* ```<SSO entityID...>```: instrucst the local SP to use the given URL of the IdP specified in the upenn-metadata file. Note that this binding is done via the entityID - i.e. they must match. 


Additionally, there is the app server level. Django needs a REMOTE_USER module to bind the passed HTTP header information to local accounts in an app. See web/requirements.txt for more info on what packages are used. 

