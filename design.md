# Design Document - HR Analytics System

## 1. Tech Stack

| Kebutuhan | Tools |
|---|---|
| Database | PostgreSQL / MySQL |
| Query | SQL (DDL, DML, JOIN, GROUP BY, Subquery, Window Function) |
| Data Cleaning | SQL + Spreadsheet |
| Backend | Tidak digunakan |
| Dashboard | Spreadsheet (Excel/Google Sheets), opsional Power BI |
| Editor | VS Code |
| Version Control | GitHub |

## 2. Arsitektur Sistem

```
Spreadsheet (CSV)
        │
Import ke PostgreSQL/MySQL  (tabel *_raw)
        │
Cleaning SQL   (handling NULL, duplicate, format, normalisasi)
        │
Data Warehouse sederhana  (tabel bersih, siap analisis)
        │
SQL Analysis   (agregasi, JOIN, subquery, window function)
        │
Dashboard   (Pivot Table + Chart / Power BI)
```

Arsitektur ini sengaja dibuat sederhana (tanpa backend, tanpa star schema) agar proyek tetap fokus pada kemampuan inti seorang Data Analyst: SQL, data cleaning, dan visualisasi insight — bukan pada kompleksitas infrastruktur.

## 3. Skema Database (ERD Logis)

8 tabel inti dengan relasi sebagai berikut:

```
department (1) ───< (N) employee
position   (1) ───< (N) employee
employee   (1) ───< (N) attendance
employee   (1) ───< (N) leave_request
employee   (1) ───< (N) performance
employee   (1) ───< (N) training
recruitment  (tabel independen, terhubung logis ke position via nama posisi)
```

### 3.1 Tabel `department`
| Kolom | Tipe | Keterangan |
|---|---|---|
| department_id | INT (PK) | |
| department_name | VARCHAR(100) | |

### 3.2 Tabel `position`
| Kolom | Tipe | Keterangan |
|---|---|---|
| position_id | INT (PK) | |
| position_name | VARCHAR(100) | |
| grade | VARCHAR(10) | Grade jabatan (misal: G1–G5) |

### 3.3 Tabel `employee`
| Kolom | Tipe | Keterangan |
|---|---|---|
| employee_id | INT (PK) | |
| full_name | VARCHAR(150) | |
| gender | VARCHAR(10) | Nilai standar: `Male` / `Female` |
| birth_date | DATE | |
| hire_date | DATE | |
| department_id | INT (FK → department) | |
| position_id | INT (FK → position) | |
| salary | NUMERIC(12,2) | |
| status | VARCHAR(20) | `Active` / `Resigned` / `Terminated` |

### 3.4 Tabel `attendance`
| Kolom | Tipe | Keterangan |
|---|---|---|
| attendance_id | INT (PK) | |
| employee_id | INT (FK → employee) | |
| date | DATE | |
| check_in | TIME | |
| check_out | TIME | |
| status | VARCHAR(20) | `Present` / `Sick` / `Leave` / `Absent` |

### 3.5 Tabel `leave_request`
| Kolom | Tipe | Keterangan |
|---|---|---|
| leave_id | INT (PK) | |
| employee_id | INT (FK → employee) | |
| leave_type | VARCHAR(50) | Cuti tahunan, sakit, melahirkan, dll |
| start_date | DATE | |
| end_date | DATE | |
| duration | INT | Jumlah hari (bisa dihitung/derived) |

### 3.6 Tabel `performance`
| Kolom | Tipe | Keterangan |
|---|---|---|
| performance_id | INT (PK) | |
| employee_id | INT (FK → employee) | |
| period | VARCHAR(10) | Contoh: `2025-Q1` |
| kpi_score | NUMERIC(5,2) | |
| manager_score | NUMERIC(5,2) | |

### 3.7 Tabel `recruitment`
| Kolom | Tipe | Keterangan |
|---|---|---|
| candidate_id | INT (PK) | |
| candidate_name | VARCHAR(150) | |
| position | VARCHAR(100) | |
| source | VARCHAR(50) | LinkedIn, referral, job portal, dll |
| status | VARCHAR(30) | Applied / Interviewed / Hired / Rejected |
| apply_date | DATE | |
| hire_date | DATE | Nullable jika belum/tidak hired |

