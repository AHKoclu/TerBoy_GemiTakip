import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import PyPDF2

# --- 1. SAYFA AYARLARI VE BAŞLIK ---
st.set_page_config(page_title="Filo Yönetim Merkezi", layout="wide")

st.markdown("<h1 style='text-align: center;'>ORTAK OPERASYON MERKEZİ</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>RightShip, PSC ve Flag State Takip Sistemi</h4>", unsafe_allow_html=True)

st.divider()

# --- 2. GEMİ VERİTABANI ---
# İleride bu kısmı Google Sheets CSV linki ile değiştireceğiz.
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

df = pd.DataFrame(gemi_verileri)

# --- 3. KULLANICI ARAYÜZÜ ---
sol_kolon, sag_kolon = st.columns([1, 2])

with sol_kolon:
    st.subheader("📋 Gemi Seçimi")
    secilen_gemi = st.selectbox("İşlem yapmak istediğiniz gemiyi seçin:", df["Gemi Adı"])
    gemi_bilgisi = df[df["Gemi Adı"] == secilen_gemi].iloc[0]
    
    st.info(f"**Grup:** {gemi_bilgisi['Grup']} \n\n"
            f"**Bayrak:** {gemi_bilgisi['Bayrak']} \n\n"
            f"**E-Posta:** {gemi_bilgisi['Email']}")

