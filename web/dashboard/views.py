from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.app_settings import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET
from .models import SiteApp
from pprint import pprint
from uuid import uuid4
import urllib
import logging
logger = logging.getLogger(__name__)

auth_wall = loader.get_template("auth_wall.html")

# @login_required
def index(request):
    app_list = SiteApp.objects
    template = loader.get_template('index.html')
    context = {
        'links': app_list,
        'user' : request.user
    }
    if not request.user.is_authenticated():
        return HttpResponse(auth_wall.render(context, request))
    else:
        return HttpResponse(template.render(context, request))


valid_github_states = {}

def is_valid_state(state, username):
    return valid_github_states[username] == state

@login_required
def link_github(request):
    state = str(uuid4())
    valid_github_states[request.user.username] = state
    save_created_state(state)
    callback_url = request.build_aboslute_url(reverse('dashboard.views.github_handshake'))
    params = {"client_id": GITHUB_CLIENT_ID,
              "state": state,
              "redirect_uri": callback_url,
              "scope": "repo,user,admin:org"}
    url = "https://github.com/login/oauth/authorize?" + urllib.urlencode(params)
    return HttpResponseRedirect(url)

@login_required
def github_handshake(request):
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state, request.user.username) \
        or request.args.get['client_id'] != GITHUB_CLIENT_ID \
        or reqeust.args.get['client_secret'] != GITHUB_CLIENT_SECRET:
        abort(403)
    else:
        valid_github_states[request.user.username] = None
        request.user.github_token = request.body.split('=')[1]
        return HttpResponseRedirect(reverse('dashboard.views.index'))