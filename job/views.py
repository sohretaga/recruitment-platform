from django.shortcuts import render

# Create your views here.

def vacancies(request):
    return render(request, 'job/vacancies.html')

def vacancy(request):
    return render(request, 'job/vacancy.html')

def categories(request):
    return render(request, 'job/categories.html')