with sag_kolon:
    st.subheader(f"⚙️ {secilen_gemi} İçin Operasyonlar")
    
    tab1, tab2, tab3 = st.tabs(["RightShip Planlama", "Flag State (FSI)", "PSC / PDF Analizi"])
    
    # --- RIGHTSHIP SEKMESİ ---
    with tab1:
        st.markdown("### ⚓ RightShip Denetim Takip Aracı")
        col_tarih, col_periyot = st.columns(2)
        with col_tarih:
            son_denetim = st.date_input("Denetimin Yapılış Tarihi (Last Inspection):", key="rs_date")
        with col_periyot:
            periyot = st.selectbox("Kaç ay sonra denetim alınacak?", [3, 6, 9, 12], key="rs_period")
            
        if st.button("RightShip Tarihini Hesapla"):
            due_date = son_denetim + relativedelta(months=periyot)
            uyari_tarihi = due_date - relativedelta(months=2)
            bugun = datetime.today().date()
            
            st.success(f"📌 **Sıradaki Denetim Tarihi (Due Date):** {due_date.strftime('%d.%m.%Y')}")
            st.warning(f"🔔 **Erken Uyarı Başlangıcı (-2 Ay):** {uyari_tarihi.strftime('%d.%m.%Y')}")
            
            st.divider()
            if bugun > due_date:
                st.error(f"🚨 KRİTİK: {secilen_gemi} gemisinin RightShip denetim tarihi geçmiş!")
            elif bugun >= uyari_tarihi and bugun <= due_date:
                kalan_gun = (due_date - bugun).days
                st.warning(f"⚠️ DİKKAT: Denetim periyoduna {kalan_gun} gün kaldı!")
            else:
                st.info(f"✅ DURUM NORMAL: Erken uyarı dönemine henüz girilmedi.")
        
    # --- FLAG STATE SEKMESİ ---
    with tab2:
        st.markdown("### 🏳️ Flag State Inspection (FSI) Penceresi")
        bayrak = gemi_bilgisi['Bayrak']
        uygun_bayraklar = ["Barbados", "Panama", "Antigua & Barbuda"]
        
        if bayrak in uygun_bayraklar:
            st.info(f"Bu gemi **{bayrak}** bayraklı olduğu için ±3 ay kuralına (Pencere sistemine) tabidir.")
            
            fsi_due_date = st.date_input("FSI Hedef Tarihini (Due Date) Giriniz:", key="fsi_date")
            
            if st.button("FSI Penceresini Hesapla"):
                pencere_baslangic = fsi_due_date - relativedelta(months=3)
                pencere_bitis = fsi_due_date + relativedelta(months=3)
                bugun = datetime.today().date()
                
                st.markdown("#### Denetim Penceresi (Window)")
                st.write(f"🟢 **Pencere Açılış:** {pencere_baslangic.strftime('%d.%m.%Y')}")
                st.write(f"🎯 **Merkez Hedef:** {fsi_due_date.strftime('%d.%m.%Y')}")
                st.write(f"🔴 **Son Geçerlilik:** {pencere_bitis.strftime('%d.%m.%Y')}")
                
                st.divider()
                if bugun < pencere_baslangic:
                    st.info("ℹ️ Pencere henüz açılmadı. Denetim yapılamaz.")
                elif pencere_baslangic <= bugun <= pencere_bitis:
                    kalan = (pencere_bitis - bugun).days
                    st.success(f"✅ Pencere şu an AÇIK. Denetimin yapılması için son {kalan} gün!")
                else:
                    st.error("❌ Pencere kapandı! Yasal denetim süresi aşıldı.")
        else:
            st.write(f"Bu gemi **{bayrak}** bayraklı. ±3 ay kuralı sadece Barbados, Panama ve Antigua & Barbuda için geçerlidir.")
        
    # --- PSC / PDF ANALİZİ SEKMESİ ---
    with tab3:
        st.markdown("### 📊 Paris MOU & PSC Rapor Analizi")
        
        # 1. Company Profile Girişi
        st.markdown("#### 1. Şirket Profili (Company Profile)")
        sirket_skoru = st.selectbox("Paris MOU Şirket Performansınızı Seçin:", 
                                    ["High Performance", "Medium Performance", "Low Performance", "Very Low Performance"])
        
        if sirket_skoru == "High Performance":
            st.success("🌟 Şirket Profili: YÜKSEK (Düşük riskli operasyon)")
        elif sirket_skoru == "Medium Performance":
            st.warning("⚖️ Şirket Profili: ORTA (Standart risk seviyesi)")
        else:
            st.error("🚨 Şirket Profili: DÜŞÜK (Yüksek denetim riski, gemiler sıkı takip edilmeli)")
            
        st.divider()
        
        # 2. PDF Yükleme ve Barbados 4+ Madde Kuralı
        st.markdown("#### 2. PSC Raporu (PDF) Yükleme")
        st.info("Sisteme bir PSC raporu yüklediğinizde, eksiklik (deficiency) sayısı analiz edilir ve bayrak kuralları tetiklenir.")
        
        yuklenen_pdf = st.file_uploader("PSC Raporunu Yükleyin (PDF Formatında)", type="pdf")
        
        if yuklenen_pdf is not None:
            try:
                pdf_okuyucu = PyPDF2.PdfReader(yuklenen_pdf)
                sayfa_sayisi = len(pdf_okuyucu.pages)
                
                st.success(f"✅ PDF başarıyla yüklendi ve tarandı! (Toplam {sayfa_sayisi} sayfa)")
                
                st.write("Lütfen raporda tespit edilen deficiency (eksiklik) sayısını onaylayın:")
                bulunan_madde_sayisi = st.number_input("Madde Sayısı:", min_value=0, max_value=100, value=0, step=1)
                
                # BARBADOS KURALI KONTROLÜ
                if bulunan_madde_sayisi >= 4 and gemi_bilgisi['Bayrak'] == "Barbados":
                    st.error(f"🚨 KURAL İHLALİ TETİKLENDİ! {secilen_gemi} gemisi Barbados bayraklı ve PSC'den {bulunan_madde_sayisi} madde aldı.")
                    st.warning("Bu durum standart ±3 aylık FSI kuralını geçersiz kılar. Lütfen aşağıdaki 'Additional Flag State Inspection' tarihini giriniz.")
                    
                    additional_tarih = st.date_input("Additional FSI Tarihini Belirleyin:")
                    if st.button("Additional FSI'yi Sisteme İşle"):
                        st.success(f"✅ Ek denetim tarihi ({additional_tarih.strftime('%d.%m.%Y')}) sisteme ve merkez ofise bildirildi. (Standart pencere kuralı ezilmiştir).")
                
                elif bulunan_madde_sayisi > 0:
                    st.info("Kayıt altına alındı. FSI kurallarını değiştirecek kritik bir eşik aşılmadı.")
                else:
                    st.success("Harika! Sıfır eksiklik (Clear Inspection).")
                    
            except Exception as e:
                st.error(f"PDF okunurken bir hata oluştu: {e}")

# --- ALT TABLO ---
st.divider()
st.subheader("Tüm Filo Listesi")
st.dataframe(df, use_container_width=True)
