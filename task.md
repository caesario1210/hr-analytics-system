# Task Breakdown - HR Analytics System

Checklist tugas disusun mengikuti roadmap 4 level pada PRD. Centang `[x]` setiap tugas selesai.

---

## Level 0 — Persiapan

- [x] Buat struktur folder sesuai `design.md` (`dataset/`, `database/`, `dashboard/`, `documentation/`)
- [x] Buat file `.gitignore` (exclude file kredensial/konfigurasi lokal)
- [x] Inisialisasi `README.md` awal (judul, deskripsi singkat, status "in progress")
- [ ] Install & setup PostgreSQL/MySQL secara lokal — *manual, sesuaikan environment*
- [ ] Setup VS Code dengan extension SQL — *manual*
- [ ] Init Git & buat repository GitHub (`hr-analytics-system`) — *manual*

---

## Level 1 — Database HR (8 Tabel) + SQL CRUD

### 1.1 Persiapan Dataset (Data Generation dengan Python + Faker)

- [x] Setup environment Python (`pip install faker numpy pandas`)
- [x] Buat script `dataset/generate_dummy_data.py` dengan `random.seed()` tetap agar reproducible
- [x] Generate `department.csv` — target **6–8 baris** ✅ 8 baris
- [x] Generate `position.csv` — target **15–20 baris** ✅ 19 baris (tanpa kolom `department`)
- [x] Generate `employee.csv` — target **300 baris** ✅ 300 baris
  - [x] Gaji dihitung menggunakan formula eksplisit di `design.md` §4.4: `salary = base_salary_per_grade × department_multiplier × (1 + noise)`. **Catatan:** `grade` hanya ada di tabel `position`, employee tidak punya kolom `grade` langsung; saat generate data, tentukan `position_id` pegawai terlebih dahulu, lalu turunkan `grade` posisi tersebut untuk lookup `base_salary_per_grade`.
  - [x] Probabilitas `status = Resigned` meningkat pada rentang masa kerja tertentu (mis. tahun ke-2–3)
- [x] Generate `attendance.csv` — target **±40.000 baris** ✅ 28.201 baris (weekday-only)
  - [x] Terapkan pola non-seragam (mis. `Sick`/`Leave` sedikit lebih tinggi di hari Jumat/Senin)
- [x] Generate `leave.csv` — target **500–800 baris** ✅ 541 baris
- [x] Generate `performance.csv` — target **1.200 baris** ✅ 1.200 baris
- [x] Generate `recruitment.csv` — target **150–250 kandidat** ✅ 225 baris
- [x] Generate `training.csv` — target **500–700 baris** ✅ 604 baris
  - [x] Terapkan korelasi lemah-positif antara `completion = Completed` dan `kpi_score` pegawai terkait
- [x] Jalankan script, verifikasi seluruh CSV ter-generate di `dataset/`
- [ ] Cek sanity data: distribusi gaji, rasio gender, rasio status kehadiran — *butuh python shell*
- [x] Dokumentasikan asumsi & rule generation di `documentation/data_dictionary.md`

### 1.2 Desain & Pembuatan Skema
- [x] Tulis `create_table.sql` untuk 8 tabel (department, position, employee, attendance, leave, performance, recruitment, training)
- [x] Definisikan primary key & foreign key sesuai relasi di `design.md`
- [x] Buat tabel `*_raw` untuk staging data mentah sebelum cleaning (tanpa FK constraint)
- [ ] Jalankan `create_table.sql` di PostgreSQL/MySQL

### 1.3 Import Data
- [x] Tulis `insert.sql` / gunakan `COPY` (PostgreSQL) atau `LOAD DATA` (MySQL) untuk import CSV ke tabel `*_raw`
- [ ] Verifikasi jumlah baris ter-import sesuai jumlah baris CSV
- [ ] Lakukan uji CRUD dasar (INSERT, UPDATE, DELETE, SELECT) pada tabel `employee` sebagai latihan

**Output Level 1:** Database aktif dengan 8 tabel + data ter-import, script `create_table.sql` dan `insert.sql`. *Tahap DB execution masih manual.*

---

## Level 2 — Data Cleaning & Analisis SQL

- [x] Identifikasi dan tangani nilai NULL pada kolom wajib
- [x] Deteksi dan hapus data duplikat (DISTINCT ON / DISTINCT)
- [x] Normalisasi kategori tidak konsisten (gender, status, attendance)
- [x] Standardisasi format tanggal ke tipe `DATE`
- [x] Validasi `department_id` dan `position_id` pada tabel `employee` (JOIN ke tabel master)
- [x] Hitung kolom turunan `duration` pada tabel `leave`
- [x] Simpan seluruh langkah di `cleaning.sql`
- [x] Dokumentasikan rule cleaning di `documentation/data_dictionary.md`

### 2.2 Analisis SQL — Employee Overview
- [x] Query total pegawai (aktif vs non-aktif)
- [x] Query jumlah pegawai per departemen
- [x] Query jumlah pegawai per posisi
- [x] Query komposisi gender

