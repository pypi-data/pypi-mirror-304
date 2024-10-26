class Clr:
    warna = {
        "merah": "\033[91m",
        "hijau": "\033[92m",
        "kuning": "\033[93m",
        "biru": "\033[94m",
        "ungu": "\033[95m",
        "cyan": "\033[96m",
        "putih": "\033[97m",
        "hitam": "\033[90m",
        "merah_terang": "\033[91;1m",
        "hijau_terang": "\033[92;1m",
        "kuning_terang": "\033[93;1m",
        "biru_terang": "\033[94;1m",
        "ungu_terang": "\033[95;1m",
        "cyan_terang": "\033[96;1m",
        "putih_terang": "\033[97;1m",
        "hitam_terang": "\033[90;1m",
        "bg_merah": "\033[101m",
        "bg_hijau": "\033[102m",
        "bg_kuning": "\033[103m",
        "bg_biru": "\033[104m",
        "bg_ungu": "\033[105m",
        "bg_cyan": "\033[106m",
        "bg_putih": "\033[107m",
        "bg_hitam": "\033[100m",
        "bg_merah_terang": "\033[101;1m",
        "bg_hijau_terang": "\033[102;1m",
        "bg_kuning_terang": "\033[103;1m",
        "bg_biru_terang": "\033[104;1m",
        "bg_ungu_terang": "\033[105;1m",
        "bg_cyan_terang": "\033[106;1m",
        "bg_putih_terang": "\033[107;1m",
        "bg_hitam_terang": "\033[100;1m",
        "reset": "\033[0m"
    }

    @staticmethod
    def beri_warna(teks, warna, warna_bg=None):
        kode_warna = Clr.warna.get(warna.lower(), Clr.warna["reset"])
        kode_bg = Clr.warna.get(warna_bg.lower(), "") if warna_bg else ""
        return f"{kode_warna}{kode_bg}{teks}{Clr.warna['reset']}"

    # Metode untuk setiap warna
    @staticmethod
    def merah(teks):
        return Clr.beri_warna(teks, "merah")

    @staticmethod
    def hijau(teks):
        return Clr.beri_warna(teks, "hijau")

    @staticmethod
    def kuning(teks):
        return Clr.beri_warna(teks, "kuning")

    @staticmethod
    def biru(teks):
        return Clr.beri_warna(teks, "biru")

    @staticmethod
    def ungu(teks):
        return Clr.beri_warna(teks, "ungu")

    @staticmethod
    def cyan(teks):
        return Clr.beri_warna(teks, "cyan")

    @staticmethod
    def putih(teks):
        return Clr.beri_warna(teks, "putih")

    @staticmethod
    def hitam(teks):
        return Clr.beri_warna(teks, "hitam")

    @staticmethod
    def merah_terang(teks):
        return Clr.beri_warna(teks, "merah_terang")

    @staticmethod
    def hijau_terang(teks):
        return Clr.beri_warna(teks, "hijau_terang")

    @staticmethod
    def kuning_terang(teks):
        return Clr.beri_warna(teks, "kuning_terang")

    @staticmethod
    def biru_terang(teks):
        return Clr.beri_warna(teks, "biru_terang")

    @staticmethod
    def ungu_terang(teks):
        return Clr.beri_warna(teks, "ungu_terang")

    @staticmethod
    def cyan_terang(teks):
        return Clr.beri_warna(teks, "cyan_terang")

    @staticmethod
    def putih_terang(teks):
        return Clr.beri_warna(teks, "putih_terang")

    @staticmethod
    def hitam_terang(teks):
        return Clr.beri_warna(teks, "hitam_terang")

    # Metode untuk setiap warna latar belakang
    @staticmethod
    def bg_merah(teks):
        return Clr.beri_warna(teks, "bg_merah")

    @staticmethod
    def bg_hijau(teks):
        return Clr.beri_warna(teks, "bg_hijau")

    @staticmethod
    def bg_kuning(teks):
        return Clr.beri_warna(teks, "bg_kuning")

    @staticmethod
    def bg_biru(teks):
        return Clr.beri_warna(teks, "bg_biru")

    @staticmethod
    def bg_ungu(teks):
        return Clr.beri_warna(teks, "bg_ungu")

    @staticmethod
    def bg_cyan(teks):
        return Clr.beri_warna(teks, "bg_cyan")

    @staticmethod
    def bg_putih(teks):
        return Clr.beri_warna(teks, "bg_putih")

    @staticmethod
    def bg_hitam(teks):
        return Clr.beri_warna(teks, "bg_hitam")

    @staticmethod
    def bg_merah_terang(teks):
        return Clr.beri_warna(teks, "bg_merah_terang")

    @staticmethod
    def bg_hijau_terang(teks):
        return Clr.beri_warna(teks, "bg_hijau_terang")

    @staticmethod
    def bg_kuning_terang(teks):
        return Clr.beri_warna(teks, "bg_kuning_terang")

    @staticmethod
    def bg_biru_terang(teks):
        return Clr.beri_warna(teks, "bg_biru_terang")

    @staticmethod
    def bg_ungu_terang(teks):
        return Clr.beri_warna(teks, "bg_ungu_terang")

    @staticmethod
    def bg_cyan_terang(teks):
        return Clr.beri_warna(teks, "bg_cyan_terang")

    @staticmethod
    def bg_putih_terang(teks):
        return Clr.beri_warna(teks, "bg_putih_terang")

    @staticmethod
    def bg_hitam_terang(teks):
        return Clr.beri_warna(teks, "bg_hitam_terang")

    @staticmethod
    def reset(teks):
        return Clr.beri_warna(teks, "reset")