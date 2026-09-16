from django.shortcuts import render


def research(request):
    return render(request, 'research/research.html')


def doctor_of_philosophy(request):
    return render(request, 'research/doctor-of-philosophy.html')


def master_of_philosophy(request):
    return render(request, 'research/master-of-philosophy.html')


def master_of_research_methodology(request):
    return render(request, 'research/master-of-research-methodology.html')


def doctor_of_education(request):
    return render(request, 'research/doctor-of-education.html')