### 3.8 Tabel `training`
| Kolom | Tipe | Keterangan |
|---|---|---|
| training_id | INT (PK) | |
| employee_id | INT (FK → employee) | |
| course_name | VARCHAR(150) | |
| completion | VARCHAR(20) | `Completed` / `In Progress` / `Not Started` |
| score | NUMERIC(5,2) | Nullable |

## 4. Data Generation Strategy

Karena proyek ini menggunakan data dummy, kualitas dan realisme data sangat menentukan apakah insight yang dihasilkan terasa "nyata" atau artifisial. Strategi generasi data:

### 4.1 Tool
- **Python + Faker** (`Faker('id_ID')` untuk nama, alamat, dan atribut lain bergaya Indonesia)
- `numpy` / `random` untuk distribusi numerik (gaji, KPI) dan probabilitas kejadian (resign, sick leave)
- Script disimpan di `dataset/generate_dummy_data.py`, dengan **random seed tetap** (mis. `random.seed(42)`) agar data reproducible setiap kali script dijalankan ulang
- Output langsung disimpan sebagai 7 file CSV di `dataset/`

### 4.2 Estimasi Jumlah Record per Tabel

| Tabel | Jumlah Baris | Catatan |
|---|---|---|
| department | 6–8 | Perusahaan skala menengah |
| position | 15–20 | Beberapa grade per departemen |
| employee | 300 | Cukup besar untuk agregasi statistik, tidak berlebihan untuk diproses di Spreadsheet |
| attendance | ±40.000 (300 pegawai × 22 hari kerja × 6 bulan) | Tabel terbesar, granular per hari |
| leave | 500–800 (±1–3 per pegawai/tahun) | |
| performance | 1.200 (300 pegawai × 4 kuartal) | Periode kuartalan selama 1 tahun |
| recruitment | 150–250 kandidat | Funnel dengan hire rate realistis ±20–30% |
| training | 500–700 (300 pegawai × 1–3 kursus) | |

> Catatan teknis: volume `attendance` cukup besar untuk agregasi mentah di Excel/Google Sheets. Sebaiknya agregasi (mis. per bulan/status) dilakukan di SQL terlebih dahulu sebelum data diekspor ke Spreadsheet untuk Pivot Table (lihat bagian 6).

### 4.3 Pendekatan agar Data Tidak Terasa Artifisial

Data dummy yang di-generate murni acak (uniform random) cenderung menghasilkan insight yang datar dan tidak meyakinkan. Untuk itu, generator data dirancang dengan pola dan korelasi yang disengaja:

| Aspek | Pendekatan |
|---|---|
| **Gaji** | Ditentukan berdasarkan kombinasi `grade` (dari tabel `position`, diakses via `position_id` pada `employee`) dan `department`, memakai distribusi normal dengan noise kecil — bukan random uniform. Departemen seperti IT/Finance diberi baseline gaji lebih tinggi. `employee` tidak menyimpan `grade` secara langsung — nilai ini selalu diturunkan via JOIN ke `position` agar tidak terjadi duplikasi data (denormalisasi tidak perlu). |
| **Turnover** | Probabilitas `status = Resigned` dibuat meningkat seiring lama masa kerja tertentu (mis. peak di tahun ke-2–3), bukan random per baris, agar pola turnover dapat "ditemukan" lewat query. |
| **Attendance** | Pola tidak seragam per hari — mis. probabilitas `Sick`/`Leave` sedikit lebih tinggi pada hari Jumat/Senin — sehingga ada insight musiman yang bisa dilaporkan. |
| **Recruitment funnel** | Rasio `Applied → Interview → Hired` dibuat proporsional dan berbeda per `source` (mis. referral punya hire rate lebih tinggi dari job portal), agar insight "sumber kandidat terbaik" masuk akal. |
| **Training vs Performance** | Sengaja dibuat korelasi lemah-positif: pegawai dengan `completion = Completed` pada training diberi sedikit bonus pada `kpi_score`, sehingga query korelasi di analisis Level 2 punya temuan yang nyata untuk ditulis di README. |

Pendekatan ini membuat proses analisis terasa seperti "menemukan" insight dari data — bukan sekadar melaporkan angka acak — sehingga lebih meyakinkan saat dipresentasikan sebagai portofolio.

