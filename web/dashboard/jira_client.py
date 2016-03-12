import requests, urllib, logging, sys
from oauthlib.oauth1 import SIGNATURE_RSA
from requests_oauthlib import OAuth1Session
from jira.client import JIRA
from django.conf import settings

logger = logging.getLogger(__name__)
log = logging.getLogger('oauth1_session')
log.addHandler(sys.stdout)
log.setLevel(logging.DEBUG)

def get_pkey():
    with open(settings.PRIVATE_KEY_LOCATION, 'r') as f:
        return f.read()

def get_oauth_session():
    data = get_pkey()
    oauth = OAuth1Session(settings.JIRA_SETTINGS['consumer_key'], 
        signature_type='auth_header', signature_method=SIGNATURE_RSA, rsa_key=data)
    return oauth

def jira_start_oauth(callback_url):
    oauth = get_oauth_session()
    request_token = oauth.fetch_request_token(settings.JIRA_SETTINGS['request_token_url'], verify=False)
    oauth_token = request_token['oauth_token']
    oauth_secret = request_token['oauth_token_secret']
    params = {
        'oauth_token' : oauth_token,
        'oauth_callback' : callback_url
    }
    return (oauth_secret, oauth_token, settings.JIRA_SETTINGS['authorize_url'] + \
        '?' + urllib.parse.urlencode(params))

def jira_continue_auth(oauth_token, oauth_token_secret):
    oauth = get_oauth_session()
    ## LOLOLOL JIRA USES OAUTH 1.0 NOT EVEN 1.0a SO WE  HAVE TO DO SHIT LIKE THIS
    ## In all the examples, the script makes the original Oauth object used for the req token
    ## persist to the access token request, but this isn't possible on a webserver without
    ## caching memory accross requests, so we have ot manually set the internal info.
    ## Who the fuck gives such a useless example like that?
    oauth._client.client.verifier = u'verified'
    oauth._client.client.resource_owner_key = oauth_token
    oauth._client.client.resource_owner_secret = (oauth_token_secret)
    ## do NOT ask me how long it took to figure this out, fuck you atlassian
    access_token = oauth.fetch_access_token(settings.JIRA_SETTINGS['access_token_url'], allow_redirects=False, verify=False)
    real_oauth_token = access_token['oauth_token']
    real_oauth_token_secret = access_token['oauth_token_secret']
    return (real_oauth_token_secret, real_oauth_token)

def jira_get_client(oauth_token, oauth_token_secret):
    jira = JIRA(options=
        {
            'server': settings.JIRA_SETTINGS['jira_base_url'],
            'verify': False

        }, oauth=
        {
            'access_token': oauth_token,
            'access_token_secret': oauth_token_secret,
            'consumer_key': settings.JIRA_SETTINGS['consumer_key'],
            'key_cert': get_pkey(),
        }
    )
    return jira

def jira_populate_information(student):
    client = jira_get_client(student.jira_token, student.jira_token_secret)
    logger.info(client.current_user())
    student.jira_username = client.current_user()

def jira_get_assigned_issues(student):
    client = jira_get_client(student.jira_token, student.jira_token_secret)
    return client.search_issues('assignee=%s' % student.jira_username)

def jira_get_project_issues(project_hook):
    client = jira_get_client(student.jira_token, student.jira_token_secret)
    return client.search_issues('project=%s' % project_hook)