# Dokumentasi Simulasi

Terdapat pada file pdf dalam folder ini simulasi_load_balancing.pdf

# Dokumentasi Penjelasan Kode

Dokumentasi ini menjelaskan secara detail setiap bagian dari kode yang mengimplementasikan load balancing sederhana dengan menggunakan socket programming di Python. Kelas ini terdiri dari tiga kelas utama: `WorkerServer`, `BrokerServer`, dan `Client`.

## 1. WorkerServer

Kelas `WorkerServer` berfungsi sebagai worker yang menangani permintaan dari broker. Setiap worker memiliki **host**, **port**, dan **ID unik**.

### Inisialisasi WorkerServer

```python
def __init__(self, host, port, worker_id):
    self.host = host
    self.port = port
    self.worker_id = worker_id
    self.load = 0  # Load saat ini untuk worker
    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server.bind((self.host, self.port))
    self.server.listen(5)
    print(f"Worker {self.worker_id} berjalan di {self.host}:{self.port}")
```
- **host, port**: Alamat dan port worker.
- **worker_id**: ID worker.
- **load**: Variabel untuk menyimpan beban kerja saat ini.
- **socket**: Mengatur server socket untuk worker.
- **bind** dan **listen**: Mengikat server ke host dan port yang ditentukan dan mulai mendengarkan koneksi.

### Fungsi `start`

```python
def start(self):
    while True:
        client_socket, addr = self.server.accept()
        print(f"Worker {self.worker_id} menerima koneksi dari {addr}")
        threading.Thread(target=self.handle_request, args=(client_socket,)).start()
```
- **accept**: Menerima koneksi dari broker.
- **Thread**: Setiap permintaan dijalankan dalam thread terpisah.

### Fungsi `handle_request`

```python
def handle_request(self, client_socket):
    request = client_socket.recv(1024).decode()
    if request == "Long":
        time.sleep(3)  # Simulasi waktu pemrosesan untuk Long
        self.load += 3
    elif request == "Short":
        time.sleep(1)  # Simulasi waktu pemrosesan untuk Short
        self.load += 1
    print(f"Worker {self.worker_id} selesai memproses {request}")
    client_socket.send(f"Worker {self.worker_id} selesai memproses {request}".encode())
    client_socket.close()
```
- **recv**: Menerima permintaan dari broker.
- **sleep**: Mensimulasikan waktu pemrosesan tugas (3 detik untuk Long, 1 detik untuk Short).
- **send**: Mengirim respons ke broker.

## 2. BrokerServer

Kelas `BrokerServer` berfungsi sebagai load balancer yang menerima permintaan dari klien dan memilih worker dengan beban terendah.

### Inisialisasi BrokerServer

```python
def __init__(self, host, port):
    self.host = host
    self.port = port
    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server.bind((self.host, self.port))
    self.server.listen(5)
    self.workers = [("localhost", 9001), ("localhost", 9002), ("localhost", 9003)]
    self.worker_loads = [0, 0, 0]  # Load tiap worker
    print(f"Broker berjalan di {self.host}:{self.port}")
```
- **host, port**: Menentukan alamat dan port broker.
- **workers**: Daftar worker yang tersedia.
- **worker_loads**: Menyimpan beban untuk setiap worker.

### Fungsi `start`

```python
def start(self):
    while True:
        client_socket, addr = self.server.accept()
        print(f"Broker menerima koneksi dari {addr}")
        threading.Thread(target=self.handle_client, args=(client_socket,)).start()
```
- **accept**: Menerima permintaan dari klien.
- **Thread**: Setiap permintaan klien dijalankan dalam thread terpisah.

### Fungsi `handle_client`

```python
def handle_client(self, client_socket):
    request = client_socket.recv(1024).decode()
    print(f"Broker menerima permintaan: {request}")
    selected_worker = self.select_worker(request)
    worker_host, worker_port = self.workers[selected_worker]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as worker_socket:
        worker_socket.connect((worker_host, worker_port))
        worker_socket.send(request.encode())
        response = worker_socket.recv(1024).decode()
    client_socket.send(response.encode())
    client_socket.close()
    self.update_worker_load(selected_worker, request)
```
- **select_worker**: Memilih worker dengan beban terendah.
- **connect, send, recv**: Mengirim permintaan ke worker yang dipilih dan menerima respons.
- **update_worker_load**: Memperbarui beban worker setelah pemrosesan.

### Fungsi `select_worker`

```python
def select_worker(self, request):
    if request == "Long":
        weights = [3, 3, 3]  # Bobot untuk Long
    else:
        weights = [1, 1, 1]  # Bobot untuk Short
    loads = [self.worker_loads[i] + weights[i] for i in range(len(self.workers))]
    min_load_worker = loads.index(min(loads))
    return min_load_worker
```
- **weights**: Menentukan bobot untuk setiap jenis permintaan.
- **loads**: Menghitung beban total setiap worker dan memilih yang terendah.

### Fungsi `update_worker_load`

```python
def update_worker_load(self, worker_index, request):
    if request == "Long":
        self.worker_loads[worker_index] += 3
    else:
        self.worker_loads[worker_index] += 1
    print(f"Update load worker: {self.worker_loads}")
```
- **worker_loads**: Memperbarui beban worker berdasarkan jenis permintaan.

## 3. Client

Kelas `Client` berfungsi sebagai klien yang mengirim permintaan ke broker.

### Inisialisasi Client

```python
def __init__(self, broker_host, broker_port):
    self.broker_host = broker_host
    self.broker_port = broker_port
```

### Fungsi `send_request`

```python
def send_request(self, request_type):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((self.broker_host, self.broker_port))
        sock.send(request_type.encode())
        response = sock.recv(1024).decode()
        print(f"Client menerima response: {response}")
```
- **connect, send, recv**: Menghubungkan ke broker, mengirim jenis permintaan, dan menerima hasil dari worker.
