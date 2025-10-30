import os
import psycopg2
# Gerekli Flask modüllerini içe aktarıyoruz
from flask import Flask, redirect, url_for, request

#deneme

# Uygulamayı oluştur
app = Flask(__name__)

# Veritabanı bağlantı fonksiyonu
def get_db_connection():
    conn_string = os.environ.get("DATABASE_URL")
    conn = psycopg2.connect(conn_string)
    return conn

# --- ANA SAYFA ---
# Mantık: DB'den sayıyı (X) oku, ekranda X'i göster.
# Sonra DB'yi X+1 olarak güncelle.
@app.route("/")
def index():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("CREATE TABLE IF NOT EXISTS visitors (count INT);")
        cur.execute("SELECT count FROM visitors;")
        row = cur.fetchone()

        if row is None:
            # DB'ye 1 yaz, ekranda 0 göster (ilk ziyaret)
            cur.execute("INSERT INTO visitors (count) VALUES (1);")
            current_count = 0
        else:
            # DB'den X'i oku, ekranda X'i göster
            current_count = row[0]
            # DB'yi bir sonraki ziyaret için X+1 yap
            new_count = current_count + 1
            cur.execute("UPDATE visitors SET count = %s;", (new_count,))
        
        conn.commit()
        cur.close()

        # HTML çıktısı: Sadece sayaç yazısı
        return f"""
        <html>
            <head>
                <title>Azure Sayaç Projesi</title>
                <!-- Sayfanın 30 saniyede bir yenilenmesini sağlar -->
                <meta http-equiv="refresh" content="30">
            </head>
            <body style="font-family: Arial; text-align: center; padding-top: 100px; font-size: 1.5em;">
                <h1>Bu site veritabanından gelen bilgiye göre {current_count} kez ziyaret edildi!</h1>
            </body>
        </html>
        """

    except Exception as ex:
        return f"Bir hata oluştu: {ex}"
    
    finally:
        if conn is not None:
            conn.close()


# --- RESET SAYFASI (PRG MODELİ UYGULANDI) ---
@app.route("/reset", methods=["GET", "POST"])
def reset_counter():
    
    # --- POST İSTEĞİ (Butona basıldığında) ---
    if request.method == "POST":
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # MANTIK DÜZELTMESİ:
            # Ana sayfada "0" görmek için DB'yi 0'a ayarlamalıyız.
            # (Sizin kodunuzda 1 yazıyordu, bu mantık hatasıydı)
            cur.execute("UPDATE visitors SET count = 0;") 
            conn.commit()
            cur.close()
            
            # --- !! İŞTE ÇÖZÜM BURADA !! ---
            # HTML döndürmek yerine, tarayıcıyı yönlendiriyoruz.
            # Adrese "?success=true" parametresini ekliyoruz.
            return redirect(url_for("reset_counter", success="true")) 

        except Exception as ex:
            return f"Sıfırlama sırasında bir hata oluştu: {ex}"
        finally:
            if conn is not None:
                conn.close()
    
    # --- GET İSTEĞİ (Sayfa normal açıldığında veya yönlendirme sonrası) ---
    success_message = "" # Mesajı varsayılan olarak boş tut
    
    # Adreste "?success=true" parametresi var mı diye kontrol et
    if request.args.get("success") == "true":
        success_message = "<p style='color: green;'><strong>Sayaç başarıyla sıfırlandı!</strong></p>"

    # HTML Çıktısı: Sadece buton (ve gerekirse başarı mesajı)
    return f"""
    <html>
        <head><title>Sayacı Sıfırla</title></head>
        <body style="font-family: Arial; text-align: center; padding-top: 100px;">
            
            <!-- Başarı mesajı sadece yönlendirme sonrası görünür -->
            {success_message}
            
            <!-- Formun kendisi -->
            <form action="" method="POST">
                <button type="submit" style="font-size: 1.2em; padding: 10px 20px;">SAYACI ŞİMDİ SIFIRLA</button>
            </form>
            
        </body>
    </html>
    """

