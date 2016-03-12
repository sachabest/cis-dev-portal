from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.urlresolvers import reverse
from .models import OAuthState
from pprint import pprint
from uuid import uuid4
import urllib, logging
from .github_client import *
from .jira_client import *

logger = logging.getLogger(__name__)

auth_wall = loader.get_template("auth_wall.html")

# @login_required
def index(request):
    app_list = None
    template = loader.get_template('index.html')
    if not request.user.is_authenticated():
        context = {}
        return HttpResponse(auth_wall.render(context, request))
    else:
        context = {
            'links': app_list,
            'user' : request.user, 
        }
        if request.user.student.github_username:
            context['groups'] = get_org_repos(request.user.student.github_token, 'cis-upenn')
        else:
            context['groups'] = []
        if request.user.student.jira_username:
            context['issues'] = jira_get_assigned_issues(request.user.student)
            logger.info(context['issues'])
        else:
            context['issues'] = []
        return HttpResponse(template.render(context, request))

def is_valid_state(state, user, jira=False):
    possible_states = OAuthState.objects.filter(user=user, active_flag=True)
    for possible_state in possible_states:
        if possible_state.key == state:
            possible_state.active_flag = False
            possible_state.save()
            return True

def set_valid_state(state, user, jira=False):
    old_states = OAuthState.objects.filter(user=user)
    for obj in old_states:
        obj.active_flag = False
        obj.save()
    new_state = OAuthState(key=state, user=user, active_flag=True)
    new_state.save()

@login_required
def link_jira(request):
    callback_url = request.build_absolute_uri(reverse('dashboard:jira_handshake'))
    (oauth_secret, oauth_token, redirect_url) = jira_start_oauth(callback_url)
    request.user.student.jira_token = oauth_token
    request.user.student.jira_token_secret = oauth_secret
    request.user.student.save()
    return HttpResponseRedirect(redirect_url)

@login_required
def jira_handshake(request):
    (oauth_secret, oauth_token) = jira_continue_auth(request.user.student.jira_token, \
        request.user.student.jira_token_secret)
    request.user.student.jira_token = oauth_token
    request.user.student.jira_token_secret = oauth_secret
    jira_populate_information(request.user.student)
    request.user.student.save()
    logger.info("Auhtorising %s for jira with %s, %s" % (request.user.username, \
        request.user.student.jira_token, request.user.student.jira_token_secret))
    return HttpResponseRedirect(reverse('dashboard:index'))

@login_required
def link_github(request):
    state = str(uuid4())
    set_valid_state(state, request.user)
    logger.info("registered state %s for %s" % (state, request.user.username))
    callback_url = request.build_absolute_uri(reverse('dashboard:github_handshake'))
    params = {"client_id": settings.GITHUB_CLIENT_ID,
              "state": state,
              "redirect_uri": callback_url,
              "scope": "repo,user,admin:org"}
    url = "https://github.com/login/oauth/authorize?" + urllib.parse.urlencode(params)
    return HttpResponseRedirect(url)

@login_required
def github_handshake(request):
    error = request.GET.get('error', None)
    if error:
        logger.error("Bad github response.")
        return HttpResponse(status=500)
    state = request.GET['state']
    if not is_valid_state(state, request.user):
        logger.error("Bad github response.")
        return HttpResponse(status=403)
    else:
        params = {
            "client_id": settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
            "code": request.GET['code'],
            "state": state,
        }
        request.user.student.github_token = send_authentication_challenge(params)
        github_populate_information(request.user.student)
        request.user.student.save()
        logger.info("Auhtorising %s with %s" % (request.user.username, request.user.student.github_token))
        return HttpResponseRedirect(reverse('dashboard:index'))

@login_required
def github_get_contributors(request):
    org_name = request.GET['org_name']
    repo_name = request.GET['repo_name']
    return get_repo_contributors(request.user.student.github_token, \
        org_name, repo_name)

@login_required
def get_project_issues(request):
    project_hook = request.GET['project']
    return jira_get_project_issues(project_hook)