import datetime
import pandas as pd
import streamlit as st


# Fungsi helper untuk mengubah format angka menjadi Rupiah (titik sebagai pemisah ribuan)
def rupiah(angka):
  return f"Rp {int(angka):,}".replace(",", ".")


# Fungsi untuk mengosongkan kembali semua isian data
def reset_data():
  st.session_state["input_nama"] = ""
  st.session_state["tipe_pesanan"] = "Dine In"
  st.session_state["metode_pembayaran"] = "Cash"
  st.session_state["produk_dipilih"] = "Laptop"
  st.session_state["jumlah_produk_key"] = 0
  st.session_state["pesanan"] = []
  st.rerun()


# Menyiapkan tempat penyimpanan sementara di web
if "input_nama" not in st.session_state:
  st.session_state["input_nama"] = ""
if "tipe_pesanan" not in st.session_state:
  st.session_state["tipe_pesanan"] = "Dine In"
if "metode_pembayaran" not in st.session_state:
  st.session_state["metode_pembayaran"] = "Cash"
if "produk_dipilih" not in st.session_state:
  st.session_state["produk_dipilih"] = "Laptop"
if "jumlah_produk_key" not in st.session_state:
  st.session_state["jumlah_produk_key"] = 0
if "pesanan" not in st.session_state:
  st.session_state["pesanan"] = []

# Bagian judul dan informasi toko
st.title("ELECTRONIC GERAI")
st.subheader("Solusi Cerdas Elektronik Anda")
st.write("Jl. Teknologi No 5, Kota Digital, Indonesia")
st.write("(021) 87654321")
st.write("---")

# Menampilkan tanggal dan waktu saat ini
now = datetime.datetime.now()
waktu_sekarang = now.strftime("%Y-%m-%d %H:%M:%S")
st.write(waktu_sekarang)

# Form isian data pembeli
nama_pelanggan = st.text_input(
    "Nama Pelanggan",
    placeholder="Masukkan nama pelanggan...",
    key="input_nama",
)
tipe_pesanan = st.selectbox(
    "Tipe Pesanan", ["Dine In", "Take Away"], key="tipe_pesanan"
)
metode_pembayaran = st.selectbox(
    "Metode Pembayaran", ["Cash", "Debit", "E-Wallet"], key="metode_pembayaran"
)

st.write("---")
st.write("### Rincian Pesanan ###")

# Pilihan barang yang mau dibeli
produk_dipilih = st.selectbox(
    "Pilih Produk",
    ["Laptop", "Television", "HandPhone", "AC", "Microwave"],
    key="produk_dipilih",
)

# Daftar harga barang
harga_produk_dict = {
    "Laptop": 5000000,
    "Television": 7000000,
    "HandPhone": 3000000,
    "AC": 10000000,
    "Microwave": 2000000,
}

jumlah_produk = st.number_input(
    "Masukkan jumlah produk",
    min_value=0,
    max_value=100,
    step=1,
    key="jumlah_produk_key",
)

# Menghitung harga total barang yang sedang dipilih
subtotal_sekarang = harga_produk_dict[produk_dipilih] * jumlah_produk
st.write(
    f"Subtotal untuk {produk_dipilih} ({jumlah_produk} pcs):"
    f" {rupiah(subtotal_sekarang)}"
)

# Tombol untuk memasukkan barang ke daftar pilihan
if st.button("Tambah ke Produk Pilihan"):
  if jumlah_produk > 0:
    st.session_state.pesanan.append({
        "produk": produk_dipilih,
        "jumlah": jumlah_produk,
        "subtotal": subtotal_sekarang,
    })
  else:
    st.warning("Jumlah produk harus lebih dari 0!")

# Menampilkan semua daftar barang yang sudah dipilih beserta total harganya
if st.session_state.pesanan:
  st.write("---")
  st.write("**Daftar Produk yang Dipilih:**")
  for item in st.session_state.pesanan:
    st.write(
        f"- {item['produk']} ({item['jumlah']}x) : {rupiah(item['subtotal'])}"
    )

  # Hitung total semua barang dan potong diskon
  total_belanja = sum(item["subtotal"] for item in st.session_state.pesanan)
  diskon = 2000
  grand_total = max(0, total_belanja - diskon)

  st.info(f"Happy Diskon Setiap Bulan: Potongan {rupiah(diskon)} !!!")
  st.write(f"Total Belanja: {rupiah(total_belanja)}")
  st.write(f"Diskon: {rupiah(diskon)}")
  st.markdown(f"### **Grand Total Bayar: {rupiah(grand_total)}**")

st.write("---")

# Tombol untuk menyimpan data, mencetak nota, serta menampilkan grafik
if st.button("Simpan"):
  if st.session_state.pesanan:
    df = pd.DataFrame(st.session_state.pesanan)

    # Simpan ke file pesanan.csv
    df.to_csv("pesanan.csv", index=False)
    st.success(
        "Data pesanan berhasil disimpan ke file 'pesanan.csv' dan siap"
        " diolah!"
    )

    # ------------------- TAMPILAN NOTA TRANSAKSI -------------------
    st.write("### 🧾 NOTA TRANSAKSI BELANJA ###")

    # Membuat kotak bingkai untuk tampilan Nota
    with st.container(border=True):
      st.markdown("### **ELECTRONIC GERAI**")
      st.caption("Jl. Teknologi No 5, Kota Digital | Telp: (021) 87654321")
      st.write("--------------------------------------------------")

      # Informasi Pembeli & Transaksi
      nama_tampil = (
          nama_pelanggan if nama_pelanggan != "" else "Pelanggan General"
      )
      col_a, col_b = st.columns(2)
      with col_a:
        st.write(f"**Waktu** : {waktu_sekarang}")
        st.write(f"**Pelanggan** : {nama_tampil}")
      with col_b:
        st.write(f"**Tipe Pesanan** : {tipe_pesanan}")
        st.write(f"**Pembayaran** : {metode_pembayaran}")

      st.write("--------------------------------------------------")
      st.write("**Rincian Barang:**")

      # Mencetak daftar barang di Nota
      for item in st.session_state.pesanan:
        st.write(
            f"- {item['produk']} x{item['jumlah']} : {rupiah(item['subtotal'])}"
        )

      st.write("--------------------------------------------------")
      st.write(f"Total Belanja : {rupiah(total_belanja)}")
      st.write(f"Diskon : {rupiah(diskon)}")
      st.markdown(f"### **GRAND TOTAL : {rupiah(grand_total)}**")
      st.write("--------------------------------------------------")
      st.caption("~ Terima Kasih Telah Berbelanja di Electronic Gerai ~")

    st.write("---")

    # Tampilkan tabel Pandas
    st.write("### Tabel Rincian Pesanan (Pandas DataFrame) ###")
    st.dataframe(df, hide_index=True)

    # Tampilkan grafik statistik penjualan
    st.write("### Grafik Statistik Jumlah Pembelian Produk ###")
    st.bar_chart(df.set_index("produk")[["jumlah"]])
  else:
    st.warning(
        "Belum ada produk yang dipilih! Silakan tambahkan produk terlebih"
        " dahulu sebelum menyimpan."
    )

# Tombol untuk mengulang dari awal
st.button("Clear", on_click=reset_data)
