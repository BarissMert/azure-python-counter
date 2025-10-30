Python ile Azure App Service ve PostgreSQL Projesi

Bu proje, Azure'da Python öğrenme yolculuğumun bir parçası olarak oluşturulmuştur. Basit bir Flask web uygulaması, Azure App Service üzerinde çalışır ve Azure Database for PostgreSQL'e bağlanarak bir ziyaretçi sayacını yönetir.

Özellikler

Ana Sayfa (/): Siteyi o ana kadar kaç kişinin ziyaret ettiğini gösteren bir sayaç.

Reset Sayfası (/reset): Veritabanındaki sayacı sıfırlamak için bir buton içerir.

Sunucusuz Mimari: Kod, gunicorn ile Azure App Service üzerinde çalışır.

Yönetilen Veritabanı: Sayaç verisi, Azure Database for PostgreSQL Flexible Server'da saklanır.

Kurulum ve Dağıtım

Bu proje, doğrudan Azure CLI kullanılarak Azure'a dağıtılmak üzere tasarlanmıştır.

Gereksinimler:

app.py (Flask uygulaması)

requirements.txt (Gerekli Python kütüphaneleri: flask, gunicorn, psycopg2-binary)

Dağıtım (Azure App Service):

# (Azure'a 'az login' ile giriş yaptıktan sonra)
az webapp up --name <benzersiz-uygulama-adi>


Veritabanı (Azure PostgreSQL):
Uygulama, Azure App Service'in "Uygulama Ayarları" (Application Settings) bölümünde tanımlanmış DATABASE_URL adında bir ortam değişkenine (environment variable) ihtiyaç duyar.

Bu değişkenin formatı şu şekildedir:
postgresql://USER:PASSWORD@HOST/DATABASE?sslmode=require