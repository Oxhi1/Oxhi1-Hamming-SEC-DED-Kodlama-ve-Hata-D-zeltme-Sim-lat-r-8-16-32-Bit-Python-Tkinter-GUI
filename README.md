#  Hamming SEC-DED Simülatörü (8/16/32 Bit)

Bu proje, **Bursa Teknik Üniversitesi - Bilgisayar Mimarisi** dersi kapsamında geliştirilmiş bir Hamming SEC-DED (Single Error Correcting, Double Error Detecting) kodlama simülatörüdür. Program, kullanıcıdan 8, 16 veya 32 bitlik ikili verileri alır, Hamming kodlamasını uygular, yapay hatalar oluşturur ve bu hataları sendrom analizi ile tespit edip tekli hataları düzeltir.

## Programın nasıl çalıştığını görmek isterseniz ---->>>  https://youtu.be/TDSSuh7kr90

##  Amaç

- Bellekte veri güvenliğini sağlamak için Hamming SEC-DED algoritmasını simüle etmek
- Tekli bit hatalarını otomatik düzeltmek
- Çiftli bit hatalarını tespit etmek
- Kullanıcıya hem ham hem kodlanmış hem de bozulmuş verileri görsel olarak sunmak
- Bit düzeyinde hata oluşturma ve düzeltme işlemlerini interaktif olarak göstermek

---

##  Kullanılan Teknolojiler

- **Python 3**
- **Tkinter** (Kullanıcı Arayüzü için)
- Bit düzeyinde hesaplama ve hata düzeltme algoritmaları

---

##  Nasıl Kullanılır?

1. Uygulamayı başlatmak için Python ile `hammin_simulator.py` dosyasını çalıştırın:
   ```bash
   python hamming_simulator.py
Açılan pencerede:

Veri kutusuna sadece 0 ve 1'lerden oluşan 8, 16 veya 32 bitlik bir veri girin.

“Belleğe Yaz (Kodla)” butonuna tıklayın.

Program, girilen veriyi Hamming SEC-DED algoritması ile kodlayarak belleğe yazar.

Hata oluşturmak için:

"Hangi biti bozmak istersiniz?" kutusuna 1'den N'e kadar bir veya birden fazla bit numarası girin (virgül ile ayırarak, örn: 3,7).

“Yapay Hata Oluştur” butonuna tıklayın.

Bozulan bit(ler) kırmızı olarak vurgulanacaktır.

Hataları analiz etmek için:

“Hata Tespit Et ve Düzelt” butonuna basın.

Eğer tekli hata varsa, program hatayı otomatik olarak düzeltir.

Eğer çiftli hata varsa, program tespiti sağlar ama düzeltme yapmaz.

Sonuçlar açıklama kutusunda ve renkli olarak görsel biçimde gösterilir.

## Teknik Açıklama
Hamming SEC-DED Algoritması
Parity Bitleri (r adet): 2^r >= m + r + 1 formülüne göre hesaplanır (m = veri bit sayısı).

Kodlama:

Her 2ⁿ konumuna parity biti yerleştirilir.

Diğer konumlara veri bitleri yerleştirilir.

P0 pozisyonuna (en başa) genel parity biti eklenir (SEC-DED için).

Sendrom Hesaplama:

Hangi parity bitlerinin uyuşmadığı kontrol edilir.

XOR toplamı, hatalı bitin pozisyonunu verir.

Hata Türleri:

Syndrome = 0 ve parity uyuşuyorsa → Hata yok.

Syndrome ≠ 0 ve parity uyuşmuyorsa → Tekli hata, düzeltilebilir.

Syndrome ≠ 0 ve parity uyumluysa → Çiftli hata, düzeltilemez ama tespit edilir.

