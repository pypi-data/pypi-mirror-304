import requests
import json
from beautifultable import BeautifulTable
from .do_print_utils import do_print  # Mengimpor fungsi do_print
from .get_base_url import get_base_url

def print_surat_jalan(doc_id, selected_printer, company_code):
    # Menggunakan get_base_url untuk mendapatkan domain yang sesuai
    base_url = get_base_url(company_code)

    # Menggunakan company_code untuk membangun URL
    response = requests.get(f"{base_url}/surat_jalan/list/id/{doc_id}")
    json_obj = json.loads(response.content)

    header = BeautifulTable()
    header.columns.width = 40
    header.columns.header = [
        f"{json_obj['data'][0]['PERUSAHAAN'][0]['PERUSAHAAN_NAMA']}\n{json_obj['data'][0]['PERUSAHAAN'][0]['PERUSAHAAN_ALAMAT']}\n{json_obj['data'][0]['PERUSAHAAN'][0]['PERUSAHAAN_TELP']}",
        f"Nomor :  {json_obj['data'][0]['SURAT_JALAN_NOMOR']}\nTanggal : {json_obj['data'][0]['TANGGAL']}\nKepada : {json_obj['data'][0]['NAMA']}  "
    ]
    header.rows.append(["", ""])
    header.set_style(BeautifulTable.STYLE_NONE)
    header.columns.alignment = BeautifulTable.ALIGN_LEFT

    table = BeautifulTable()
    subtable = BeautifulTable()
    for result in json_obj['data'][0]['BARANG']:
        subtable.rows.append([result['MASTER_BARANG_NAMA'], result['SURAT_JALAN_BARANG_QUANTITY']])

    subtable2 = BeautifulTable()
    subtable2.rows.append(["                                          "])
    subtable2.rows.append([f"{json_obj['data'][0]['SURAT_JALAN_KETERANGAN']}"])

    table.rows.append([subtable2, subtable])
    table.set_style(BeautifulTable.STYLE_NONE)
    table.columns.alignment = BeautifulTable.ALIGN_LEFT

    ttd = BeautifulTable()
    ttd.columns.width = 25
    ttd.columns.header = ["Diterima Oleh", "Dibawa Oleh", "Dibuat Oleh"]
    ttd.rows.append(["\n", "\n", "\n"])
    ttd.rows.append(["                         ", "                         ", "                         "])
    ttd.rows.append(
        [f"{json_obj['data'][0]['NAMA']}", f"{json_obj['data'][0]['DRIVER']}", f"{json_obj['data'][0]['USER']}"])
    ttd.set_style(BeautifulTable.STYLE_NONE)
    ttd.columns.alignment = BeautifulTable.ALIGN_CENTER

    klaim = BeautifulTable()
    klaim.columns.width = 80
    klaim.columns.header = ["Klaim hanya dapat dilayani dalam waktu 1x24 Jam sejak barang diterima."]
    klaim.rows.append(["                                                                                "])
    klaim.set_style(BeautifulTable.STYLE_NONE)
    klaim.columns.alignment = BeautifulTable.ALIGN_CENTER

    judul = BeautifulTable()
    judul.columns.width = 80
    judul.columns.header = ["SURAT JALAN"]
    judul.rows.append(["                                                                      "])
    judul.set_style(BeautifulTable.STYLE_NONE)
    judul.columns.alignment = BeautifulTable.ALIGN_CENTER

    with open(f'{doc_id}.txt', 'w') as f:
        f.write(str(header))
        f.write("\n")
        f.write(str(judul))
        f.write("\n")
        f.write(str(table))
        f.write("\n")
        f.write("\n")
        f.write("\n")
        f.write(str(ttd))
        f.write("\n")
        f.write("\n")
        f.write(str(klaim))

    do_print(doc_id, selected_printer)