### 4.4 Formula Perhitungan Gaji (Salary Generation)

Agar tidak perlu menebak logika saat menulis script, gaji dihitung dengan formula eksplisit berikut:

```
salary = base_salary_per_grade × department_multiplier × (1 + noise)
```

**a) Base Salary per Grade** (nilai awal, dalam Rupiah, sebelum multiplier)

| Grade | Base Salary (IDR) |
|---|---|
| G1 | 5.000.000 |
| G2 | 7.500.000 |
| G3 | 11.000.000 |
| G4 | 16.000.000 |
| G5 | 25.000.000 |

**b) Department Multiplier** (mencerminkan variasi kompensasi antar fungsi)

| Departemen | Multiplier |
|---|---|
| IT | 1.25 |
| Finance | 1.20 |
| Sales | 1.10 |
| Marketing | 1.05 |
| Operations | 1.00 |
| HR | 0.95 |
| Admin/GA | 0.90 |

*(Sesuaikan daftar departemen ini dengan isi `department.csv` yang dibuat pada Level 1.)*

**c) Noise** — variasi acak individual agar gaji dalam grade+departemen yang sama tidak identik semua:

```
noise ~ Normal(mean=0, std_dev=0.08)   # ±8% variasi acak
```

Di Python (contoh implementasi konseptual):

```python
import numpy as np

base_salary = {"G1": 5_000_000, "G2": 7_500_000, "G3": 11_000_000,
                "G4": 16_000_000, "G5": 25_000_000}

dept_multiplier = {"IT": 1.25, "Finance": 1.20, "Sales": 1.10,
                     "Marketing": 1.05, "Operations": 1.00,
                     "HR": 0.95, "Admin": 0.90}

def generate_salary(grade, department):
    base = base_salary[grade]
    mult = dept_multiplier[department]
    noise = np.random.normal(loc=0, scale=0.08)
    salary = base * mult * (1 + noise)
    return round(salary, -3)  # dibulatkan ke ribuan terdekat
```

**d) Alur penerapan saat generate data `employee.csv`:**
1. Tentukan `position_id` pegawai (yang sudah punya `grade` dan berelasi ke posisi tertentu).
2. Tentukan `department_id` pegawai.
3. Ambil `grade` dari tabel `position` via `position_id` (bukan kolom langsung di `employee`).
4. Hitung `salary` menggunakan formula di atas.
5. Simpan `salary` sebagai kolom hasil generate di `employee.csv` — bukan formula, hanya nilai akhir (karena `employee.salary` di skema adalah nilai statis `NUMERIC(12,2)`, bukan computed column).

> Formula ini hanya dipakai pada tahap *generasi data dummy* (di luar database). Setelah data masuk ke PostgreSQL/MySQL, kolom `salary` tetap berupa nilai tersimpan biasa — bukan derived/computed column — supaya query analisis (`AVG`, `RANK()`, dll di §6) bekerja langsung tanpa perlu menghitung ulang.

## 5. Alur Data Cleaning

Pola umum data cleaning yang diterapkan pada tabel `*_raw` sebelum masuk ke tabel final:

1. **Handling NULL** — identifikasi kolom wajib (mis. `full_name`, `employee_id`) yang tidak boleh kosong; isi nilai default atau exclude baris tidak valid.
2. **Handling Duplicate** — deduplikasi berdasarkan primary key alami (mis. kombinasi `employee_id` + `date` pada attendance).
3. **Standardisasi Kategori** — normalisasi nilai kategori tidak konsisten, contoh:
   ```sql
   UPDATE employee
   SET gender = 'Male'
   WHERE gender = 'M';
   ```
4. **Format Tanggal** — konversi berbagai format tanggal (DD/MM/YYYY, MM-DD-YYYY, dll) ke tipe `DATE` standar.
5. **Validasi Referensial** — memastikan `department_id` dan `position_id` pada `employee` valid dan ada di tabel master.
6. **Derived Column** — menghitung kolom turunan seperti `duration` pada tabel `leave` (`end_date - start_date`).

## 6. Desain Analisis SQL

Kategori query analisis yang disiapkan di `analysis.sql`:

