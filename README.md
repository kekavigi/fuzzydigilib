# fuzzydigilib

Anda dapat mengunjungi situs ini di https://fuzzydigilib.herokuapp.com

Saya sering kesulitan mencari pustaka di [Digital Library ITB](www.digilib.itb.ac.id) yang relevan, secara cepat. Proyek ini ini saya buat untuk mempermudah proses tersebut, namun disesuaikan dengan opini pribadi apa yang saya anggap "penting". Data yang digunakan proyek ini adalah *cache* dari situs Digital Library ITB (selanjutnya saya sebut dengan Digilib). Dengan demikian, setiap perubahan pustaka yang terjadi disana -- baik penambahan, perbaikan, maupun penghapusan -- tidak langsung terlihat di situs proyek ini. Namun, ada beberapa data yang saya ubah maupun tidak diikutkan, karena saya anggap kurang relevan. Contohnya mengetahui sebuah pustaka berasal dari fakultas <code>FMIPA</code> ketika pustaka tersebut diterbitkan oleh <code>FMIPA - Matematika</code>, adanya teks <code>TIDAK ADA ABSTRAK</code> pada data abstrak, mapun berapa banyak <code>File</code> dimiliki pustaka, yang jumlahnya dapat berubah tergantung pada akses yang diberikan.

## Tahapan pengerjaan

### Pengumpulan data
Katalog info pustaka yang digunakan dalam proyek ini adalah milik Digilib yang dapat diakses secara publik. Terdapat dua cara untuk mendapatkan data ini dari Digilib. Pertama menggunakan akses [OAI-PMH](https://www.openarchives.org/pmh/) [GetRecords](https://digilib.itb.ac.id/oai.php?verb=GetRecord&identifier=54322&metadataPrefix=oai_dc) (atau [ListRecords](https://digilib.itb.ac.id/oai.php?verb=ListRecords&metadataPrefix=oai_dc)) yang disediakan oleh Digilib. Walaupun tersedia dalam format XML yang mudah diproses, data ini tidak memiliki data kontributor (data dosen pembimbing dan semacamnya). Hal ini yang membuat saya melakukan cara kedua, crawling situs Digilib. Kode Python yang saya gunakan dapat dilihat pada [crawler_infobox.py](resource/crawler_infobox.py) dan [crawler_file.py](resource/crawler_file.py).

### Perapian data
Setelah data dikumpulkan, saya melakukan perapian sebelum menyimpannya dalam bentuk database. Detail mengenai proses yang saya lakukan dapat dilihat di [cleaning.ipynb](resource/cleaning.ipynb)

### Desain database dan situs
Dalam membuat database yang mampu melakukan pencarian teks dengan baik dan cepat, saya menyukai PostgreSQL. Namun dengan ukuran berat hampir mencapai 150MB dan 58K baris, sulit untuk mencari penyedia layanan PostgreSQL gratis. Heroku contohnya, hanya memberikan layanan gratis untuk data tanpa batasan berat, asal kurang dari 10K baris. Saya memutuskan untuk menggunakan MongoDB (saat ini versi 4.4.8) yang memberikan layanan gratis tanpa batasan baris, asal kurang dari 512MB. Fasilitas pencarian teks di MongoDB saat ini tidak sebagus PostgreSQL *, namun untuk kasus sederhana sudah memberikan hasil yang kurang-lebih sama.

Sedangkan untuk situs, saya memilih Flask untuk membuatnya. Desain tampilan disusun sehingga semua info mengenai pustaka dapat dilihat secara cepat dan mudah -- setidaknya di layar berukuran besar, dan setidaknya bagi saya. Heroku dipilih sebagai hos karena sifatnya yang gratis, dan saya tidak berkeberatan dengan batasan yang terjadi.

## Lisensi
Saya menggunakan [MIT License](LICENSE.txt)


## Catatan kaki
* Misalkan anda ingin mencari pustaka skripsi mengenai machine learning (atau pemelajaran mesin dalam bahasa Indonesia) namun tidak dibimbing oleh Nama Dosen. Di PostgreSQL (yang mirip dengan pencarian lanjut di Google), anda dapat menuliskan kueri
  `skripsi ("machine learning"|"pemelajaran mesin") -"Nama Dosen"`
  Kemampuan ini belum dapat dilakukan di MongoDB.
