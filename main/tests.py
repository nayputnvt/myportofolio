from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User, Group

from main.models import Experience, Project


class MainTest(TestCase):
    def setUp(self):
        # dummy user superuser, user biasa, dan editor
        self.admin_user = User.objects.create_superuser(
            username="nayla_admin",
            password="adminpassword123",
        )
        self.normal_user = User.objects.create_user(
            username="sasha_guest",
            password="userpassword123",
        )
        self.editor_group = Group.objects.create(name="Editor")
        self.editor_user = User.objects.create_user(
            username="budi_editor",
            password="editorpassword123",
        )
        self.editor_user.groups.add(self.editor_group)

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

    # test render struktur halaman experience (AJAX skeleton) & get_experiences_json
    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, 'id="experience-grid"')
        self.assertContains(response, 'id="search-input"')
        self.assertContains(response, f'href="{reverse("main:show_main")}"')
        self.assertContains(response, f'href="{reverse("main:show_projects")}"')

        # test endpoint AJAX get_experiences_json
        json_res = self.client.get(reverse("main:get_experiences_json"))
        self.assertEqual(json_res.status_code, 200)
        data = json_res.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], self.experience.title)

    # test tampilan kalau database experience lagi kosong
    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)

        # test endpoint AJAX get_experiences_json mengembalikan list kosong
        json_res = self.client.get(reverse("main:get_experiences_json"))
        self.assertEqual(json_res.status_code, 200)
        self.assertEqual(json_res.json(), [])

    # test pencarian via AJAX get_experiences_json
    def test_get_experiences_json_search(self):
        response = self.client.get(reverse("main:get_experiences_json") + "?title=Software")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], self.experience.title)

        # pencarian dengan kata kunci yang tidak cocok
        response_empty = self.client.get(reverse("main:get_experiences_json") + "?title=NonExistent")
        self.assertEqual(response_empty.status_code, 200)
        self.assertEqual(response_empty.json(), [])

    # test status kalau tanggal selesai diisi
    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        self.assertFalse(self.experience.is_ongoing)

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

    # test render struktur halaman projects (AJAX skeleton)
    def test_projects_page_displays_data(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="projects-grid"')
        self.assertContains(response, 'id="search-input"')

        # test endpoint AJAX get_projects_json
        json_res = self.client.get(reverse("main:get_projects_json"))
        self.assertEqual(json_res.status_code, 200)
        data = json_res.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], self.project.title)

    # test tampilan kalau database project lagi kosong
    def test_empty_projects_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_projects"))
        self.assertEqual(response.status_code, 200)

        # test endpoint AJAX get_projects_json mengembalikan list kosong
        json_res = self.client.get(reverse("main:get_projects_json"))
        self.assertEqual(json_res.status_code, 200)
        self.assertEqual(json_res.json(), [])

    # test pencarian via AJAX get_projects_json
    def test_get_projects_json_search(self):
        response = self.client.get(reverse("main:get_projects_json") + "?title=Personal")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], self.project.title)

        # pencarian dengan kata kunci yang tidak ada
        response_empty = self.client.get(reverse("main:get_projects_json") + "?title=NonExistent")
        self.assertEqual(response_empty.status_code, 200)
        self.assertEqual(response_empty.json(), [])

    # test akses halaman form tambah pengalaman (GET)
    def test_create_experience_page_accessible(self):
        self.client.login(username="nayla_admin", password="adminpassword123")
        response = self.client.get(reverse("main:create_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_experience.html")

    # test submit form tambah pengalaman berhasil menyimpan data (POST)
    def test_create_experience_post_success(self):
        self.client.login(username="nayla_admin", password="adminpassword123")
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
        self.client.login(username="nayla_admin", password="adminpassword123")
        response = self.client.get(reverse("main:create_project"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_project.html")

    # test submit form tambah project berhasil (POST)
    def test_create_project_post_success(self):
        self.client.login(username="nayla_admin", password="adminpassword123")
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

    # test edit project (GET & POST) oleh Superuser
    def test_edit_project(self):
        self.client.login(username="nayla_admin", password="adminpassword123")
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

    # test delete project oleh Superuser
    def test_delete_project(self):
        self.client.login(username="nayla_admin", password="adminpassword123")
        response = self.client.get(reverse("main:delete_project", args=[str(self.project.id)]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Project.objects.filter(id=self.project.id).exists())

    # test edit experience oleh Superuser
    def test_edit_experience(self):
        self.client.login(username="nayla_admin", password="adminpassword123")
        response = self.client.get(reverse("main:edit_experience", args=[str(self.experience.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_experience.html")

        response_post = self.client.post(reverse("main:edit_experience", args=[str(self.experience.id)]), {
            "title": "Senior Software Engineer Intern",
            "description": "Membantu pengembangan arsitektur web aplikasi.",
            "category": "full-time",
        })
        self.assertEqual(response_post.status_code, 302)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Senior Software Engineer Intern")

    # test delete experience oleh Superuser
    def test_delete_experience(self):
        self.client.login(username="nayla_admin", password="adminpassword123")
        response = self.client.get(reverse("main:delete_experience", args=[str(self.experience.id)]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Experience.objects.filter(id=self.experience.id).exists())

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

    # test registrasi akun baru
    def test_register_user(self):
        response = self.client.post(reverse("main:register"), {
            "username": "newuser",
            "password1": "ComplexPass123!@",
            "password2": "ComplexPass123!@",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    # test login dan cookie last_login
    def test_login_and_last_login_cookie(self):
        response = self.client.post(reverse("main:login"), {
            "username": "sasha_guest",
            "password": "userpassword123",
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn("last_login", response.cookies)

    # test logout dan pembersihan cookie
    def test_logout_user(self):
        self.client.login(username="sasha_guest", password="userpassword123")
        response = self.client.get(reverse("main:logout"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.cookies["last_login"].value, "")

    # test otorisasi: pengguna belum login diarahkan ke login saat buat data
    def test_unauthenticated_redirects_to_login(self):
        # test create project
        response_project = self.client.get(reverse("main:create_project"))
        self.assertEqual(response_project.status_code, 302)
        self.assertIn(reverse("main:login"), response_project.url)

        # test create experience
        response_exp = self.client.get(reverse("main:create_experience"))
        self.assertEqual(response_exp.status_code, 302)
        self.assertIn(reverse("main:login"), response_exp.url)

    # test otorisasi: pengguna biasa (non-superuser) ditolak 403 saat buat data
    def test_regular_user_cannot_create_or_delete(self):
        self.client.login(username="sasha_guest", password="userpassword123")
        # tidak bisa create
        self.assertEqual(self.client.get(reverse("main:create_project")).status_code, 403)
        self.assertEqual(self.client.get(reverse("main:create_experience")).status_code, 403)
        # tidak bisa edit
        self.assertEqual(self.client.get(reverse("main:edit_project", args=[str(self.project.id)])).status_code, 403)
        self.assertEqual(self.client.get(reverse("main:edit_experience", args=[str(self.experience.id)])).status_code, 403)
        # tidak bisa delete
        self.assertEqual(self.client.get(reverse("main:delete_project", args=[str(self.project.id)])).status_code, 403)
        self.assertEqual(self.client.get(reverse("main:delete_experience", args=[str(self.experience.id)])).status_code, 403)

    # test otorisasi: Editor diizinkan edit, tetapi dilarang create dan delete (403)
    def test_editor_role_permissions(self):
        self.client.login(username="budi_editor", password="editorpassword123")

        # Editor BISA mengakses halaman edit
        self.assertEqual(self.client.get(reverse("main:edit_project", args=[str(self.project.id)])).status_code, 200)
        self.assertEqual(self.client.get(reverse("main:edit_experience", args=[str(self.experience.id)])).status_code, 200)

        # Editor BISA update data lewat form edit
        res_edit_proj = self.client.post(reverse("main:edit_project", args=[str(self.project.id)]), {
            "title": "Edited by Editor",
            "description": "Description edited by editor.",
            "category": "Web Development",
            "tech_stack": "Python, Django",
        })
        self.assertEqual(res_edit_proj.status_code, 302)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Edited by Editor")

        # Editor TIDAK BISA create (403)
        self.assertEqual(self.client.get(reverse("main:create_project")).status_code, 403)
        self.assertEqual(self.client.get(reverse("main:create_experience")).status_code, 403)

        # Editor TIDAK BISA delete (403)
        self.assertEqual(self.client.get(reverse("main:delete_project", args=[str(self.project.id)])).status_code, 403)
        self.assertEqual(self.client.get(reverse("main:delete_experience", args=[str(self.experience.id)])).status_code, 403)

    # test fitur toggle star pada project
    def test_toggle_star_project(self):
        self.client.login(username="sasha_guest", password="userpassword123")

        # beri star
        response = self.client.post(reverse("main:toggle_star", args=[str(self.project.id)]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.project.starred_by.filter(username="sasha_guest").exists())

        # batalkan star
        response_unstar = self.client.post(reverse("main:toggle_star", args=[str(self.project.id)]))
        self.assertEqual(response_unstar.status_code, 302)
        self.assertFalse(self.project.starred_by.filter(username="sasha_guest").exists())

    # test fitur toggle star pada experience
    def test_toggle_star_experience(self):
        self.client.login(username="sasha_guest", password="userpassword123")

        # beri star pada experience
        response = self.client.post(reverse("main:toggle_experience_star", args=[str(self.experience.id)]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.experience.starred_by.filter(username="sasha_guest").exists())

        # batalkan star pada experience
        response_unstar = self.client.post(reverse("main:toggle_experience_star", args=[str(self.experience.id)]))
        self.assertEqual(response_unstar.status_code, 302)
        self.assertFalse(self.experience.starred_by.filter(username="sasha_guest").exists())

    # test tambah proyek via AJAX POST oleh Superuser
    def test_create_project_ajax_success(self):
        self.client.login(username="nayla_admin", password="adminpassword123")
        response = self.client.post(reverse("main:create_project_ajax"), {
            "title": "Machine Learning Dashboard",
            "description": "Interactive analytics dashboard with Scikit-learn.",
            "category": "Data Science",
            "tech_stack": "Python, Django, Pandas",
            "project_url": "https://github.com/nayputnvt/ml-dashboard",
            "thumbnail": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800",
        })

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertTrue(Project.objects.filter(title="Machine Learning Dashboard").exists())

    # test otorisasi create_project_ajax untuk user non-superuser
    def test_create_project_ajax_permission_denied(self):
        # user belum login
        response_unauth = self.client.post(reverse("main:create_project_ajax"), {
            "title": "Unauthorized Project",
            "description": "Should fail",
        })
        self.assertEqual(response_unauth.status_code, 302)

        # user biasa (bukan superuser)
        self.client.login(username="sasha_guest", password="userpassword123")
        response_user = self.client.post(reverse("main:create_project_ajax"), {
            "title": "Unauthorized Project",
            "description": "Should fail",
        })
        self.assertEqual(response_user.status_code, 403)

        # editor (bukan superuser)
        self.client.login(username="budi_editor", password="editorpassword123")
        response_editor = self.client.post(reverse("main:create_project_ajax"), {
            "title": "Unauthorized Project",
            "description": "Should fail",
        })
        self.assertEqual(response_editor.status_code, 403)

    # test sanitasi XSS (strip_tags) pada form input proyek
    def test_project_form_strip_tags_xss(self):
        self.client.login(username="nayla_admin", password="adminpassword123")
        xss_payload = "<script>alert('xss_attack');</script>Aplikasi Aman"
        
        response = self.client.post(reverse("main:create_project_ajax"), {
            "title": xss_payload,
            "description": "<p>Deskripsi <b>bold</b> <script>alert('xss');</script></p>",
            "category": "Web Development",
            "tech_stack": "HTML, <script>malicious()</script>CSS",
        })

        self.assertEqual(response.status_code, 201)
        created_project = Project.objects.get(title__contains="Aplikasi Aman")
        self.assertNotIn("<script>", created_project.title)
        self.assertNotIn("</script>", created_project.title)
        self.assertNotIn("<script>", created_project.description)
        self.assertNotIn("<p>", created_project.description)
        self.assertNotIn("<script>", created_project.tech_stack)

    # test tambah experience via ajax post oleh superuser
    def test_create_experience_ajax_success(self):
        self.client.login(username="nayla_admin", password="adminpassword123")
        response = self.client.post(reverse("main:create_experience_ajax"), {
            "title": "Data Analyst Intern",
            "description": "Mengolah dan memvisualisasikan data bisnis menggunakan Python.",
            "category": "internship",
        })

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertTrue(Experience.objects.filter(title="Data Analyst Intern").exists())

    # test otorisasi create_experience_ajax untuk user non-superuser
    def test_create_experience_ajax_permission_denied(self):
        # user belum login dialihkan ke login (302)
        response_unauth = self.client.post(reverse("main:create_experience_ajax"), {
            "title": "Unauthorized Experience",
            "description": "Should fail",
            "category": "internship",
        })
        self.assertEqual(response_unauth.status_code, 302)

        # user biasa (bukan superuser) dilarang (403)
        self.client.login(username="sasha_guest", password="userpassword123")
        response_user = self.client.post(reverse("main:create_experience_ajax"), {
            "title": "Unauthorized Experience",
            "description": "Should fail",
            "category": "internship",
        })
        self.assertEqual(response_user.status_code, 403)

        # editor (bukan superuser) dilarang (403)
        self.client.login(username="budi_editor", password="editorpassword123")
        response_editor = self.client.post(reverse("main:create_experience_ajax"), {
            "title": "Unauthorized Experience",
            "description": "Should fail",
            "category": "internship",
        })
        self.assertEqual(response_editor.status_code, 403)

    # test sanitasi xss (strip_tags) pada form input experience
    def test_experience_form_strip_tags_xss(self):
        self.client.login(username="nayla_admin", password="adminpassword123")
        xss_payload = "<script>alert('xss_attack');</script>Frontend Developer"
        
        response = self.client.post(reverse("main:create_experience_ajax"), {
            "title": xss_payload,
            "description": "<p>Deskripsi pengalaman <script>alert('xss');</script></p>",
            "category": "freelance",
        })

        self.assertEqual(response.status_code, 201)
        created_exp = Experience.objects.get(title__contains="Frontend Developer")
        self.assertNotIn("<script>", created_exp.title)
        self.assertNotIn("</script>", created_exp.title)
        self.assertNotIn("<script>", created_exp.description)
        self.assertNotIn("<p>", created_exp.description)