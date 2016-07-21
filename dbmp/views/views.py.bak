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

    return render(request, 'list.html', {'title': 'title', 'user': user})

def test(request):
    return render(request, 'test.html')
