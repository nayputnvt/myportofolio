import datetime
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.db.models import Q 
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
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
        response.set_cookie("last_login", str(timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")))
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

# Halaman daftar pengalaman (rendering kerangka untuk AJAX)
def show_experience(request):
    title_query = request.GET.get('title', '').strip() or request.GET.get('q', '').strip()
    is_editor = request.user.is_authenticated and (request.user.is_superuser or request.user.groups.filter(name='Editor').exists())
    context = {
        "name": "Nayla",
        "title_query": title_query,
        "is_editor": is_editor,
    }
    return render(request, "experience.html", context)

# Halaman daftar proyek (rendering kerangka untuk AJAX)
def show_projects(request):
    title_query = request.GET.get('title', '').strip() or request.GET.get('q', '').strip()
    is_editor = request.user.is_authenticated and (request.user.is_superuser or request.user.groups.filter(name='Editor').exists())
    context = {
        "name": "Nayla",
        "title_query": title_query,
        "is_editor": is_editor,
    }
    return render(request, "projects.html", context)

# form tambah pengalaman baru (halaman standar)
@login_required(login_url="/login/")
def create_experience(request):
    # cuma superuser yang boleh bikin data baru
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

# tambah pengalaman baru pake ajax post
@login_required(login_url="/login/")
@require_POST
def create_experience_ajax(request):
    # cuma superuser yang boleh nambah data lewat ajax
    if not request.user.is_superuser:
        return JsonResponse({"status": "error", "message": "Unauthorized"}, status=403)

    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse({
            "status": "success",
            "message": "Pengalaman baru berhasil ditambahkan!",
            "experience": {
                "pk": str(experience.pk),
                "title": experience.title,
                "category": experience.category,
                "category_display": experience.get_category_display(),
                "description": experience.description,
                "thumbnail": experience.thumbnail or "",
                "is_ongoing": experience.is_ongoing,
                "started_at": experience.started_at.strftime("%Y-%m-%d") if experience.started_at else "",
                "ended_at": experience.ended_at.strftime("%Y-%m-%d") if experience.ended_at else "",
                "star_count": experience.starred_by.count(),
                "is_starred": False,
            }
        }, status=201)

    return JsonResponse({
        "status": "error",
        "message": "Data form tidak valid.",
        "errors": form.errors
    }, status=400)

# Form tambah proyek baru (halaman standar)
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

# Tambah proyek baru via AJAX POST
@login_required(login_url="/login/")
@require_POST
def create_project_ajax(request):
    # Hanya Superuser (pemilik portofolio) yang diizinkan menambah data via AJAX
    if not request.user.is_superuser:
        return JsonResponse({"status": "error", "message": "Unauthorized"}, status=403)

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse({
            "status": "success",
            "message": "Proyek baru berhasil ditambahkan!",
            "project": {
                "pk": str(project.pk),
                "title": project.title,
                "category": project.category,
                "description": project.description,
                "tech_stack": project.tech_stack or "",
                "thumbnail": project.thumbnail or "",
                "project_url": project.project_url or "",
                "star_count": project.starred_by.count(),
                "is_starred": False,
            }
        }, status=201)

    return JsonResponse({
        "status": "error",
        "message": "Data form tidak valid.",
        "errors": form.errors
    }, status=400)

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

# ambil data pengalaman format json buat ajax dan pencarian
def get_experiences_json(request):
    title_query = request.GET.get('title', '').strip() or request.GET.get('q', '').strip()
    experiences = Experience.objects.all()

    # filter kalau ada query pencarian
    if title_query:
        experiences = experiences.filter(
            Q(title__icontains=title_query) | 
            Q(description__icontains=title_query) |
            Q(category__icontains=title_query)
        )

    data = []
    for exp in experiences:
        data.append({
            "pk": str(exp.pk),
            "title": exp.title,
            "description": exp.description,
            "category": exp.category,
            "category_display": exp.get_category_display(),
            "thumbnail": exp.thumbnail or "",
            "is_ongoing": exp.is_ongoing,
            "started_at": exp.started_at.strftime("%Y-%m-%d") if exp.started_at else "",
            "ended_at": exp.ended_at.strftime("%Y-%m-%d") if exp.ended_at else "",
            "star_count": exp.starred_by.count(),
            "is_starred": request.user.is_authenticated and exp.starred_by.filter(pk=request.user.pk).exists(),
            "starred_by_names": [user.username for user in exp.starred_by.all()],
        })

    return JsonResponse(data, safe=False)

# alias show_json biar kompatibel
show_json = get_experiences_json

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

# Mengembalikan data proyek dalam format JSON untuk AJAX dan pencarian dinamis
def get_projects_json(request):
    title_query = request.GET.get('title', '').strip() or request.GET.get('q', '').strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    data = []
    for project in projects:
        data.append({
            "pk": str(project.pk),
            "title": project.title,
            "description": project.description,
            "category": project.category,
            "tech_stack": project.tech_stack or "",
            "project_url": project.project_url or "",
            "thumbnail": project.thumbnail or "",
            "star_count": project.starred_by.count(),
            "is_starred": request.user.is_authenticated and project.starred_by.filter(pk=request.user.pk).exists(),
            "starred_by_names": [user.username for user in project.starred_by.all()],
        })

    return JsonResponse(data, safe=False)

# Alias untuk show_project_json agar kompatibel
show_project_json = get_projects_json

# Mengembalikan 1 data proyek berdasarkan ID dalam format XML
def show_project_xml_by_id(request, id):
    data = Project.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# Mengembalikan 1 data proyek berdasarkan ID dalam format JSON
def show_project_json_by_id(request, id):
    data = Project.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data, use_natural_foreign_keys=True), content_type="application/json")