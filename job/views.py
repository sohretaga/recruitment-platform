from django.shortcuts import render

# Create your views here.

def vacancies(request):
    return render(request, 'vacancies.html')

def vacancy(request):
    return render(request, 'vacancy.html')

def categories(request):
    return render(request, 'categories.html')