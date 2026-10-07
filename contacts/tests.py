from django.test import TestCase
from django.urls import reverse
from .models import Contact

class ContactsHTMXTest(TestCase):
    def setUp(self):
        # buat data dummy kontak buat testing
        self.contact = Contact.objects.create(
            name="Nayla Putri",
            email="nayla@example.com",
            phone="08123456789"
        )

    # test halaman utama contacts
    def test_contact_list_page(self):
        response = self.client.get(reverse("contacts:contact_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacts/index.html")
        self.assertContains(response, "Nayla Putri")
        self.assertContains(response, "nayla@example.com")

    # test tambah kontak via htmx post
    def test_contact_add_htmx(self):
        response = self.client.post(reverse("contacts:contact_add"), {
            "name": "Budi Santoso",
            "email": "budi@example.com",
            "phone": "08987654321"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacts/_contact_rows.html")
        self.assertTrue(Contact.objects.filter(name="Budi Santoso").exists())
        self.assertContains(response, "Budi Santoso")

    # test live search kontak via htmx get
    def test_contact_search_htmx(self):
        # cari yang cocok
        response = self.client.get(reverse("contacts:contact_search") + "?q=Nayla")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nayla Putri")

        # cari yang gak ada
        response_empty = self.client.get(reverse("contacts:contact_search") + "?q=NonExistentPerson")
        self.assertEqual(response_empty.status_code, 200)
        self.assertContains(response_empty, "Belum ada kontak yang ditemukan")

    # test hapus kontak via htmx delete
    def test_contact_delete_htmx(self):
        response = self.client.delete(reverse("contacts:contact_delete", args=[self.contact.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "")
        self.assertFalse(Contact.objects.filter(id=self.contact.id).exists())

    # test request form edit baris
    def test_contact_edit_row_htmx(self):
        response = self.client.get(reverse("contacts:contact_edit", args=[self.contact.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacts/_contact_edit_row.html")
        self.assertContains(response, f'value="{self.contact.name}"')

    # test batal edit baris
    def test_contact_cancel_row_htmx(self):
        response = self.client.get(reverse("contacts:contact_row", args=[self.contact.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacts/_contact_row.html")
        self.assertContains(response, self.contact.name)

    # test update kontak via htmx put
    def test_contact_update_htmx(self):
        payload = "name=Nayla+Updated&email=nayla.updated%40example.com&phone=0811111111"
        response = self.client.put(
            reverse("contacts:contact_update", args=[self.contact.id]),
            data=payload,
            content_type="application/x-www-form-urlencoded"
        )
        self.assertEqual(response.status_code, 200)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, "Nayla Updated")
        self.assertEqual(self.contact.email, "nayla.updated@example.com")
        self.assertEqual(self.contact.phone, "0811111111")
