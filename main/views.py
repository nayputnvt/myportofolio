import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Q 
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from main.models import Experience, Project
from main.forms import ExperienceForm, ProjectForm

# Halaman registrasi akun
def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Nayla",
        "form": form,
    }
    return render(request, "register.html", context)

# Halaman login & simpan cookie last_login
def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie("last_login", str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        return response

    context = {
        "name": "Nayla",
        "form": form,
    }
    return render(request, "login.html", context)

# Halaman logout & hapus cookie last_login
def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response

# Halaman profil / home
def show_main(request):
    last_login = request.COOKIES.get("last_login", "Belum ada sesi login / Cookie tidak ditemukan")
    context = {
        "name": "Nayla",
        "npm": "2506657182",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Information Systems student at Universitas Indonesia passionate "
            "about web development, technology solutions, and building impactful digital products."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)

# Halaman daftar pengalaman
def show_experience(request):
    # Cek apakah pengguna memiliki hak akses Editor atau Superuser
    is_editor = request.user.is_authenticated and (request.user.is_superuser or request.user.groups.filter(name='Editor').exists())
    context = {
        "name": "Nayla",
        "experience_list": Experience.objects.all(),
        "is_editor": is_editor,
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
    
    # Cek apakah pengguna memiliki hak akses Editor atau Superuser
    is_editor = request.user.is_authenticated and (request.user.is_superuser or request.user.groups.filter(name='Editor').exists())
    context = {
        "name": "Nayla",
        "project_list": projects,
        "search_query": search_query,
        "is_editor": is_editor,
    }
    return render(request, "projects.html", context)

# Form tambah pengalaman baru
@login_required(login_url="/login/")
def create_experience(request):
    # Hanya Superuser (pemilik portofolio) yang boleh membuat data baru
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ExperienceForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_experience')

    context = {
        "name": "Nayla",
        "form": form,
    }
    return render(request, "create_experience.html", context)

# Form tambah proyek baru
@login_required(login_url="/login/")
def create_project(request):
    # Hanya Superuser (pemilik portofolio) yang boleh membuat proyek baru
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_projects')

    context = {
        "name": "Nayla",
        "form": form,
    }
    return render(request, "create_project.html", context)

# Fungsi untuk mengedit proyek yang sudah ada
@login_required(login_url="/login/")
def edit_project(request, id):
    # Superuser dan Editor diizinkan untuk mengubah data proyek
    if not (request.user.is_superuser or request.user.groups.filter(name='Editor').exists()):
        raise PermissionDenied

    project = get_object_or_404(Project, pk=id)
    form = ProjectForm(request.POST or None, instance=project)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_projects')

    context = {
        "name": "Nayla",
        "form": form,
        "project": project,
    }
    return render(request, "edit_project.html", context)

# Fungsi untuk menghapus proyek
@login_required(login_url="/login/")
def delete_project(request, id):
    # Hanya Superuser yang boleh menghapus data proyek
    if not request.user.is_superuser:
        raise PermissionDenied

    project = get_object_or_404(Project, pk=id)
    project.delete()
    return redirect('main:show_projects')

# Fungsi untuk memberi atau membatalkan star pada proyek
@login_required(login_url="/login/")
def toggle_star(request, id):
    project = get_object_or_404(Project, pk=id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect('main:show_projects')

# Fungsi untuk mengedit pengalaman
@login_required(login_url="/login/")
def edit_experience(request, id):
    # Superuser dan Editor diizinkan untuk mengubah data pengalaman
    if not (request.user.is_superuser or request.user.groups.filter(name='Editor').exists()):
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_experience')

    context = {
        "name": "Nayla",
        "form": form,
        "experience": experience,
    }
    return render(request, "edit_experience.html", context)

# Fungsi untuk menghapus pengalaman
@login_required(login_url="/login/")
def delete_experience(request, id):
    # Hanya Superuser yang boleh menghapus data pengalaman
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=id)
    experience.delete()
    return redirect('main:show_experience')

# Fungsi untuk memberi atau membatalkan star pada pengalaman
@login_required(login_url="/login/")
def toggle_experience_star(request, id):
    experience = get_object_or_404(Experience, pk=id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect('main:show_experience')

# Mengembalikan seluruh data pengalaman dalam format XML
def show_xml(request):
    data = Experience.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# Mengembalikan seluruh data pengalaman dalam format JSON
def show_json(request):
    data = Experience.objects.all()
    return HttpResponse(serializers.serialize("json", data, use_natural_foreign_keys=True), content_type="application/json")

# Mengembalikan 1 data pengalaman berdasarkan ID dalam format XML
def show_xml_by_id(request, id):
    data = Experience.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# Mengembalikan 1 data pengalaman berdasarkan ID dalam format JSON
def show_json_by_id(request, id):
    data = Experience.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data, use_natural_foreign_keys=True), content_type="application/json")

# Mengembalikan seluruh data proyek dalam format XML
def show_project_xml(request):
    data = Project.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# Mengembalikan seluruh data proyek dalam format JSON
def show_project_json(request):
    data = Project.objects.all()
    return HttpResponse(serializers.serialize("json", data, use_natural_foreign_keys=True), content_type="application/json")

# Mengembalikan 1 data proyek berdasarkan ID dalam format XML
def show_project_xml_by_id(request, id):
    data = Project.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# Mengembalikan 1 data proyek berdasarkan ID dalam format JSON
def show_project_json_by_id(request, id):
    data = Project.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data, use_natural_foreign_keys=True), content_type="application/json")