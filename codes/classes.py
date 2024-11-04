import socket
import threading
import time

class WorkerServer:
    def __init__(self, host, port, worker_id):
        # Inisialisasi alamat, port, dan id server worker
        self.host = host
        self.port = port
        self.worker_id = worker_id
        self.load = 0  # Load saat ini untuk worker
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"Worker {self.worker_id} berjalan di {self.host}:{self.port}")

    def start(self):
        # Menunggu koneksi dari broker
        while True:
            client_socket, addr = self.server.accept()
            print(f"Worker {self.worker_id} menerima koneksi dari {addr}")
            threading.Thread(target=self.handle_request, args=(client_socket,)).start()

    def handle_request(self, client_socket):
        # Menerima pesan dari broker
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

class BrokerServer:
    def __init__(self, host, port):
        # Inisialisasi alamat dan port broker
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        # Daftar worker dengan alamat dan port yang sesuai
        self.workers = [("localhost", 9001), ("localhost", 9002), ("localhost", 9003)]
        self.worker_loads = [0, 0, 0]  # Load tiap worker
        print(f"Broker berjalan di {self.host}:{self.port}")

    def start(self):
        # Menerima koneksi dari client
        while True:
            client_socket, addr = self.server.accept()
            print(f"Broker menerima koneksi dari {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        # Menerima permintaan dari client
        request = client_socket.recv(1024).decode()
        print(f"Broker menerima permintaan: {request}")

        # Pilih worker dengan load paling rendah
        selected_worker = self.select_worker(request)

        # Kirim permintaan ke worker yang terpilih
        worker_host, worker_port = self.workers[selected_worker]
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as worker_socket:
            worker_socket.connect((worker_host, worker_port))
            worker_socket.send(request.encode())
            response = worker_socket.recv(1024).decode()

        # Kirim kembali hasil ke client
        client_socket.send(response.encode())
        client_socket.close()

        # Update load untuk worker terpilih
        self.update_worker_load(selected_worker, request)

    def select_worker(self, request):
        # Pilih worker berdasarkan metode load balancing
        if request == "Long":
            weights = [3, 3, 3]  # Bobot untuk Long
        else:
            weights = [1, 1, 1]  # Bobot untuk Short

        # Hitung worker dengan load terendah
        loads = [self.worker_loads[i] + weights[i] for i in range(len(self.workers))]
        min_load_worker = loads.index(min(loads))

        return min_load_worker

    def update_worker_load(self, worker_index, request):
        # Update load sesuai dengan jenis request
        if request == "Long":
            self.worker_loads[worker_index] += 3
        else:
            self.worker_loads[worker_index] += 1
        print(f"Update load worker: {self.worker_loads}")

class Client:
    def __init__(self, broker_host, broker_port):
        # Inisialisasi alamat dan port broker
        self.broker_host = broker_host
        self.broker_port = broker_port

    def send_request(self, request_type):
        # Membuat koneksi ke broker dan mengirim permintaan
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.broker_host, self.broker_port))
            sock.send(request_type.encode())
            response = sock.recv(1024).decode()
            print(f"Client menerima response: {response}")