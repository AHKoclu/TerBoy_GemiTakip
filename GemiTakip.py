import streamlit as st
import pandas as pd
from datetime import datetime

# 1. SAYFA AYARLARI VE LOGOLAR
# Sayfanın geniş olmasını ve başlığını ayarlıyoruz
st.set_page_config(page_title="Filo Yönetim Merkezi", layout="wide")

# Logoları ve Başlığı yan yana dizmek için kolonlar oluşturuyoruz
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    # SPARK logosu (Senin yüklediğin dosya adıyla)
    try:
        st.image("Spark logo.jpeg", width=250)
    except FileNotFoundError:
        st.error("Spark logo.jpeg dosyası bulunamadı. Lütfen kodla aynı klasöre koyun.")

with col2:
    st.markdown("<h1 style='text-align: center;'>ORTAK OPERASYON MERKEZİ</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>RightShip, PSC ve Flag State Takip Sistemi</p>", unsafe_allow_html=True)

with col3:
    # AQMARIS logosu (Senin yüklediğin dosya adıyla)
    try:
        st.image("image_53b0e3.png", width=150)
    except FileNotFoundError:
        st.error("image_53b0e3.png dosyası bulunamadı. Lütfen kodla aynı klasöre koyun.")

st.divider() # Araya bir çizgi çekiyoruz

# 2. GEMİ VERİTABANI (Gönderdiğin Listeye Göre)
# Bu verileri ileride Excel'den veya bir veritabanından da çekebiliriz.
gemi_verileri = [
    {"Grup": "Spark", "Gemi Adı": "Beam", "Bayrak": "Barbados", "Email": "beam@infinitymail.eu"},
    {"Grup": "Spark", "Gemi Adı": "GIFT", "Bayrak": "Barbados", "Email": "gift@infinitymail.eu"},
    {"Grup": "Spark", "Gemi Adı": "just", "Bayrak": "Panama", "Email": "just@infinitymail.eu"},
    {"Grup": "Spark", "Gemi Adı": "IDON", "Bayrak": "Barbados", "Email": "idon@infinitymail.eu"},
    {"Grup": "Spark", "Gemi Adı": "Kronos", "Bayrak": "Barbados", "Email": "kronos@infinitymail.eu"},
    {"Grup": "Spark", "Gemi Adı": "April", "Bayrak": "Antigua & Barbuda", "Email": "april@infinitymail.eu"},
    {"Grup": "Spark", "Gemi Adı": "flat", "Bayrak": "Barbados", "Email": "flat@infinitymail.eu"},
    {"Grup": "Spark", "Gemi Adı": "canal", "Bayrak": "Barbados", "Email": "canal@infinitymail.eu"},
    {"Grup": "Spark", "Gemi Adı": "comet", "Bayrak": "Barbados", "Email": "comet@infinitymail.eu"},
    {"Grup": "Spark", "Gemi Adı": "dali", "Bayrak": "Barbados", "Email": "dali@vesselsat.com"},
    {"Grup": "Spark", "Gemi Adı": "Dodo", "Bayrak": "Panama", "Email": "dodo@skyfile.com"},
    {"Grup": "Spark", "Gemi Adı": "dream", "Bayrak": "Barbados", "Email": "dream@infinitymail.eu"},
    {"Grup": "Spark", "Gemi Adı": "faun", "Bayrak": "Barbados", "Email": "faun@infinitymail.eu"},
    {"Grup": "Spark", "Gemi Adı": "laker", "Bayrak": "Panama", "Email": "laker@infinitymail.eu"},
    {"Grup": "Spark", "Gemi Adı": "ares", "Bayrak": "Panama", "Email": "mvares@skyfile.com"},
    {"Grup": "Aqmaris", "Gemi Adı": "Zeynep", "Bayrak": "Barbados", "Email": "zeynep@infinitymail.eu"},
    {"Grup": "Aqmaris", "Gemi Adı": "Emine", "Bayrak": "Panama", "Email": "emine@infinitymail.eu"}
]

# Veriyi tabloya çeviriyoruz (Pandas DataFrame)
df = pd.DataFrame(gemi_verileri)

# 3. KULLANICI ARAYÜZÜ BÖLÜMÜ
sol_kolon, sag_kolon = st.columns([1, 2])

with sol_kolon:
    st.subheader("📋 Gemi Seçimi")
    # Kullanıcı listeden bir gemi seçiyor
    secilen_gemi = st.selectbox("İşlem yapmak istediğiniz gemiyi seçin:", df["Gemi Adı"])
    
    # Seçilen geminin bilgilerini filtreleyip gösteriyoruz
    gemi_bilgisi = df[df["Gemi Adı"] == secilen_gemi].iloc[0]
    
    st.info(f"**Grup:** {gemi_bilgisi['Grup']} \n\n"
            f"**Bayrak:** {gemi_bilgisi['Bayrak']} \n\n"
            f"**E-Posta:** {gemi_bilgisi['Email']}")

with sag_kolon:
    st.subheader(f"⚙️ {secilen_gemi} İçin Operasyonlar")
    
    # İleride buraya algoritmalarımızı ekleyeceğiz
    tab1, tab2, tab3 = st.tabs(["RightShip Planlama", "Flag State (FSI)", "PSC / PDF Analizi"])
    
    with tab1:
        st.write("Buraya RightShip için 3, 6, 9, 12 ay tarih öteleme ve 2 ay uyarı sistemini ekleyeceğiz.")
        
    with tab2:
        st.write("Buraya +- 3 ay 'due date' kuralını ekleyeceğiz.")
        
    with tab3:
        st.write("Buraya 4 madde kuralı ve ek denetim tarihlerini yükleme modülünü ekleyeceğiz.")

# Tabloyu en altta genel bakış olarak gösteriyoruz
st.subheader("Tüm Filo Listesi")
st.dataframe(df, use_container_width=True)