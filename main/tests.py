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
            thumbnail="https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800",
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

    # test tampilan kalau database project lagi kosong
    def test_empty_projects_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Belum ada proyek yang ditambahkan.")

    # test akses halaman form tambah pengalaman (GET)
    def test_create_experience_page_accessible(self):
        response = self.client.get(reverse("main:create_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_experience.html")

    # test submit form tambah pengalaman berhasil menyimpan data (POST)
    def test_create_experience_post_success(self):
        response = self.client.post(reverse("main:create_experience"), {
            "title": "Graphic Designer",
            "description": "Membuat aset visual dan promosi event kampus.",
            "category": "volunteer",
        })

        self.assertEqual(response.status_code, 302)  # redirect ke experience list
        self.assertTrue(Experience.objects.filter(title="Graphic Designer").exists())

    # test delivery seluruh data format XML
    def test_show_xml_status_and_content_type(self):
        response = self.client.get(reverse("main:show_xml"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")

    # test delivery seluruh data format JSON
    def test_show_json_status_and_content_type(self):
        response = self.client.get(reverse("main:show_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

    # test delivery data by id format XML
    def test_show_xml_by_id(self):
        response = self.client.get(reverse("main:show_xml_by_id", args=[str(self.experience.id)]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")

    # test delivery data by id format JSON
    def test_show_json_by_id(self):
        response = self.client.get(reverse("main:show_json_by_id", args=[str(self.experience.id)]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

    # test akses halaman form tambah project (GET)
    def test_create_project_page_accessible(self):
        response = self.client.get(reverse("main:create_project"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_project.html")

    # test submit form tambah project berhasil (POST)
    def test_create_project_post_success(self):
        response = self.client.post(reverse("main:create_project"), {
            "title": "AI Task Manager",
            "description": "Aplikasi manajemen tugas berbasis AI.",
            "category": "Web Development",
            "tech_stack": "Django, Python",
            "project_url": "https://github.com/nayputnvt/myportofolio",
            "thumbnail": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800",
        })

        self.assertEqual(response.status_code, 302)  # redirect ke project list
        self.assertTrue(Project.objects.filter(title="AI Task Manager").exists())

    # test edit project (GET & POST)
    def test_edit_project(self):
        # test akses halaman edit
        response = self.client.get(reverse("main:edit_project", args=[str(self.project.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_project.html")

        # test update data proyek
        response_post = self.client.post(reverse("main:edit_project", args=[str(self.project.id)]), {
            "title": "Updated Portfolio Project",
            "description": "Updated project description.",
            "category": "Web Development",
            "tech_stack": "Django, HTML5, CSS3",
            "project_url": "https://github.com/nayputnvt/myportofolio",
            "thumbnail": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800",
        })
        self.assertEqual(response_post.status_code, 302)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Updated Portfolio Project")

    # test delete project
    def test_delete_project(self):
        response = self.client.get(reverse("main:delete_project", args=[str(self.project.id)]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Project.objects.filter(id=self.project.id).exists())

    # test delivery seluruh data project format XML
    def test_show_project_xml_status_and_content_type(self):
        response = self.client.get(reverse("main:show_project_xml"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")

    # test delivery seluruh data project format JSON
    def test_show_project_json_status_and_content_type(self):
        response = self.client.get(reverse("main:show_project_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

    # test delivery data project by id format JSON
    def test_show_project_json_by_id(self):
        response = self.client.get(reverse("main:show_project_json_by_id", args=[str(self.project.id)]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")