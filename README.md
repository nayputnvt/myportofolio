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
Dalam menyelesaikan Tugas 3 ini, saya memanfaatkan AI Assistant (Google Gemini) secara transparan sebagai rekan diskusi (*learning companion*) untuk memperdalam pemahaman konsep Django.

Diskusi difokuskan pada pemahaman cara kerja `ModelForm` dan validasinya, mekanisme keamanan CSRF, efisiensi data delivery JSON vs XML, alur serialisasi data, serta perancangan skenario unit test.
Seluruh penulisan kode (model, form, views, URL, template), perbaikan logika, hingga verifikasi 23 skenario unit test tetap saya pelajari, kerjakan, dan uji secara mandiri pada proyek `myportofolio`.

* **Tautan Bukti Percakapan AI (Gemini):** [Riwayat Diskusi PBP di Google Gemini](https://gemini.google.com/share/d/1x9N04SH-viI2-Nxy0Yd7ljqCvqXOKy95?usp=sharing)


### Tugas 4

*(Catatan: Mengikuti panduan resmi pada spesifikasi Tugas 4, pertanyaan reflektif untuk pekan ini ditiadakan/dihilangkan).*

1. **Implementasi Autentikasi, Sesi, dan Cookie:**
   - Saya mengimplementasikan alur autentikasi bawaan Django melalui fungsi `register`, `login_user`, dan `logout_user`.
   - Saat pengguna berhasil login, view memasang cookie `last_login` yang menyimpan informasi tanggal dan jam login. Data ini ditampilkan di halaman profil utama (`index.html`). Saat pengguna melakukan logout, sesi login dihapus dan cookie `last_login` langsung dibersihkan dari browser.

2. **Penerapan Hak Akses & 4 Peran Pengguna (Authorization):**
   - **Guest (Belum Login):** Pengunjung hanya bisa membaca daftar pengalaman dan proyek. Jika mencoba melakukan penambahan, pengubahan, penghapusan, atau pemberian star, pengunjung akan otomatis dialihkan ke halaman login.
   - **Regular User (Pengguna Biasa):** Pengguna yang sudah login dapat membaca data serta memberikan atau membatalkan *star* (`toggle_star`). Pengguna biasa tidak memiliki akses untuk membuat, mengedit, atau menghapus data (diberikan respon `403 PermissionDenied` jika mencoba mengaksesnya).
   - **Editor:** Saya membuat grup `Editor` melalui Django Admin. Pengguna yang tergabung dalam grup ini memiliki hak akses pengguna biasa ditambah izin untuk **mengubah/mengedit data** (`edit_project` dan `edit_experience`). Namun, Editor tetap tidak diizinkan membuat data baru atau menghapus data.
   - **Superuser (Pemilik Portofolio):** Memiliki hak akses penuh untuk membuat, mengedit, menghapus, serta memberikan star pada seluruh data portofolio.
   - Di sisi template (`projects.html` dan `experience.html`), tombol aksi (`Add`, `Edit`, `Delete`) ditampilkan dan disembunyikan secara kondisional menggunakan tag template Django sesuai dengan peran pengguna yang sedang aktif.

3. **Fitur Star pada Experience dan Project:**
   - Saya menambahkan relasi `starred_by = models.ManyToManyField(User, ...)` pada model `Experience` dan `Project`.
   - Fitur pemberian star ditangani oleh view `toggle_experience_star` dan `toggle_star` menggunakan method `POST` dan dilindungi dengan `{% csrf_token %}` untuk keamanan dari serangan CSRF.
   - Endpoint JSON juga disesuaikan dengan menambahkan parameter `use_natural_foreign_keys=True` pada serializer agar data relasi many-to-many dapat ditampilkan secara aman dan terstruktur.

**Penggunaan AI:**
Dalam menyelesaikan Tugas 4 ini, saya memanfaatkan AI Assistant (Google Gemini) secara transparan sebagai rekan diskusi (*learning companion*) untuk memperdalam konsep autentikasi, pengelolaan sesi, mekanisme otorisasi berbasis grup di Django, serta perancangan skenario unit test.

Diskusi difokuskan pada pemahaman perbedaan session dan cookie, cara kerja `PermissionDenied` untuk menghasilkan respon HTTP 403, penanganan relasi `ManyToManyField` pada serialisasi JSON, dan pembuatan skenario pengujian 4 peran di `tests.py`. Seluruh penulisan kode, penyesuaian logika peran, perapian antarmuka, hingga verifikasi pengujian 33 unit test saya pelajari, terapkan, dan uji secara mandiri pada proyek `myportofolio`.

* **Tautan Bukti Percakapan AI (Gemini):** [Riwayat Diskusi Konsep Tugas 4 di Google Gemini](https://share.gemini.google/BLbvmPPDAYfR)


### Tugas 5

1. **Jelaskan apa itu debouncing dan mengapa teknik ini penting diterapkan pada fitur pencarian yang menggunakan AJAX!**
   - **Pengertian Debouncing:** Debouncing adalah teknik pemrograman JavaScript untuk menunda eksekusi suatu fungsi sampai beberapa saat setelah pengguna berhenti melakukan aksi (misalnya berhenti mengetik pada kolom pencarian). Setiap kali pengguna menekan tombol keyboard baru, timer penundaan di-reset kembali dari awal, sehingga fungsi pencarian baru akan benar-benar dijalankan ketika pengguna sudah diam atau selesai mengetik selama durasi jeda tertentu (pada tugas ini diatur 300 ms).
   - **Alasan Penting Diterapkan pada Pencarian AJAX:**
     - **Mengurangi Beban Request ke Server:** Tanpa debouncing, setiap karakter yang diketik atau dihapus oleh pengguna akan langsung mengirim satu request HTTP via AJAX ke server backend. Jika pengguna mengetik 10 karakter dengan cepat, server akan dihujani 10 request beruntun. Dengan debouncing, request hanya dikirim 1 kali setelah pengguna selesai mengetik kata kuncinya.
     - **Mencegah Masalah Race Condition:** Request jaringan membutuhkan waktu respon yang bervariasi. Jika request dikirim terus-menerus tanpa jeda, respon dari pencarian yang lama bisa saja datang lebih lambat daripada respon pencarian yang baru, sehingga tampilan hasil pencarian bisa keliru atau tidak sesuai dengan kata kunci terakhir yang diketik pengguna.
     - **Meningkatkan Performa dan Pengalaman Pengguna (UX):** Debouncing membuat aplikasi terasa lebih responsif, hemat bandwidth jaringan, dan antarmuka tidak mengalami kedipan (*flickering*) karena tidak me-reload data secara berlebihan setiap milidetik.

2. **Jelaskan fungsi dari penggunaan `await` ketika kita menggunakan `fetch()`! Apa yang akan terjadi jika kita tidak menggunakan `await`?**
   - **Fungsi `await` pada `fetch()`:**
     - `fetch()` bekerja secara asinkronus (*asynchronous*) dan mengembalikan sebuah objek `Promise` yang mewakili proses pertukaran data jaringan di latar belakang.
     - Kata kunci `await` berfungsi untuk memberhentikan sementara alur eksekusi kode di dalam fungsi `async` sampai `Promise` dari `fetch()` selesai diselesaikan (*resolved*) dan mengembalikan objek `Response` yang sebenarnya, atau sampai proses `response.json()` selesai mengurai (*parsing*) payload menjadi data JavaScript.
   - **Apa yang terjadi jika tidak menggunakan `await`:**
     - Jika kita tidak menggunakan `await` (dan tidak menggunakan rangkaian rantai `.then()`), JavaScript akan langsung mengeksekusi baris kode berikutnya tanpa menunggu respon data dari server selesai tiba.
     - Variabel yang menampung hasil pemanggilan `fetch()` akan berisi objek `Promise {<pending>}` dan bukan objek `Response` atau data JSON aslinya.
     - Ketika kode di baris selanjutnya mencoba membaca atau mengiterasi data tersebut (misalnya memanggil `.map()` atau mengakses properti objek), program akan menghasilkan galat *runtime* (seperti `TypeError: Cannot read properties of undefined` atau error karena mencoba memproses `Promise` yang belum selesai).

3. **Jelaskan apa itu serangan XSS (Cross-Site Scripting) dan mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini daripada data yang ditampilkan langsung melalui template Django!**
   - **Pengertian XSS (Cross-Site Scripting):**
     - XSS adalah jenis kerentanan keamanan web di mana pihak penyerang berhasil menyisipkan skrip berbahaya (biasanya JavaScript) ke dalam konten web yang dilihat oleh pengguna lain. Saat halaman dimuat di peramban korban, skrip berbahaya tersebut otomatis dieksekusi, sehingga penyerang dapat mencuri cookie sesi login, membajak akun pengguna, atau memanipulasi tampilan dan fungsi halaman secara ilegal.
   - **Alasan Data AJAX/JavaScript Lebih Rentan Dibandingkan Template Django:**
     - **Auto-Escaping pada Template Django:** Mesin template Django (DTL) secara bawaan (*default*) menerapkan mekanisme *automatic HTML escaping* pada setiap variabel yang dirender (seperti `{{ experience.title }}`). Karakter khusus seperti `<`, `>`, `&`, `"`, dan `'` otomatis diubah menjadi entitas HTML aman (`&lt;`, `&gt;`, dsb.), sehingga kode skrip yang diinput tidak akan dieksekusi sebagai program oleh browser.
     - **DOM Manipulation Manual di JavaScript:** Saat data diambil via AJAX dalam format JSON, data tersebut diolah dan dimasukkan ke dalam DOM secara manual menggunakan JavaScript. Jika developer menggunakan metode yang tidak aman seperti `innerHTML` atau *template literals* `${data.title}` tanpa melakukan sanitasi manual (atau tanpa memanfaatkan properti aman seperti `textContent`), tag `<script>` atau atribut berbahaya (misalnya `<img src=x onerror=alert(1)>`) yang tersimpan di database akan langsung dirender sebagai elemen HTML hidup dan dieksekusi oleh peramban pengguna.
     - **Solusi Pencegahan:** Pada proyek ini, pencegahan XSS diterapkan secara berlapis, yaitu sanitasi di sisi server menggunakan fungsi `strip_tags` pada form Django (`forms.py`) sebelum data tersimpan di database, serta fungsi pembersih `escapeHtml()` di sisi client JavaScript sebelum elemen kartu pengalaman dimasukkan ke dalam DOM antarmuka.

**Penggunaan AI:**
Dalam menyelesaikan Tugas 5 ini, saya memanfaatkan AI Assistant (Google Gemini) secara transparan sebagai rekan diskusi (*learning companion*) untuk mempelajari konsep interaktivitas JavaScript dan AJAX pada Django.

Diskusi difokuskan pada pemahaman mekanisme pengambilan data asinkronus dengan `fetch()` dan `async/await`, penerapan teknik debouncing beserta pembatalan request menggunakan `AbortController`, implementasi modal popover dan AJAX POST untuk penambahan data tanpa reload, serta proteksi keamanan dari serangan XSS (*Cross-Site Scripting*) baik di sisi backend (`strip_tags`) maupun frontend (`escapeHtml`). Seluruh penulisan kode, penyesuaian fungsi view, penataan antarmuka modal dan toast, serta pembuatan skenario pengujian unit test tetap saya pelajari, terapkan, dan uji secara mandiri pada proyek `myportofolio`.

* **Tautan Bukti Percakapan AI (Gemini):** [Riwayat Diskusi Konsep Tugas 5 di Google Gemini](https://gemini.google.com)


### Tugas 6

1. **Jelaskan apa yang dimaksud dengan REST dan mengapa mengembalikan JSON saja belum cukup untuk menyebut sebuah API sebagai RESTful!**
   - **Pengertian REST (*Representational State Transfer*):**
     REST adalah sebuah gaya arsitektur (*architectural style*) perangkat lunak yang diperkenalkan oleh Roy Fielding pada disertasinya tahun 2000 untuk mendesain sistem terdistribusi, terutama pada Web API. REST berpusat pada konsep *resource* (sumber daya) yang diidentifikasi secara unik menggunakan URI/URL. Klien berinteraksi dengan server dengan cara mempertukarkan representasi dari status sumber daya tersebut (biasanya dalam format teks terstruktur seperti JSON, XML, atau HTML) menggunakan protokol komunikasi standar (HTTP).
   - **Mengapa Mengembalikan JSON Saja Belum Cukup Disebut RESTful:**
     Hanya karena sebuah endpoint menghasilkan respon berformat JSON (seperti fungsi view `get_experiences_json` pada tugas sebelumnya), endpoint tersebut belum otomatis memenuhi kriteria RESTful. JSON hanyalah format serialisasi payload data (*data format*), sedangkan RESTful menuntut kepatuhan terhadap serangkaian prinsip arsitektural:
     - **Pemanfaatan HTTP Method Sesuai Semantik (*Uniform Interface*):** API RESTful menggunakan kata kerja HTTP standar sesuai fungsinya: `GET` untuk membaca, `POST` untuk membuat data baru, `PUT` untuk memperbarui data secara menyeluruh, `PATCH` untuk pembaruan parsial, dan `DELETE` untuk menghapus. API yang sekadar mengembalikan JSON tetapi semua operasinya menggunakan method `GET` atau `POST` dengan URL aksi (seperti `/api/add_item/` atau `/api/delete_item/`) merupakan pola RPC (*Remote Procedure Call*), bukan RESTful.
     - **Karakteristik *Stateless*:** Setiap request yang dikirimkan klien harus membawa seluruh konteks dan kredensial yang dibutuhkan oleh server untuk memprosesnya secara mandiri, tanpa server bergantung pada riwayat percakapan request sebelumnya.
     - **Penggunaan Kode Status HTTP Standar:** API harus mengembalikan status code yang mencerminkan hasil eksekusi operasi secara akurat (`200 OK`, `201 Created`, `204 No Content`, `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, atau `405 Method Not Allowed`).
     - **Desain URI Berorientasi Objek (*Resource-Oriented*):** Endpoint disusun menggunakan kata benda jamak untuk merepresentasikan koleksi dan entitas tunggal (misalnya `/api/v1/experiences/` untuk daftar dan `/api/v1/experiences/<uuid>/` untuk satu data spesifik).

2. **Jelaskan pula perbedaan PUT dan PATCH beserta contoh kapan masing-masing sebaiknya digunakan!**
   - **Perbedaan Konseptual:**
     - `PUT` (*Complete Replacement / Idempotent*): Digunakan untuk menggantikan representasi *resource* yang ada secara menyeluruh dengan data baru yang dikirim oleh klien. Klien wajib menyertakan seluruh field yang dibutuhkan. Apabila ada field yang tidak dikirim, server dapat mengosongkan nilai field tersebut atau menolak request dengan galat validasi jika field tersebut bersifat wajib (*required*).
     - `PATCH` (*Partial Modification*): Digunakan untuk memodifikasi sebagian atribut atau field tertentu dari sebuah *resource* tanpa memengaruhi atribut lain yang tidak disertakan dalam payload.
   - **Contoh Penggunaan pada Model `Experience`:**
     - **Kapan Menggunakan PUT:** Ketika seorang pengguna membuka form pengeditan penuh dan mengirim ulang seluruh data pengalaman (misalnya mencakup `title`, `description`, `category`, `thumbnail`, dan `ended_at`). Klien mengirim seluruh atribut secara komprehensif untuk menimpa rekaman data yang lama.
     - **Kapan Menggunakan PATCH:** Ketika kita hanya ingin memperbarui atribut spesifik tanpa membebani jaringan dengan mengirim seluruh data lama. Sebagai contoh, peran Editor hanya ingin memperbaiki kesalahan ketik pada judul posisi (`{"title": "Senior Software Engineer Intern"}`) atau menandai tanggal berakhirnya kegiatan (`{"ended_at": "2026-11-01T00:00:00Z"}`). Dengan `PATCH`, atribut lain seperti deskripsi, foto, dan daftar pengguna yang memberi bintang (*starred_by*) tetap utuh terjaga di database.

3. **Jelaskan peran serializer pada Django REST Framework! Apa keuntungannya dibandingkan merakit dictionary secara manual dengan JsonResponse seperti pada Tutorial sebelumnya?**
   - **Peran Serializer:**
     Serializer dalam Django REST Framework berfungsi sebagai jembatan penerjemah dua arah (*two-way data translator*) antara tipe data kompleks internal Python/Django (seperti objek model dan QuerySet) dengan format data jaringan yang terstruktur (seperti JSON):
     - **Serialisasi (*Read Pipeline*):** Mengubah instance model database menjadi dictionary Python sederhana yang kemudian dapat dirender menjadi string JSON untuk dikirim ke klien.
     - **Deserialisasi & Validasi (*Write Pipeline*):** Menerima payload JSON dari request klien, memvalidasi tipe data dan batasan logika, membersihkan input berbahaya, lalu mengonversinya menjadi objek model yang siap disimpan ke database (`.is_valid()` dan `.save()`).
   - **Keuntungan Dibandingkan Merakit Dictionary Manual (`JsonResponse`):**
     - **Validasi Terpusat dan Deklaratif:** Serializer otomatis memeriksa aturan basis data (panjang karakter, format URL, pilihan kategori yang valid) dan mendukung fungsi validasi kustom (`validate_<field>`), sehingga kita tidak perlu menulis rangkaian logika `if-else` manual yang panjang di dalam view.
     - **Respon Galat yang Terstandarisasi:** Jika input salah, serializer otomatis menghasilkan pesan error terstruktur per field (seperti `{"title": ["This field may not be blank."]}`), memudahkan frontend untuk menampilkan pesan error yang tepat kepada pengguna.
     - **Mendukung Atribut Terhitung (*Computed Fields*):** Kita dapat menyematkan field dinamis yang dihitung saat runtime melalui `SerializerMethodField` (seperti `star_count`, status `is_starred` sesuai konteks pengguna yang sedang aktif, dan relasi Many-to-Many `starred_by_names`) tanpa perlu memodifikasi skema fisik database.
     - **Prinsip DRY (*Don't Repeat Yourself*):** Menghindari duplikasi kode perakitan dictionary di banyak view yang berbeda, sehingga pemeliharaan (*maintenance*) kode jauh lebih rapi dan minim risiko galat ketik (*typo*).

4. **Jelaskan perbedaan autentikasi dan otorisasi pada Django REST Framework!**
   - **Autentikasi (*Authentication* - "Siapa Anda?"):**
     Proses untuk memvalidasi dan mengenali identitas pengguna yang melakukan request ke API. Pada DRF, proses ini ditangani oleh *authentication classes* (seperti `SessionAuthentication` yang membaca cookie sesi). Mekanisme ini memeriksa kredensial klien dan mengisi atribut `request.user` dengan objek akun yang sesuai (atau `AnonymousUser` apabila pengguna belum masuk log).
   - **Otorisasi (*Authorization* / *Permissions* - "Apa hak Anda?"):**
     Proses untuk menentukan apakah pengguna yang identitasnya sudah dikenali (atau tamu anonim) memiliki izin untuk mengeksekusi tindakan atau mengakses endpoint tertentu. Hal ini diatur oleh *permission classes* (seperti `IsPortfolioOwnerOrReadOnly` dan `IsPortfolioOwnerOrEditorOrReadOnly`). Permission class mengevaluasi method HTTP yang digunakan dan peran akun pengguna, lalu memutuskan apakah request diizinkan (`True`) atau ditolak dengan respon HTTP `403 Forbidden` (atau `401 Unauthorized` jika pengguna belum login).
   - **Hubungan Keduanya:** Autentikasi selalu dieksekusi terlebih dahulu agar server mengetahui siapa klien yang sedang berinteraksi. Setelah identitas terpasang pada `request.user`, barulah lapisan otorisasi memutuskan apakah aksi tersebut boleh dilanjutkan.

5. **Mengapa hak akses harus diperiksa dengan permission class di server, bukan hanya dengan menyembunyikan tombol di template?**
   - **Kerapuhan Pemeriksaan di Sisi Klien (*Client-Side Is Not Secure*):**
     Menyembunyikan tombol aksi (seperti tombol *Hapus* atau *Edit*) di template HTML hanyalah sarana kenyamanan tampilan antarmuka (*UI/UX helper*), bukan mekanisme pengamanan. Segala hal yang berjalan di peramban klien berada di luar kendali server:
     - Pengguna dapat dengan mudah memunculkan kembali elemen yang disembunyikan menggunakan fitur *Inspect Element* (DevTools) peramban.
     - Pengguna dapat langsung menembakkan request HTTP berbahaya (misalnya request `DELETE /api/v1/experiences/<uuid>/`) secara mandiri menggunakan peralatan seperti Postman, cURL, ekstensi peramban, atau perintah `fetch()` dari konsol JavaScript tanpa harus menyentuh tombol di halaman web.
   - **Pertahanan Mutlak di Sisi Server (*Server-Side Authorization*):**
     Pemeriksaan menggunakan *permission class* di server bertindak sebagai benteng pertahanan mutlak (*gatekeeper*) yang tidak dapat dimanipulasi oleh klien. Server akan memvalidasi setiap paket request yang masuk; apabila seorang pengguna biasa atau Editor mencoba mengirim request penghapusan, server akan langsung menggugurkannya dengan status `403 Forbidden`, sehingga integritas data di database tetap aman.

6. **Jelaskan mengapa permintaan yang mengubah data tetap memerlukan token CSRF ketika API memakai SessionAuthentication!**
   - **Karakteristik Bawaan Peramban:**
     Ketika API memanfaatkan `SessionAuthentication`, peramban web secara otomatis menyertakan cookie sesi (`sessionid`) pada setiap request yang dikirimkan ke domain aplikasi kita, terlepas dari apakah request tersebut berasal dari website kita sendiri atau dipicu oleh halaman web lain.
   - **Ancaman Serangan CSRF (*Cross-Site Request Forgery*):**
     Apabila pengguna yang sedang aktif login di website portofolio kita membuka tab lain yang berisi situs web berbahaya, situs penyerang tersebut dapat menjalankan skrip tersembunyi yang mengirim request mutasi (seperti `POST /api/v1/experiences/` atau `DELETE /api/v1/experiences/<id>/`) ke server kita. Karena peramban otomatis menyertakan cookie `sessionid` milik pengguna, server Django akan mengira request tersebut datang dari aksi sah pengguna jika tidak ada perlindungan tambahan.
   - **Token CSRF Sebagai Bukti Keabsahan (*Synchronizer Token*):**
     Token CSRF adalah nilai unik, acak, dan terlindungi yang disimpan di cookie `csrftoken`. Token ini tidak dikirimkan secara otomatis oleh peramban, melainkan harus dibaca oleh skrip frontend aplikasi kita dan disematkan secara manual ke dalam header request (`X-CSRFToken`). Karena aturan keamanan peramban *Same-Origin Policy* (SOP) melarang situs penyerang membaca cookie domain lain, request palsu dari pihak penyerang tidak akan memiliki header `X-CSRFToken` yang valid dan akan seketika digugurkan oleh server Django dengan status `403 Forbidden`.

7. **Mengapa test yang memakai force_authenticate tidak cukup untuk membuktikan bahwa perlindungan CSRF berjalan?**
   - **Mekanisme Kerja `force_authenticate`:**
     Method `force_authenticate(user=...)` pada `APIClient` DRF bekerja dengan cara langsung menyuntikkan (*mocking*) objek pengguna ke dalam atribut `request.user` pada tingkat objek Python sebelum view dipanggil.
   - **Melewati Pipeline Middleware Django:**
     Proses tersebut sengaja **melewati (*bypasses*) seluruh alur otentikasi sesi yang sesungguhnya serta middleware keamanan Django**, termasuk `CsrfViewMiddleware`. Oleh karena itu, pengujian yang memanfaatkan `force_authenticate` tidak menguji apakah request klien membawa cookie sesi yang valid dan tidak memeriksa keberadaan token `X-CSRFToken`.
   - **Risiko *False Positive*:**
     Apabila kita hanya mengandalkan `force_authenticate`, celah keamanan seperti hilangnya pemeriksaan CSRF pada konfigurasi view tidak akan terdeteksi oleh pengujian karena request selalu dianggap sah.
   - **Praktik Pengujian yang Benar:**
     Untuk membuktikan bahwa mekanisme perlindungan CSRF benar-benar bekerja di kondisi produksi, kita wajib membuat skenario pengujian menggunakan `APIClient(enforce_csrf_checks=True)` dan mengautentikasi pengguna melalui alur login nyata (`client.login()`). Melalui metode ini, kita dapat membuktikan secara empiris bahwa request mutasi tanpa token CSRF akan ditolak (`403 Forbidden`), sedangkan request yang menyertakan header token `HTTP_X_CSRFTOKEN` yang sah berhasil dieksekusi (`201 Created` / `200 OK`).

**Penggunaan AI:**
Dalam menyelesaikan Tugas 6 ini, saya memanfaatkan AI Assistant (Google Gemini) secara transparan sebagai rekan belajar (*learning companion*) untuk mendiskusikan implementasi arsitektur Django REST Framework (DRF) pada model portofolio pribadi (`Experience`).

Diskusi berfokus pada pemahaman prinsip RESTful API, perbedaan semantik method `PUT` dan `PATCH`, peran serializer dalam serialisasi dan validasi sanitasi input (`strip_tags`), perancangan otorisasi berbasis peran (RBAC) menggunakan custom permission class `IsPortfolioOwnerOrEditorOrReadOnly`, integrasi komunikasi AJAX frontend dengan header token `X-CSRFToken`, serta penyusunan skenario pengujian menyeluruh menggunakan `APITestCase` dan `APIClient(enforce_csrf_checks=True)`. Seluruh penulisan kode, penyesuaian fungsi API view, penataan interaksi JavaScript di antarmuka, hingga verifikasi keberhasilan 74 unit test saya pelajari, terapkan, dan uji secara mandiri pada proyek `myportofolio`.

* **Tautan Bukti Percakapan AI (Gemini):** [Riwayat Diskusi Konsep Tugas 6 di Google Gemini](https://share.gemini.google/330VeksdbDXS)