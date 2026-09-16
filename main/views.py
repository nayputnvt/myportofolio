from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from main.models import Experience, Project
from main.forms import ExperienceForm
from django.db.models import Q 

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

# Halaman daftar proyek (dengan fitur pencarian)
def show_projects(request):
    search_query = request.GET.get('q', '').strip()
    if search_query:
        # Filter berdasarkan nama proyek (title) atau tech_stack atau deskripsi
        projects = Project.objects.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(tech_stack__icontains=search_query)
        )
    else:
        projects = Project.objects.all()
    context = {
        "name": "Nayla",
        "project_list": projects,
        "search_query": search_query,
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

# Mengembalikan seluruh data pengalaman dalam format XML
def show_xml(request):
    data = Experience.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# Mengembalikan seluruh data pengalaman dalam format JSON
def show_json(request):
    data = Experience.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# Mengembalikan 1 data pengalaman berdasarkan ID dalam format XML
def show_xml_by_id(request, id):
    data = Experience.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# Mengembalikan 1 data pengalaman berdasarkan ID dalam format JSON
def show_json_by_id(request, id):
    data = Experience.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")