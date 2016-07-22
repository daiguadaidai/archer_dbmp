#-*- coding: utf-8 -*-

from django.shortcuts import render
from dbmp.models.cmdb_os import CmdbOs

# Create your views here.

def home(request):
    return render(request, 'home.html')

def index(request):
    user = {'name': 'HH',
            'age': 25,
            'gender': 'gen',
            'brother': {
               'name': 'HH',
               'age': '34',
            },
            'books': ['Python', 'Java']
    }
    
    cmdbos = CmdbOs.objects.all()

    return render(request, 'dbmp_mysql_instance/index.html', {'title': 'title', 'user': user, 'cmdbos': cmdbos})

def add(request):
    pass

def view(request):
    pass

def edit(request):
    pass

def delete(request):
    pass

def test(request):
    return render(request, 'test.html')
