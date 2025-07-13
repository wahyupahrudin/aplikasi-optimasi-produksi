import streamlit as st
from pulp import LpMaximize, LpProblem, LpVariable, lpSum
import matplotlib.pyplot as plt
import numpy as np

st.title("🔧 Aplikasi Optimasi Produksi (Linear Programming)")

st.markdown("""
Aplikasi ini membantu memaksimalkan keuntungan produksi dua produk dengan kendala sumber daya (waktu, bahan baku, tenaga kerja, dll).
""")

st.header("📥 Input Data")

# Input jumlah produk
produk1 = st.text_input("Nama Produk 1", "Produk A")
produk2 = st.text_input("Nama Produk 2", "Produk B")

keuntungan1 = st.number_input(f"Keuntungan per unit {produk1}", value=30)
keuntungan2 = st.number_input(f"Keuntungan per unit {produk2}", value=20)

# Kendala sumber daya
st.subheader("🔧 Kendala Produksi")
waktu1 = st.number_input(f"Waktu per unit {produk1} (jam)", value=2)
waktu2 = st.number_input(f"Waktu per unit {produk2} (jam)", value=1)
total_waktu = st.number_input("Total Waktu Tersedia (jam)", value=100)

bahan1 = st.number_input(f"Bahan per unit {produk1} (kg)", value=1)
bahan2 = st.number_input(f"Bahan per unit {produk2} (kg)", value=1)
total_bahan = st.number_input("Total Bahan Tersedia (kg)", value=80)

if st.button("🔍 Hitung Solusi Optimal"):

    # Definisikan model
    model = LpProblem(name="optimasi-produksi", sense=LpMaximize)

    x = LpVariable(name=produk1, lowBound=0, cat='Continuous')
    y = LpVariable(name=produk2, lowBound=0, cat='Continuous')

    # Fungsi objektif
    model += keuntungan1 * x + keuntungan2 * y, "Total Keuntungan"

    # Kendala
    model += (waktu1 * x + waktu2 * y <= total_waktu, "Kendala Waktu")
    model += (bahan1 * x + bahan2 * y <= total_bahan, "Kendala Bahan")

    # Solve
    model.solve()

    st.subheader("📈 Solusi Optimal")

    st.write(f"Jumlah {produk1}: ", x.value())
    st.write(f"Jumlah {produk2}: ", y.value())
    st.write(f"Total Keuntungan Maksimum: Rp {model.objective.value():,.2f}")

    # Visualisasi area feasible
    st.subheader("📊 Visualisasi Area Feasible")
    x_vals = np.linspace(0, total_waktu / waktu1, 100)
    waktu_line = (total_waktu - waktu1 * x_vals) / waktu2
    bahan_line = (total_bahan - bahan1 * x_vals) / bahan2

    plt.figure(figsize=(8, 5))
    plt.plot(x_vals, waktu_line, label="Kendala Waktu")
    plt.plot(x_vals, bahan_line, label="Kendala Bahan")
    plt.fill_between(x_vals, np.minimum(waktu_line, bahan_line), alpha=0.3)
    plt.xlim(0, max(x_vals))
    plt.ylim(0, max(max(waktu_line), max(bahan_line)))
    plt.xlabel(produk1)
    plt.ylabel(produk2)
    plt.axvline(x.value(), color='red', linestyle='--', label=f'Solusi {produk1}')
    plt.axhline(y.value(), color='green', linestyle='--', label=f'Solusi {produk2}')
    plt.legend()
    st.pyplot(plt)