| Kategori | Contoh Insight | Teknik SQL |
|---|---|---|
| Employee Overview | Total pegawai, komposisi gender/departemen/posisi | `COUNT`, `GROUP BY`, `JOIN` |
| Payroll | Rata-rata gaji, top 10 gaji, distribusi gaji per departemen | `AVG`, `ORDER BY`, `RANK() OVER (PARTITION BY ...)` |
| Attendance | Distribusi status kehadiran, tingkat absensi per bulan | `GROUP BY`, `CASE WHEN` |
| Turnover | Turnover rate, jumlah resign per departemen | `GROUP BY`, subquery |
| Recruitment | Funnel rekrutmen, sumber kandidat terbaik | `GROUP BY`, `CASE WHEN` |
| Performance | Rata-rata KPI, top & bottom performer per periode | `AVG`, `RANK() OVER (...)` |
| Training | Efektivitas training terhadap skor performa | `JOIN`, `AVG`, subquery korelatif |

Contoh query representatif (lihat juga PRD bagian pertanyaan bisnis):

```sql
-- Ranking gaji per departemen (window function)
SELECT
    full_name,
    department_name,
    salary,
    RANK() OVER (PARTITION BY department_name ORDER BY salary DESC) AS salary_rank
FROM employee e
JOIN department d ON e.department_id = d.department_id;
```

```sql
-- Turnover rate
SELECT
    ROUND(
        100.0 * SUM(CASE WHEN status <> 'Active' THEN 1 ELSE 0 END) / COUNT(*), 2
    ) AS turnover_rate_percent
FROM employee;
```

## 7. Desain Dashboard

Menggunakan Pivot Table + Chart di Spreadsheet (Excel/Google Sheets), dengan 5 sheet/section:

| Dashboard | Isi |
|---|---|
| 1. Employee Overview | Total Employee, Male/Female, per Department, per Position |
| 2. Attendance | Present, Sick, Leave, Absent (per bulan) |
| 3. Payroll | Average Salary, Highest Salary, Salary Distribution per Departemen |
| 4. Recruitment | Applicant, Interview, Hired, Rejected (funnel chart) |
| 5. Performance | Average KPI, Top Performer, Lowest Performer |

Setiap dashboard idealnya menggunakan hasil query dari `analysis.sql` yang di-export ke CSV, kemudian dijadikan sumber Pivot Table agar proses tetap traceable dari SQL ke visual.

Versi lanjutan (opsional): dashboard yang sama dibangun ulang di Power BI dengan koneksi langsung ke database untuk menunjukkan kemampuan tool BI tambahan.

## 8. Struktur Folder Proyek

```
HR Analytics System
│
├── dataset
│     generate_dummy_data.py
│     employee.csv
│     attendance.csv
│     leave.csv
│     performance.csv
│     training.csv
│     recruitment.csv
│     department.csv
│     position.csv
│
├── database
│     create_table.sql
│     insert.sql
│     cleaning.sql
│     analysis.sql
│
├── dashboard
│     HR Dashboard.xlsx
│
├── documentation
│     ERD.png
│     Database Schema.png
│     data_dictionary.md
│
├── PRD.md
├── design.md
├── task.md
└── README.md
```

## 9. Konvensi & Standar

- Penamaan tabel dan kolom: `snake_case`, singular (mis. `employee`, bukan `employees`).
- Semua tabel mentah diberi suffix `_raw` (mis. `employee_raw`) sebelum dibersihkan menjadi tabel final.
- Semua script SQL disusun urut eksekusi: `create_table.sql` → `insert.sql` → `cleaning.sql` → `analysis.sql`.
- Commit Git dilakukan per tahap (Level 1–4) agar histori proyek mencerminkan proses kerja seorang Data Analyst.

## 10. Kemungkinan Pengembangan Lanjutan (Future Work)

- Migrasi ke star schema (fact & dimension table) untuk latihan data warehousing.
- Otomatisasi ETL sederhana menggunakan Python (pandas) sebagai pengganti proses manual.
- Dashboard interaktif berbasis Power BI/Tableau dengan filter dinamis.
- Penambahan analisis prediktif sederhana (mis. prediksi risiko turnover) menggunakan Python.