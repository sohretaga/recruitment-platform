from django.shortcuts import render

# Create your views here.

def blog(request):
    return render(request, 'blog/blog.html')

def detail(request):
    return render(request, 'blog/detail.html')

def grid(request):
    return render(request, 'blog/grid.html')