from django.shortcuts import render


#======================================================================================================
def career_type_index(request):
    return render(request, 'cp/parameters/career_type.html')

#======================================================================================================
def career_level_index(request):
    return render(request, 'cp/parameters/career_level.html')

#======================================================================================================
def career_type_level_index(request):
    return render(request, 'cp/parameters/career_type_level.html')

#======================================================================================================
def location_index(request):
    return render(request, 'cp/parameters/location.html')

#======================================================================================================
def fte_index(request):
    return render(request, 'cp/parameters/fte.html')

#======================================================================================================
def job_catalogue_index(request):
    return render(request, 'cp/parameters/job_catalogue.html')