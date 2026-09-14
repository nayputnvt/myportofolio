from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Project


class MainTest(TestCase):
    def setUp(self):
        # dummy data buat testing
        self.experience = Experience.objects.create(
            title="Software Engineer Intern",
            description="Membantu pengembangan fitur web aplikasi.",
            category="part-time",
        )

        self.project = Project.objects.create(
            title="Personal Static Portfolio",
            description="Responsive personal portfolio website built with semantic HTML5.",
            category="Web Development",
            tech_stack="HTML5, CSS3, Git",
            project_url="https://github.com/nayputnvt/myportofolio",
        )

    # test halaman home & link navbar
    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')
        self.assertContains(response, f'href="{reverse("main:show_projects")}"')

    # test kalau url asal / gak ada (404)
    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    # test atribut di model experience
    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Software Engineer Intern")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    # test render konten halaman experience
    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')
        self.assertContains(response, f'href="{reverse("main:show_projects")}"')

    # test tampilan kalau database experience lagi kosong
    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    # test status kalau tanggal selesai diisi
    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

    # test atribut di model project
    def test_project_model(self):
        self.assertEqual(str(self.project), "Personal Static Portfolio")
        self.assertEqual(self.project.category, "Web Development")
        self.assertEqual(self.project.tech_stack, "HTML5, CSS3, Git")

    # test akses routing halaman projects
    def test_projects_page_accessible_and_using_template(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    # test render konten data project
    def test_projects_page_displays_data(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)
        self.assertContains(response, self.project.category)
        self.assertContains(response, self.project.tech_stack)
        self.assertContains(response, self.project.project_url)

    # test tampilan kalau database project lagi kosong
    def test_empty_projects_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Belum ada proyek yang ditambahkan.")