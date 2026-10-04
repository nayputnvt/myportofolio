from django.forms import ModelForm
from django.utils.html import strip_tags
from main.models import Experience, Project

# form buat nambah pengalaman
class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ["title", "description", "category", "thumbnail"]

    # sanitasi input pengalaman biar aman dari xss
    def clean_title(self):
        title = self.cleaned_data.get("title", "")
        return strip_tags(title)

    def clean_description(self):
        description = self.cleaned_data.get("description", "")
        return strip_tags(description)

    def clean_category(self):
        category = self.cleaned_data.get("category", "")
        return strip_tags(category)

# form buat nambah project
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "category", "thumbnail", "tech_stack", "project_url"]

    # sanitasi input teks project di server biar aman dari xss
    def clean_title(self):
        title = self.cleaned_data.get("title", "")
        return strip_tags(title)

    def clean_description(self):
        description = self.cleaned_data.get("description", "")
        return strip_tags(description)

    def clean_category(self):
        category = self.cleaned_data.get("category", "")
        return strip_tags(category)

    def clean_tech_stack(self):
        tech_stack = self.cleaned_data.get("tech_stack", "")
        if tech_stack:
            return strip_tags(tech_stack)
        return tech_stack