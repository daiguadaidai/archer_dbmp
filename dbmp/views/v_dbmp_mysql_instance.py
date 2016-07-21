from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def list(request):
    user = {'name': 'HH',
            'age': 25,
            'gender': 'gen',
            'brother': {
               'name': 'HH',
               'age': '34',
            },
            'books': ['Python', 'Java']
    }

    return render(request, 'dbmp_mysql_instance/list.html', {'title': 'title', 'user': user})

def view(request):

def edit(request):
    pass

def delete(request):
    pass

def test(request):
    return render(request, 'test.html')
