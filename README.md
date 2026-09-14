Nama : Nayla Putri Novita
NPM : 2506657182
Kelas : PBP A

### Tugas 1

1. **Penggunaan Elemen Semantik HTML5:**
   Ya, saya menggunakan elemen semantik HTML5 seperti `<header>`, `<main>`, `<section>`, dan `<footer>`. Penggunaan elemen-elemen ini sangat membantu dalam menyusun struktur *static web* karena membuat kode lebih terstruktur, mudah dibaca (*readable*), dan memisahkan bagian-b
   agian konten secara logis (seperti memisahkan bagian *Experience*, *Education*, dan *Skills*). Selain itu, penggunaan elemen semantik ini juga direkomendasikan untuk meningkatkan aksesibilitas (bagi pembaca layar) dan SEO.

2. **Tantangan CSS Responsive & Evaluasi Elemen:**
   Tantangan utamanya adalah memastikan elemen yang menggunakan tata letak berkolom (seperti bagian *Hero* atau *Grid* pada *Skills*) tidak terlihat sempit atau saling menumpuk saat diakses melalui perangkat dengan layar kecil (mobile). Saya melakukan evaluasi dengan menggunakan fitur *Inspect Element* (DevTools) untuk memeriksa tata letak pada berbagai ukuran layar. Saat ukuran layar mengecil dan konten terlihat terlalu padat untuk dibaca dengan nyaman, saya menggunakan *Media Queries* (`@media`) untuk mengubah tata letak elemen dari horizontal menjadi vertikal (satu kolom ke bawah), sehingga informasi tetap proporsional dan pengalaman pengguna (*user experience*) tetap baik.

3. **Batasan Static Web & Fungsionalitas Dinamis yang Diinginkan:**
   Batasan utama dari *static web* murni adalah data bersifat statis atau "hardcoded". Apabila saya ingin menambahkan pengalaman kerja, riwayat pendidikan, atau keahlian baru, saya harus memodifikasi langsung berkas HTML secara manual berulang kali. Fungsionalitas dinamis yang paling ingin saya persiapkan pada iterasi proyek selanjutnya adalah implementasi *database* dan *backend* (menggunakan arsitektur MVT Django) untuk menyimpan data portofolio. Dengan demikian, pembaruan konten dapat dilakukan secara langsung melalui halaman *dashboard admin* tanpa harus mengubah kode sumber HTML lagi.

**Penggunaan AI:**
Saya dibantu oleh AI Assistant (Gemini) dalam proses pengerjaan tugas ini, namun sebatas untuk membantu membuatkan kerangka dasar HTML serta memberikan ide implementasi CSS Grid dan Flexbox saat merancang penambahan *section* `Education` dan `Skills`. Setelah kerangka tersebut dibuat, tahapan implementasi tata letak yang spesifik, penulisan konten, desain, serta penyempurnaan kode agar berjalan lancar sepenuhnya saya kerjakan dan sesuaikan secara mandiri.


### Tugas 2
1. **Alur saat pengguna membuka halaman portofolio baru:**
   Saat pengguna membuka alamat seperti `/projects/`, alurnya berjalan sebagai berikut:
   - Request dari browser pertama kali masuk ke `portofolio/urls.py` (level proyek). Di sini Django membaca routing dan meneruskannya ke routing aplikasi `main` lewat fungsi `include()`.
   - Di `main/urls.py` (level aplikasi), Django mencocokkan path `'projects/'` dengan fungsi view yang dituju, yaitu `show_projects`.
   - Fungsi `show_projects` di `main/views.py` dijalankan. View ini bertugas mengambil data proyek dari database dengan memanggil `Project.objects.all()`.
   - Model `Project` di `main/models.py` mengambil data dari database SQLite sesuai permintaan view.
   - View memasukkan data tersebut ke dalam dictionary `context`, lalu merendernya bersama template `projects.html`.
   - Di `projects.html`, tag DTL (seperti perulangan `{% for %}`) menyusun data proyek menjadi tampilan HTML yang rapi.
   - Django mengembalikan hasil HTML tersebut ke browser pengguna untuk ditampilkan di layar.

2. **Alasan data disimpan di model dan bukan di template:**
   Lebih Mudah Dikelola: Kalau ada proyek baru atau ingin mengubah isi deskripsi, kita cukup mengupdate datanya di database/Django shell tanpa harus mengubah file HTML yang rawan merusak susunan CSS.
   Bisa Dipakai Berulang: Data yang ada di model bisa dipanggil kembali di berbagai halaman lain tanpa perlu menulis ulang teks yang sama.
   Mendukung Fitur Lanjutan: Dengan model, kita bisa dengan mudah menambahkan fitur seperti pencarian (search), filter kategori, atau sorting di kemudian hari.

3. **Perbedaan `makemigrations` dan `migrate` serta contohnya:**
   `makemigrations`: Bertugas mencatat perubahan yang kita buat di `models.py` dan menyimpannya sebagai file migrasi baru di folder `migrations/`. Perintah ini baru membuat rencana perubahannya, belum mengubah database fisik.
   `migrate`: Bertugas mengeksekusi file migrasi tersebut ke dalam database SQLite, sehingga tabel atau kolom baru benar-benar terbuat di database.
   Contoh: Saat saya membuat model baru `class Project(models.Model)` di `main/models.py`, saya harus menjalankan `python3 manage.py makemigrations` terlebih dahulu untuk membuat file migrasinya, lalu menjalankan `python3 manage.py migrate` agar tabel proyek resmi terbuat di database `db.sqlite3`.

**Penggunaan AI:**
Dalam pengerjaan Tugas 2 ini, saya memanfaatkan AI Assistant (Gemini) secara transparan sebagai rekan diskusi untuk membantu merancang struktur model `Project`, membimbing konfigurasi routing MVT bertahap, dan menyusun pengujian unit test. Seluruh kode, styling antarmuka, pengisian data portofolio, serta pemahaman alur kerja saya terapkan dan verifikasi secara mandiri.