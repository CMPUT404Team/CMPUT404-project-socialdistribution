from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def index(index):
    return HttpResponse("Hello, world. You're at the polls index.")
