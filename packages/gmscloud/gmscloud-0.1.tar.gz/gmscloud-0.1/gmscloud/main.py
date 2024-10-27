import win32print
import sys
from beautifultable import BeautifulTable
from .print_surat_jalan_utils import print_surat_jalan 
from .do_print_utils import do_print 
from .get_app_info import get_app_info
# ANSI escape codes for colors
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
RED = "\033[31m"

def select_printer():
    # Mengambil daftar printer lokal
    printer_list = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)
    printer_names = [printer_info[2] for printer_info in printer_list]
    return printer_names

def print_ascii_art():
    art = r"""
   ____                   ____  _                    _ 
 / ___| _ __ ___   ___  / ___|| |  ___   _   _   __| |
| |  _ | '_ ` _ \ / __|| |    | | / _ \ | | | | / _` |
| |_| || | | | | |\__ \| |___ | || (_) || |_| || (_| |
 \____||_| |_| |_||___/ \____||_| \___/  \__,_| \__,_|                                                                        
    """
    print(art)
    print(get_app_info())

def print_separator():
    print("\n" + "=" * 50 + "\n")

def main():
    print_ascii_art()

    company_code = input(f"{YELLOW}Masukkan Kode Perusahaan: {RESET}")
    print(f"{CYAN}Kode Perusahaan yang dimasukkan: {BOLD}{company_code}{RESET}")

    print_separator()

    printers = select_printer()

    # Pilih printer
    print(f"{GREEN}Pilih Printer:{RESET}")
    for idx, printer in enumerate(printers):
        print(f"{idx + 1}. {printer}")

    printer_choice = int(input(f"{YELLOW}Masukkan nomor printer yang dipilih: {RESET}")) - 1
    selected_printer = printers[printer_choice]

    while True:
        print_separator()

        # Masukkan ID Dokumen
        doc_id = input(f"{YELLOW}Masukkan ID Dokumen (atau ketik 'exit' untuk keluar): {RESET}")
        if doc_id.lower() == 'exit':
            print(f"{GREEN}Terima kasih telah menggunakan aplikasi ini!{RESET}")
            break

        # Pilih jenis tombol print
        print(f"{GREEN}Pilih jenis print:{RESET}")
        print("1. Surat Jalan")
        # Tambahkan opsi lainnya sesuai kebutuhan

        print_choice = int(input(f"{YELLOW}Masukkan nomor jenis print yang dipilih: {RESET}"))

        # Proses pencetakan berdasarkan pilihan
        print(f"{CYAN}Printer yang dipilih: {BOLD}{selected_printer}{RESET}")

        if print_choice == 1:
            print_surat_jalan(doc_id, selected_printer, company_code)  # Mengirim company_code ke print_surat_jalan
        else:
            print(f"{RED}Pilihan tidak valid!{RESET}")

if __name__ == "__main__":
    main()
