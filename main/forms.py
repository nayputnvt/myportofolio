from django.forms import ModelForm
from main.models import Experience, Project

# Form untuk menambah pengalaman baru
class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ["title", "description", "category", "thumbnail"]

# Form untuk menambah proyek baru (lengkap dengan thumbnail foto)
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "category", "thumbnail", "tech_stack", "project_url"]