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
import urllib
import logging
logger = logging.getLogger(__name__)

auth_wall = loader.get_template("auth_wall.html")

# @login_required
def index(request):
    app_list = None
    template = loader.get_template('index.html')
    context = {
        'links': app_list,
        'user' : request.user
    }
    if not request.user.is_authenticated():
        return HttpResponse(auth_wall.render(context, request))
    else:
        return HttpResponse(template.render(context, request))


def is_valid_state(state, user):
    possible_states = OAuthState.objects.filter(user=user, active_flag=True)
    for possible_state in possible_states:
        if possible_state.key == state:
            possible_state.active_flag = False
            possible_state.save()
            return True

def set_valid_state(state, user):
    old_states = OAuthState.objects.filter(user=user)
    for obj in old_states:
        obj.active_flag = False
        obj.save()
    new_state = OAuthState(key=state, user=user, active_flag=True)
    new_state.save()

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
        request.user.student.github_token = request.GET['code']
        request.user.student.save()
        logger.info("Auhtorising %s with %s" % (request.user.username, request.user.student.github_token))
        return HttpResponseRedirect(reverse('dashboard:index'))