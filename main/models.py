import uuid
from django.db import models

# Model untuk menyimpan riwayat pengalaman dan organisasi
class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    # return True jika kegiatan belum ada tanggal selesai (masih berlangsung)
    @property
    def is_ongoing(self):
        return self.ended_at is None


# Model untuk menyimpan daftar proyek portofolio
class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, default='Web Development')
    tech_stack = models.CharField(max_length=255, blank=True, null=True) # teknologi atau bahasa pemrograman yang dipakai
    project_url = models.URLField(blank=True, null=True) # tautan repo github atau live demo
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title