# Anton-Color

 Anton-Color adalah modul Python sederhana untuk memberikan warna pada teks di terminal menggunakan ANSI escape codes. Modul ini memungkinkan pengguna untuk menampilkan teks dalam berbagai warna dan latar belakang yang berbeda.

## Instalasi

Untuk menginstal modul ini, kamu bisa menggunakan `pip`:

```bash
pip install anton-color
```

## Penggunaan

Berikut adalah contoh penggunaan modul ini:

```python
from anton_color import Clr

print(Clr.merah("Halo, ini teks merah!"))
print(Clr.hijau("Teks dengan warna hijau!"))
print(Clr.bg_kuning("Teks dengan latar belakang kuning!"))
```

## Daftar Warna

- **Teks**:
  - `merah`
  - `hijau`
  - `kuning`
  - `biru`
  - `ungu`
  - `cyan`
  - `putih`
  - `hitam`
  - `merah_terang`
  - `hijau_terang`
  - `kuning_terang`
  - `biru_terang`
  - `ungu_terang`
  - `cyan_terang`
  - `putih_terang`
  - `hitam_terang`

- **Latar Belakang**:
  - `bg_merah`
  - `bg_hijau`
  - `bg_kuning`
  - `bg_biru`
  - `bg_ungu`
  - `bg_cyan`
  - `bg_putih`
  - `bg_hitam`
  - `bg_merah_terang`
  - `bg_hijau_terang`
  - `bg_kuning_terang`
  - `bg_biru_terang`
  - `bg_ungu_terang`
  - `bg_cyan_terang`
  - `bg_putih_terang`
  - `bg_hitam_terang`

## Lisensi

Modul ini dilisensikan di bawah [MIT License](LICENSE).
