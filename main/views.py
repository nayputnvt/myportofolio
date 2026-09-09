from django.shortcuts import render
from main.models import Experience

def show_main(request):
    context = {
        "name": "Nayla",
        "npm": "2506657182",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Information Systems student at Universitas Indonesia passionate "
            "about web development, technology solutions, and building impactful digital products."
        ),
    }
    return render(request, "index.html", context)

def show_experience(request):
    context = {
        "name": "Nayla",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)