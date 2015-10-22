from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core import serializers
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory, model_to_dict
from django.contrib.auth import authenticate, login, logout
from django.core import serializers

from .models import User
from .forms import UserCreationForm

# Create your views here.

@login_required
def main(request):
	return render(request, 'web/main.html')

def about(request):
	return render(request, 'web/team.html')

def user_login(request):
	if not request.user.is_authenticated():
		if request.method == 'POST':
			form = AuthenticationForm(None, request.POST)
			nextpage = request.GET.get('next')
			if form.is_valid():
				login(request, form.get_user())
				return HttpResponseRedirect(nextpage)
		else:
			form = AuthenticationForm(None)
		return render(request, 'web/login.html', {'form': form, 'next': request.GET.get('next')})
	else:
		return HttpResponseRedirect('/')

def user_logout(request):
	logout(request)
	# Redirect to logout successful
	message = "Logout successful"
	return render(request, 'web/login.html', {'message': message})

def new_user(request):
	if not request.user.is_authenticated():
		if request.method == 'POST':
			form = UserCreationForm(request.POST)
			if form.is_valid():
				form.save()
				user = authenticate(username=request.POST['email'], password=request.POST['password1'])
				login(request, user)
				return HttpResponseRedirect('')
		else:
			form = UserCreationForm()
		return render(request, 'web/new_user.html', {'form': form})
	else:
		return HttpResponseRedirect('/')
