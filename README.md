
# Socket Programming - Load Balancing

Repositori atau project ini bertujuan untuk mengimplementasikan **load balancing** menggunakan socket programming di Python, yang berfungsi untuk mendistribusikan beban kerja secara efisien antar beberapa server (workers) melalui mekanisme broker.

<img src="/images/diagram.jpg">

Diagram ini menunjukkan alur kerja sistem load balancing:

- Client mengirimkan permintaan ke Broker.
- Broker berfungsi sebagai Load Balancer, yang akan memilih Worker dengan beban terendah (Least Load) untuk memproses permintaan.
- Broker kemudian mendistribusikan permintaan ke salah satu dari Worker 1, Worker 2, atau Worker 3 berdasarkan beban kerja terkini.
- Worker yang dipilih menangani permintaan dari client untuk menjaga distribusi beban yang seimbang antar server.

<div align="center">
    <img src="/images/flowchart.jpg" style="max-height: 500px;">
</div>

Flowchart ini menunjukkan alur kerja sistem load balancing:

- Start: Sistem dimulai.
- Request: Klien mengirimkan permintaan ke broker.
- Broker menerima permintaan: Broker menerima permintaan dari klien.
- Broker memilih worker: Broker menggunakan algoritma Least Load untuk memilih worker dengan beban terendah.
- Kirim permintaan ke worker: Broker meneruskan permintaan ke worker terpilih.
- Worker memproses permintaan: Worker memproses permintaan dari klien.
- Worker mengirim respons ke broker: Worker mengirim hasil pemrosesan kembali ke broker.
- Broker mengirim respons ke klien: Broker meneruskan respons dari worker ke klien.
- End: Proses selesai.

## Deskripsi Repositori

Repositori ini terdiri dari beberapa direktori dan file yang berfungsi sebagai bagian dari sistem load balancing. Berikut adalah struktur repositori beserta deskripsi singkatnya:

### Struktur Repositori

- **codes/**: Berisi semua file kode utama yang diperlukan untuk menjalankan simulasi load balancing. 
- **documentation/**: Berisi dokumentasi lengkap, termasuk file markdown dan PDF yang menjelaskan simulasi dan penjelasan kode load balancing.

### Tujuan Project

Project ini bertujuan untuk memecahkan masalah distribusi beban kerja secara otomatis menggunakan **broker** sebagai load balancer untuk mendistribusikan permintaan antar beberapa **worker**. Sistem ini memungkinkan pemrosesan tugas yang lebih efisien dengan mengalokasikan tugas kepada worker yang memiliki beban kerja terendah.

## Direktori `codes`

Direktori `codes` berisi beberapa file yang menjadi komponen utama dari implementasi load balancing ini. Berikut adalah penjelasan dari setiap file:

1. **classes.py**: 
   - Berisi class utama yang digunakan dalam implementasi ini, yaitu `WorkerServer`, `BrokerServer`, dan `Client`. 
   - class ini berfungsi untuk menginisialisasi server worker, broker, dan client yang akan saling berkomunikasi dalam sistem load balancing.

2. **worker-1.ipynb**:
   - Notebook ini menjalankan instance dari `WorkerServer` pertama. 
   - Worker ini berfungsi untuk menerima permintaan dari broker dan memprosesnya sesuai jenis tugas yang diberikan.

3. **worker-2.ipynb**:
   - Notebook ini menjalankan instance dari `WorkerServer` kedua. 
   - Fungsinya sama dengan `worker-1`, bertindak sebagai worker kedua dalam sistem load balancing.

4. **worker-3.ipynb**:
   - Notebook ini menjalankan instance dari `WorkerServer` ketiga.
   - Sama seperti worker lainnya, worker ini siap menerima permintaan dari broker dan memproses tugas sesuai dengan jenis tugas yang diberikan.

5. **broker.ipynb**:
   - Notebook ini menjalankan instance dari `BrokerServer`. 
   - Broker bertindak sebagai load balancer yang menerima permintaan dari klien, memilih worker dengan beban kerja terendah, dan mengirimkan permintaan ke worker tersebut.

6. **client.ipynb**:
   - Notebook ini menjalankan instance dari `Client`.
   - Klien ini mengirimkan permintaan ke broker yang kemudian akan diarahkan ke worker sesuai dengan beban kerja saat ini.

## Direktori `documentation`

Direktori ini berisi file dokumentasi mengenai implementasi project ini. File-file tersebut:

- **Readme.md**: File markdown yang menjelaskan kode dari project load balancing ini.
- **simulasi_load_balancing.pdf**: File PDF yang berisi simulasi dan ilustrasi mengenai distribusi beban kerja antar worker melalui broker.

## Informasi Anggota

Project ini dikerjakan oleh:

- **Nama**: Rezky Arisanti Putri
- **NIM**: 24051905008

