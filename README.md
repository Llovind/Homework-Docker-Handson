# Praktikum Docker Dasar

Repository ini berisi implementasi tugas praktikum Docker Dasar yang mencakup pengujian **container lifecycle** menggunakan `ubuntu:22.04` serta pembuatan dan deployment aplikasi web sederhana menggunakan Dockerfile.

## Identitas

| Informasi | Detail |
|---|---|
| Nama | Lovind |
| NIM | 101012330245 |
| Mata Kuliah | Praktikum Docker |
| Repository | Homework-Docker-Handson |

---

# Bagian 1 — Pengujian Lifecycle Kontainer Dasar

Tahap pertama dilakukan untuk memahami lifecycle dasar sebuah Docker container, mulai dari menjalankan container, berinteraksi dengan container, melihat informasi sistem operasi, hingga menghapus container.

## 1. Menjalankan Container Ubuntu

Container berbasis image `ubuntu:22.04` dijalankan secara interaktif dengan nama:

```bash
docker run -it --name tes-ubuntu-101012330245 ubuntu:22.04 bash
```

Setelah berhasil dijalankan, terminal akan masuk ke dalam container Ubuntu.

## 2. Mengecek Informasi Versi OS

Di dalam container, digunakan perintah:

```bash
cat /etc/os-release
```

Perintah tersebut digunakan untuk menampilkan informasi sistem operasi Ubuntu yang sedang berjalan di dalam container.

## 3. Keluar dari Container

Setelah selesai melakukan pengujian:

```bash
exit
```

## 4. Menghapus Container

Container kemudian dihapus menggunakan:

```bash
docker rm tes-ubuntu-101012330245
```

Tahapan tersebut menunjukkan lifecycle dasar container:

```text
docker run
    ↓
Container Created & Running
    ↓
Interactive Shell
    ↓
cat /etc/os-release
    ↓
exit
    ↓
docker rm
    ↓
Container Removed
```

---

# Bagian 2 — Building Image Aplikasi Web dengan Dockerfile

Pada tahap kedua dibuat aplikasi web sederhana menggunakan Python HTTP Server. Aplikasi akan berjalan pada port `8000` di dalam container dan diakses melalui port `8080` pada host.

## Struktur Project

Struktur project utama adalah:

```text
tugas-docker-101012330245/
│
├── app.py
├── Dockerfile
└── docker-compose.yml
```

---

## 1. Aplikasi Web — `app.py`

Aplikasi menggunakan module bawaan Python `http.server` untuk membuat HTTP server sederhana.

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        nim = os.getenv('STUDENT_NIM', '12345678')

        message = f"""
        <h1>Praktikum Docker Dasar Berhasil!</h1>
        <p>Dikembangkan oleh NIM: {nim}</p>
        """

        self.wfile.write(message.encode())

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), SimpleHandler)
    print("Server berjalan pada port 8000...")
    server.serve_forever()
```

Aplikasi membaca NIM dari environment variable `STUDENT_NIM` yang diberikan oleh Dockerfile.

---

# 2. Dockerfile

Dockerfile digunakan untuk membuat custom Docker image berdasarkan `python:3.11-slim`.

```dockerfile
FROM python:3.11-slim

WORKDIR /app

ENV STUDENT_NIM=101012330245

COPY app.py /app/app.py

EXPOSE 8000

CMD ["python", "/app/app.py"]
```

### Penjelasan

| Instruction | Fungsi |
|---|---|
| `FROM python:3.11-slim` | Menggunakan Python 3.11 sebagai base image |
| `WORKDIR /app` | Menentukan working directory di dalam container |
| `ENV STUDENT_NIM=101012330245` | Menentukan NIM sebagai environment variable |
| `COPY app.py /app/app.py` | Menyalin aplikasi Python ke dalam image |
| `EXPOSE 8000` | Mendokumentasikan port aplikasi |
| `CMD` | Menjalankan aplikasi Python ketika container dimulai |

---

# 3. Build Docker Image

Docker image dibuat menggunakan command berikut:

```bash
docker build -t web-tugas-101012330245:1.0 .
```

> Tanda `.` di akhir command menunjukkan bahwa current directory digunakan sebagai **build context**.

Setelah proses build selesai, image dapat diperiksa dengan:

```bash
docker images
```

Image yang dibuat:

```text
web-tugas-101012330245:1.0
```

---

# 4. Menjalankan Container

Container dijalankan dalam mode detached menggunakan:

```bash
docker run -d -p 8080:8000 --name web-container-101012330245 web-tugas-101012330245:1.0
```

Mapping port yang digunakan adalah:

```text
Host                    Container
8080       ────────────> 8000
```

Sehingga aplikasi yang berjalan pada port `8000` di dalam container dapat diakses melalui port `8080` pada host.

Status container dapat diperiksa dengan:

```bash
docker ps
```

---

# 5. Pengujian Aplikasi

Aplikasi kemudian diuji menggunakan `curl`:

```bash
curl http://localhost:8080
```

Jika aplikasi berhasil berjalan, response yang diberikan akan berisi:

```html
<h1>Praktikum Docker Dasar Berhasil!</h1>
<p>Dikembangkan oleh NIM: 101012330245</p>
```

---

# 6. Docker Compose

Repository juga menyediakan `docker-compose.yml` sebagai bagian dari deliverables praktikum.

Docker Compose digunakan untuk mendefinisikan dan menjalankan service secara terstruktur.

Contoh struktur service:

```yaml
services:
  web:
    build: .
    container_name: web-container-101012330245
    ports:
      - "8080:8000"
    environment:
      - STUDENT_NIM=101012330245
```

Untuk menjalankan service:

```bash
docker compose up -d
```

Untuk melihat status service:

```bash
docker compose ps
```

Untuk menghentikan service:

```bash
docker compose down
```

---

# 7. Screenshot / Evidence

## Screenshot 1 — Docker Compose

Hasil `docker compose ps` digunakan sebagai bukti bahwa service yang didefinisikan pada Docker Compose berhasil berjalan.

![Screenshot Docker Compose](./Screenshot%202026-10-07%20165432.png)

---

## Screenshot 2 — Pengujian Curl

Pengujian menggunakan:

```bash
curl http://localhost:8080
```

Screenshot berikut menunjukkan hasil pengujian aplikasi web melalui port `8080`.

![Screenshot Curl](./Screenshot%202026-10-07%20165457.png)

---

# 8. Kesimpulan

Berdasarkan praktikum yang telah dilakukan, Docker dapat digunakan untuk menjalankan aplikasi secara terisolasi menggunakan container.

Pada praktikum ini telah dilakukan:

- Menjalankan container `ubuntu:22.04` secara interaktif.
- Mengecek informasi sistem operasi menggunakan `cat /etc/os-release`.
- Menghapus container menggunakan `docker rm`.
- Membuat aplikasi web sederhana menggunakan Python.
- Membuat custom Docker image menggunakan Dockerfile.
- Menggunakan environment variable untuk menyimpan NIM.
- Melakukan port mapping dari host `8080` ke container `8000`.
- Menjalankan aplikasi dalam detached mode.
- Menguji aplikasi menggunakan `curl`.
- Mendefinisikan service menggunakan Docker Compose.

## Deliverables

Repository ini berisi:

```text
tugas-docker-101012330245/
├── app.py
├── Dockerfile
└── docker-compose.yml
```

Dokumentasi dan bukti praktikum disertakan pada README ini dalam bentuk screenshot hasil pengujian.
