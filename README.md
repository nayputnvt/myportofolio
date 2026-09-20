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


### Tugas 3

1. **Mengapa kita menggunakan `ModelForm` pada Django alih-alih membuat form HTML secara manual? Jelaskan pula mengapa kita diwajibkan menambahkan `{% csrf_token %}` pada form tersebut!**
   - **Keunggulan `ModelForm` dibandingkan Form HTML Manual:**
     - **Prinsip DRY (*Don't Repeat Yourself*):** `ModelForm` secara otomatis membaca definisi field dari model Django (`models.Model`) dan menghasilkan field input HTML yang sesuai secara otomatis. Kita tidak perlu menulis tag `<input>`, `<textarea>`, label, dan atribut validasi satu per satu secara manual di file template.
     - **Validasi Otomatis dan Sanitasi Data:** Saat memanggil `form.is_valid()`, Django secara otomatis memeriksa kesesuaian tipe data, batasan panjang karakter (`max_length`), keabsahan URL (`URLField`), dan membersihkan input dari script berbahaya (*sanitization*) melalui `cleaned_data`. Jika membuat form manual, developer harus mengambil input satu per satu via `request.POST.get(...)` dan menulis validasi manual yang panjang dan rentan kesalahan.
     - **Integrasi Erat dengan Database (ORM):** Dengan memanggil `form.save()`, Django langsung menyimpan data baru atau memperbarui data yang ada di database secara otomatis tanpa perlu menulis query ORM manual.
     - **Manajemen Pesan Error Terstruktur:** Jika input pengguna tidak valid, `ModelForm` otomatis mengaitkan pesan error spesifik ke field yang bersangkutan sehingga dapat langsung ditampilkan kembali kepada pengguna di template.
   - **Urgensi Menambahkan `{% csrf_token %}`:**
     - Token CSRF (*Cross-Site Request Forgery*) adalah mekanisme keamanan wajib pada setiap form ber-method POST untuk melindungi aplikasi dari pemalsuan permintaan antar-situs.
     - Tanpa token ini, pihak penyerang dapat memanfaatkan sesi login pengguna yang sah melalui website berbahaya untuk mengeksekusi request ilegal (seperti membuat, memodifikasi, atau menghapus data) di aplikasi kita tanpa disadari oleh pengguna.
     - Tag `{% csrf_token %}` menghasilkan token unik per sesi pengguna. Ketika form dikirimkan, middleware Django (`CsrfViewMiddleware`) memvalidasi token tersebut. Jika token tidak ada atau tidak cocok, Django langsung menolak request dengan respon keamanan **403 Forbidden**.

2. **Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?**
   - **Ukuran Payload Lebih Ringkas (*Lightweight*):** XML menggunakan tag pembuka dan penutup yang redundan (contoh: `<title>...</title>`), sedangkan JSON menggunakan notasi berbasis kurung kurawal `{}` dan kurung siku `[]`. Hal ini membuat ukuran transmisi data JSON jauh lebih kecil, menghemat bandwidth, dan mempercepat waktu pengiriman melalui jaringan internet.
   - **Native di JavaScript dan Peramban Modern:** JSON (*JavaScript Object Notation*) adalah format data native pada JavaScript. Browser dan bahasa pemrograman modern dapat mem-parsing data JSON secara langsung menggunakan fungsi bawaan `JSON.parse()`, tanpa membutuhkan pustaka *XML DOM Parser* yang kompleks dan memakan banyak memori.
   - **Keterbacaan (*Human-Readable*):** Format key-value pada JSON jauh lebih mudah dibaca, dipahami, dan di-*debug* oleh developer dibandingkan struktur XML yang penuh dengan tag berulang.
   - **Standar Ekosistem Web Modern:** Arsitektur RESTful API, framework frontend modern (React, Vue, dsb.), dan aplikasi mobile telah mengadopsi JSON sebagai standar de facto dalam pertukaran data.
   *(Catatan: XML saat ini lebih banyak dipertahankan pada sistem warisan/legacy, integrasi enterprise perbankan berbasis protokol SOAP/WSDL, atau dokumen yang membutuhkan validasi skema ketat melalui XSD).*

3. **Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan?**
   - **Alur Kerja Pengembalian Data JSON:**
     1. **Request dari Client:** Client (browser atau API consumer) mengakses URL endpoint data delivery, misalnya `/projects/json/` atau `/projects/json/<id>/`.
     2. **Routing URL:** Django mencocokkan URL di `urls.py` dan memanggil fungsi view yang bersangkutan di `views.py` (`show_project_json` atau `show_project_json_by_id`).
     3. **Pengambilan Data dari Database:** Di dalam view, Django ORM mengeksekusi query database melalui `Project.objects.all()` atau `Project.objects.filter(pk=id)`. Hasil query ini berupa objek Python bertipe `QuerySet`.
     4. **Proses Serialisasi (*Serialization*):** Modul serializer Django dipanggil melalui `serializers.serialize('json', data)`. Modul ini mengiterasi objek model Python dan mengonversinya menjadi representasi teks berformat JSON.
     5. **Pembungkusan Respon HTTP:** Hasil teks JSON dibungkus dalam `HttpResponse(..., content_type='application/json')` agar client mengenali bahwa payload yang dikirimkan adalah data JSON murni.
     6. **Pengiriman Respon ke Client:** Respon dikirim kembali melalui protokol HTTP dan ditampilkan atau diolah oleh client.
   - **Alasan Perlunya Proses Serialization:**
     - Objek model Django (`QuerySet` maupun instance model) adalah objek internal Python yang berada di memori server. Objek ini memuat metode bawaan, koneksi database, dan metadata yang tidak bisa dikirimkan langsung melalui jaringan protokol HTTP.
     - Protokol HTTP hanya dapat mentransmisikan data berbasis teks (*plain text/string*) atau byte biner.
     - Proses *serialization* berfungsi sebagai penerjemah yang mengekstrak nilai field dari objek model Python dan mengubahnya menjadi format teks standar (JSON) yang terstruktur, netral, dan dapat dikonsumsi oleh bahasa pemrograman atau platform apapun di sisi client.

**Penggunaan AI:**
Dalam pengerjaan Tugas 3 ini, saya memanfaatkan AI Assistant (Google Gemini) secara transparan sebagai rekan diskusi (*thought partner*) untuk memperdalam pemahaman konsep Django. Diskusi difokuskan pada pemahaman cara kerja `ModelForm` dan validasinya, mekanisme keamanan CSRF, efisiensi data delivery JSON vs XML, alur serialisasi data, serta perancangan skenario unit test.

Seluruh penulisan kode (model, form, views, URL, template), perbaikan logika, hingga verifikasi 23 skenario unit test tetap saya pelajari, kerjakan, dan uji secara mandiri pada proyek `myportofolio`.

* **Tautan Bukti Percakapan AI (Gemini):** [Riwayat Diskusi PBP di Google Gemini](https://gemini.google.com/share/d/1-AZDerg8HxhMeNabr6V2gadfEUQsHv-e?usp=sharing)