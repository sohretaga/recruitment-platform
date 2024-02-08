from django.shortcuts import render

def contact(request):
    if request.POST:
        ...

    return render(request, 'main/contact.html')