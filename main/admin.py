from django.contrib import admin
from main.models import Experience, Project

# Mendaftarkan model Experience dan Project
admin.site.register(Experience)
admin.site.register(Project)

# Custom judul dan nama website di halaman Admin
admin.site.site_header = "Nayla Putri Novita • Admin Portal"
admin.site.site_title = "Nayla Portfolio Admin"
admin.site.index_title = "Kelola Data Portfolio & Pengalaman"