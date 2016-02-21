# cis599
CIS 599 - Independent Study

## Technology Used

* Docker: environment replication and deployment
* Nginx: web server
* Django: application server
* Shibboleth: Penn SSO
* Redis: in memory DB
* Postgres: SQL backend for Django

## Repository Organization

* nginx/: holds configuration files for nginx
  * attribute-map.xml: the shibboleth attributes to map (basically default)
  * default.conf: nginx site configuration (directives for SSL, shib, etc.)
  * Dockerfile: the file run by docker-compose to build nginx and copy necessary config files
  * nginx.conf: nginx global configuration
  * private.key (NOT INCLUDED): SSL pkey
  * sachabest.com.crt (NOT INCLUDED): SSL cert
  * shibboleth2.xml: The shibboleth SP config file (see Shibboleth setup)
  * upenn-metadata.xml: UPenn specific Shibboleth metadata
* web/: holds web server files and django configuration
  * cis_dev_portal/: the main project folder for django
  * dashbaord/: the first application under the main project
* docker-compose.yml: the docker-compose specification file
* production.yml: a docker-compose file for production deployment (currently same as docker-compose.yml)
* prod.sh: runs and deploys to the production machine in docker-machine
* dev.sh: runs locally on the default machine in docker-machine
* makenmigrate.sh: make and deploys database migrations for Django


## Shibboleth Setup

Shibboleth is a monster with very little relevant documentation as it pertains to UPenn specifically. I will now attempt to go through the process I followed to get it working.


