# PRD - HR Analytics System

## 1. Ringkasan Proyek

| Item | Keterangan |
|---|---|
| Nama Proyek | HR Analytics System |
| Jenis | Portfolio Project (Data Analyst / BI Analyst) |
| Tujuan Utama | Menunjukkan kemampuan end-to-end data analytics: database design, SQL, data cleaning, analisis, dan dashboard |
| Target Posisi | Data Analyst, Business Intelligence Analyst, Junior Business Analyst |
| Status | Perencanaan |

## 2. Latar Belakang

Departemen HR pada perusahaan pada umumnya mengelola data yang tersebar di banyak sumber: data pegawai, absensi, cuti, performa, rekrutmen, dan pelatihan. Data yang tersebar ini menyulitkan manajemen dalam mengambil keputusan berbasis data (data-driven decision).

Proyek ini mensimulasikan proses seorang Data Analyst dalam mengubah data mentah HR (CSV) menjadi informasi yang siap dipakai untuk pengambilan keputusan, melalui proses: import data → cleaning → data warehouse sederhana → analisis SQL → dashboard.

## 3. Tujuan Proyek

1. Membangun database HR yang relasional dan terstruktur (8 tabel inti).
2. Melakukan proses data cleaning dan transformasi menggunakan SQL.
3. Melakukan analisis data HR untuk menjawab pertanyaan bisnis (headcount, turnover, payroll, attendance, recruitment funnel, performance).
4. Membangun dashboard visual (Spreadsheet, opsional Power BI) yang merangkum insight utama.
5. Mendokumentasikan proyek secara profesional di GitHub sebagai portofolio.

## 4. Target Pengguna (Persona)

| Persona | Kebutuhan |
|---|---|
| HR Manager | Melihat ringkasan headcount, turnover, dan distribusi departemen |
| HR Operations | Memantau absensi dan cuti pegawai |
| Finance/Payroll | Melihat rata-rata gaji, distribusi gaji, top salary |
| Recruiter | Memantau funnel rekrutmen (applicant → interview → hired) |
| Manager Tim | Melihat performa (KPI) tim dan pelatihan pegawai |
| (Perekrut/Reviewer CV) | Menilai kemampuan SQL, database design, dan storytelling data dari pemilik proyek |

## 5. Ruang Lingkup (Scope)

### 5.1 In-Scope
- Desain database relasional 8 tabel: `employee`, `department`, `position`, `attendance`, `leave`, `performance`, `recruitment`, `training`.
- Import data dari CSV ke PostgreSQL/MySQL (tabel `*_raw`).
- Data cleaning menggunakan SQL (handling NULL, duplicate, normalisasi format).
- Query analisis SQL: agregasi, JOIN, GROUP BY, subquery, window function.
- Dashboard menggunakan Spreadsheet (Pivot Table + Chart), opsional Power BI.
- Dokumentasi: README, ERD, data dictionary, business rules.

### 5.2 Out-of-Scope
- Backend/API (tidak diperlukan pada versi ini).
- Aplikasi web front-end interaktif.
- Real-time data pipeline / ETL otomatis.
- Autentikasi/role-based access control.
- Data personal pegawai sungguhan (menggunakan data dummy/sintetis).

## 6. Functional Requirements

| ID | Kebutuhan | Prioritas |
|---|---|---|
| FR-1 | Sistem harus memiliki skema database dengan 8 tabel sesuai domain HR | Must |
| FR-2 | Data CSV harus dapat diimpor ke tabel `*_raw` di database | Must |
| FR-3 | Tersedia script SQL untuk membersihkan data (NULL, duplikat, format tanggal, normalisasi kategori) | Must |
| FR-4 | Tersedia minimal 15 query analisis bisnis (headcount, turnover, payroll, attendance, recruitment, performance) | Must |
| FR-5 | Tersedia dashboard spreadsheet dengan minimal 5 sub-dashboard (Employee, Attendance, Payroll, Recruitment, Performance) | Must |
| FR-6 | Tersedia ERD dan data dictionary | Must |
| FR-7 | Tersedia README yang menjelaskan tujuan, cara menjalankan, dan insight proyek | Must |
| FR-8 | Dashboard opsional dapat dikembangkan di Power BI | Could |
| FR-9 | Query analisis menggunakan window function (contoh: ranking gaji per departemen) | Should |

## 7. Non-Functional Requirements

| ID | Kebutuhan |
|---|---|
| NFR-1 | Struktur folder proyek rapi dan konsisten (dataset, database, dashboard, documentation) |
| NFR-2 | Seluruh script SQL dapat dijalankan ulang (reproducible) dari awal (create table → insert → cleaning → analysis) |
| NFR-3 | Penamaan tabel dan kolom konsisten (snake_case) |
| NFR-4 | Data dummy yang digunakan realistis (distribusi gaji, gender, departemen masuk akal) |
| NFR-5 | Proyek di-version control dengan Git/GitHub, dengan commit history yang logis per tahap |

## 8. Pertanyaan Bisnis yang Harus Terjawab

1. Berapa total pegawai aktif dan non-aktif saat ini?
2. Bagaimana komposisi pegawai per departemen, posisi, dan gender?
3. Berapa rata-rata, gaji tertinggi, dan distribusi gaji per departemen?
4. Bagaimana pola kehadiran pegawai (present, sick, leave, absent)?
5. Berapa turnover rate perusahaan?
6. Bagaimana funnel rekrutmen (applicant → interview → hired → rejected) dan sumber kandidat terbaik?
7. Siapa top performer dan bottom performer berdasarkan KPI?
8. Bagaimana efektivitas training terhadap skor performa pegawai?

## 9. Deliverables

1. `database/create_table.sql`, `insert.sql`, `cleaning.sql`, `analysis.sql`
2. Dataset CSV dummy (7 file)
3. Dashboard Spreadsheet (`HR Dashboard.xlsx`) — opsional versi Power BI
4. Dokumentasi: `ERD.png`, `Database Schema.png`, `data_dictionary.md`
5. `README.md` di root repository GitHub
6. `PRD.md`, `design.md`, `task.md` (dokumen ini)

## 10. Roadmap Bertahap

| Level | Fokus | Output |
|---|---|---|
| Level 1 | Database HR (8 tabel) + SQL CRUD | Schema + data ter-import |
| Level 2 | Data cleaning & analisis SQL | Script cleaning + analysis, insight awal |
| Level 3 | Dashboard interaktif Spreadsheet | Pivot Table, Chart, KPI |
| Level 4 | Dokumentasi profesional | ERD, data dictionary, business rules, README |

## 11. Metrik Keberhasilan Proyek

- Semua query analisis berjalan tanpa error dan menghasilkan insight yang masuk akal.
- Dashboard menampilkan minimal 5 kategori insight (Employee, Attendance, Payroll, Recruitment, Performance).
- Repository GitHub memiliki dokumentasi lengkap (README, ERD, data dictionary) sehingga siapapun bisa memahami proyek tanpa penjelasan tambahan.
- Proyek dapat dijelaskan secara lisan dalam wawancara kerja (storytelling: masalah → proses → insight → rekomendasi).

## 12. Risiko & Batasan

| Risiko | Mitigasi |
|---|---|
| Data dummy kurang realistis sehingga insight terasa artifisial | Gunakan generator data dengan distribusi statistik wajar (misal Python `faker`) |
| Scope merambat (scope creep) ke fitur backend/web app | Tetap berpegang pada scope Level 1–4, fitur lanjutan dicatat sebagai "future work" |
| Query SQL terlalu sederhana sehingga kurang menonjolkan skill | Sertakan minimal satu window function dan satu subquery kompleks per kategori analisis |