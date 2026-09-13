from django.shortcuts import render
from main.models import Experience, Project

# Halaman profil / home
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

# Halaman daftar pengalaman
def show_experience(request):
    context = {
        "name": "Nayla",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

# Halaman daftar proyek
def show_projects(request):
    context = {
        "name": "Nayla",
        "project_list": Project.objects.all(),
    }
    return render(request, "projects.html", context)