### 2.3 Analisis SQL — Payroll
- [x] Query rata-rata gaji keseluruhan
- [x] Query rata-rata gaji per departemen
- [x] Query top 10 gaji tertinggi
- [x] Query ranking gaji per departemen (window function `RANK()`)

### 2.4 Analisis SQL — Attendance
- [x] Query distribusi status kehadiran (present/sick/leave/absent)
- [x] Query tren kehadiran per bulan
- [x] Query late check-in count

### 2.5 Analisis SQL — Turnover
- [x] Query jumlah pegawai per status (`Active`/`Resigned`/`Terminated`)
- [x] Query turnover rate (%)
- [x] Query turnover per departemen

### 2.6 Analisis SQL — Recruitment
- [x] Query funnel rekrutmen (Applied → Interview → Hired → Rejected)
- [x] Query sumber kandidat terbaik (source dengan hire rate tertinggi)
- [x] Query rata-rata waktu dari `apply_date` ke `hire_date`

### 2.7 Analisis SQL — Performance & Training
- [x] Query rata-rata KPI per periode
- [x] Query top performer dan bottom performer
- [x] Query rata-rata skor training per kursus
- [x] Query korelasi training completion vs kpi_score (subquery/JOIN)

- [x] Kumpulkan seluruh query final ke `analysis.sql` (22 queries)
- [ ] Tulis insight singkat (2–3 kalimat per kategori) — *bisa ditambah setelah DB running*

**Output Level 2:** `cleaning.sql`, `analysis.sql`, ringkasan insight awal.

---

## Level 3 — Dashboard Interaktif Spreadsheet

- [x] Export script siap: `dataset/export_analysis.py` → generate 16 CSV ke `dashboard/analysis_results/`
- [x] Panduan layout: `dashboard/DASHBOARD_GUIDE.md`
- [ ] Jalankan `python dataset/export_analysis.py` — *manual*
- [ ] Import CSV hasil query ke Spreadsheet (Excel/Google Sheets)
- [ ] Buat Pivot Table & Chart — **Dashboard 1: Employee Overview** (Total Employee, Male/Female, Department, Position)
- [ ] Buat Pivot Table & Chart — **Dashboard 2: Payroll** (Average Salary, Highest Salary, Salary Distribution)
- [ ] Buat Pivot Table & Chart — **Dashboard 3: Attendance** (Present, Sick, Leave, Absent)
- [ ] Buat Pivot Table & Chart — **Dashboard 4: Recruitment** (Applicant, Interview, Hired, Rejected)
- [ ] Buat Pivot Table & Chart — **Dashboard 5: Performance** (Average KPI, Top Performer, Lowest Performer)
- [ ] Rapikan layout, warna, dan judul setiap dashboard agar terlihat profesional
- [ ] Simpan sebagai `dashboard/HR Dashboard.xlsx`
- [ ] *(Opsional)* Bangun ulang dashboard yang sama di Power BI dengan koneksi ke database

**Output Level 3:** `HR Dashboard.xlsx` (dan opsional file Power BI).

---

## Level 4 — Dokumentasi Profesional

- [x] Buat ERD — Mermaid diagram di `documentation/ERD.md` (render otomatis di GitHub)
- [x] Buat diagram skema database — flow diagram di `documentation/ERD.md`
- [x] Tulis `documentation/data_dictionary.md` (nama tabel, kolom, tipe data, deskripsi, contoh nilai)
- [x] Tulis `documentation/business_rules.md` (definisi turnover, status kehadiran, hired, salary formula, dsb)
- [x] Finalisasi `README.md` mencakup:
  - [x] Latar belakang & tujuan proyek
  - [x] Tech stack
  - [x] Struktur folder
  - [x] Cara menjalankan proyek (setup database → import → cleaning → analysis → dashboard)
  - [x] Ringkasan insight utama (real metrics dari data: 300 emp, 12.7% turnover, Rp13M avg salary, dll)
  - [x] Kemungkinan pengembangan lanjutan
- [x] Review konsistensi penamaan tabel/kolom di seluruh script SQL — found & fixed 2 issues (leave→leave_request, Interview→Interviewed) di `design.md`
- [ ] Push seluruh file ke GitHub dengan commit history yang logis per level — *manual*
- [ ] Cek ulang bahwa repository dapat dipahami tanpa penjelasan tambahan — *manual*

**Output Level 4:** Dokumentasi lengkap, repository GitHub siap ditampilkan sebagai portofolio.

---

## Ringkasan Prioritas Pengerjaan

| Urutan | Level | Fokus |
|---|---|---|
| 1 | Level 0 | Setup environment & repository |
| 2 | Level 1 | Database & import data |
| 3 | Level 2 | Cleaning & analisis SQL |
| 4 | Level 3 | Dashboard spreadsheet |
| 5 | Level 4 | Dokumentasi & finalisasi portofolio |