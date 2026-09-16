from django.shortcuts import render, redirect
from main.models import Experience, Project
from main.forms import ExperienceForm

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

# Form tambah pengalaman baru
def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_experience')

    context = {
        "name": "Nayla",
        "form": form,
    }
    return render(request, "create_experience.html", context)