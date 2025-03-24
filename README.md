# Sürücüsüz Metro Simülasyonu (Rota Optimizasyonu)

Bu proje, bir metro ağında iki istasyon arasındaki en hızlı ve en az aktarmalı rotaları bulan bir simülasyon uygulamasıdır. Proje, graf veri yapısını kullanarak metro ağını modellemekte ve farklı algoritmaları uygulayarak optimum rotaları hesaplamaktadır.

## Kullanılan Teknolojiler ve Kütüphaneler

- **Python**: Projenin ana programlama dili
- **collections.defaultdict**: Varsayılan değerli sözlük yapısı için kullanılmıştır. Hat bilgilerini saklamak için kullanılmıştır.
- **collections.deque**: BFS algoritması için çift uçlu kuyruk yapısı sağlar. FIFO (First In First Out) prensibiyle çalışır.
- **heapq**: A* algoritması için öncelik kuyruğu (priority queue) yapısı sağlar. En düşük maliyetli elemanı öncelikli olarak çıkarmak için kullanılır.
- **typing**: Tip belirteçleri (type hints) için kullanılmıştır. Kodun okunabilirliğini ve hata ayıklamayı kolaylaştırır.

## Algoritmaların Çalışma Mantığı

### BFS (Breadth-First Search) Algoritması

BFS algoritması, grafikte bir başlangıç noktasından başlayarak, tüm komşu düğümleri ziyaret eden ve ardından bu komşuların komşularını ziyaret eden bir arama algoritmasıdır. Bu projede, en az aktarmalı rotayı bulmak için kullanılmıştır.

**Çalışma Adımları:**
1. Başlangıç istasyonunu kuyruğa ekle ve ziyaret edildi olarak işaretle
2. Kuyruk boş olana kadar:
   - Kuyruğun başındaki istasyonu ve rotayı al
   - Eğer bu istasyon hedef istasyonsa, rotayı döndür
   - Tüm komşu istasyonları kontrol et:
     - Eğer komşu daha önce ziyaret edilmediyse, yeni rotayı oluştur ve kuyruğa ekle
     - Komşuyu ziyaret edildi olarak işaretle

BFS algoritması, en kısa yolu (düğüm sayısı açısından) garanti eder. Bu nedenle, en az aktarmalı rotayı bulmak için idealdir, çünkü her istasyon bir düğüm olarak temsil edilir ve en az düğüm sayısına sahip yol, en az aktarmalı rotayı verir.

### A* Algoritması

A* algoritması, en kısa yolu bulmak için kullanılan bir arama algoritmasıdır. Dijkstra algoritmasının bir uzantısıdır ve hedef düğüme olan tahmini mesafeyi (sezgisel) kullanarak daha verimli çalışır. Bu projede, en hızlı rotayı bulmak için kullanılmıştır.

**Çalışma Adımları:**
1. Başlangıç istasyonunu öncelik kuyruğuna ekle (f_score = g_score + h_score)
   - g_score: Başlangıçtan şimdiye kadar geçen süre (başlangıçta 0)
   - h_score: Şimdiden hedefe tahmini süre (Öklid mesafesi)
2. Öncelik kuyruğu boş olana kadar:
   - En düşük f_score'a sahip istasyonu ve rotayı al
   - Eğer bu istasyon hedef istasyonsa, rotayı ve toplam süreyi döndür
   - İstasyon daha önce ziyaret edildiyse, atla
   - İstasyonu ziyaret edildi olarak işaretle
   - Tüm komşu istasyonları kontrol et:
     - Yeni rotayı ve g_score'u hesapla (geçen süre)
     - Hat değişimi varsa ek süre ekle (aktarma süresi)
     - h_score'u hesapla (Öklid mesafesi)
     - f_score = g_score + h_score
     - Komşuyu öncelik kuyruğuna ekle (öncelik = f_score)

A* algoritması, en düşük maliyetli yolu garanti eder. Bu projede, maliyet seyahat süresidir ve hat değişimleri için ek süre eklenir. Öklid mesafesi heuristiği, algoritmanın hedef istasyona doğru daha verimli bir şekilde ilerlemesini sağlar. Bu nedenle, en hızlı rotayı bulmak için idealdir.

### Neden Bu Algoritmaları Kullandık?

- **BFS**: En az aktarmalı rotayı bulmak için BFS kullanılmıştır çünkü BFS, düğüm sayısı açısından en kısa yolu garanti eder. Metro ağında, her istasyon bir düğüm olarak temsil edildiğinden, en az düğüm sayısına sahip yol, en az aktarmalı rotayı verir.

- **A***: En hızlı rotayı bulmak için A* kullanılmıştır çünkü A*, en düşük maliyetli yolu garanti eder. Metro ağında, maliyet seyahat süresidir ve hat değişimleri için ek süre eklenir. A* algoritması, bu maliyetleri dikkate alarak en hızlı rotayı bulur.

## Örnek Kullanım ve Test Sonuçları

Proje, üç farklı senaryo için test edilmiştir:

### Senaryo 1: AŞTİ'den OSB'ye

```
En az aktarmalı rota: AŞTİ -> Kızılay -> Kızılay (Kırmızı Hat) -> Ulus -> Demetevler -> OSB
En hızlı rota (27 dakika): AŞTİ -> Kızılay -> Kızılay (Kırmızı Hat) -> Ulus -> Demetevler -> OSB
```

### Senaryo 2: Batıkent'ten Keçiören'e

```
En az aktarmalı rota: Batıkent -> Demetevler -> Gar -> Keçiören
En hızlı rota (21 dakika): Batıkent -> Demetevler -> Gar -> Keçiören
```

### Senaryo 3: Keçiören'den AŞTİ'ye

```
En az aktarmalı rota: Keçiören -> Gar -> Gar (Mavi Hat) -> Sıhhiye -> Kızılay -> AŞTİ
En hızlı rota (21 dakika): Keçiören -> Gar -> Gar (Mavi Hat) -> Sıhhiye -> Kızılay -> AŞTİ
```

## Projeyi Geliştirme Fikirleri

1. **Görselleştirme Ekleme**: Metro ağını ve bulunan rotaları görsel olarak göstermek için bir arayüz eklenebilir. Bu, kullanıcıların rotaları daha iyi anlamasına yardımcı olabilir.

2. **Gerçek Zamanlı Veri Entegrasyonu**: Gerçek metro sistemlerinden alınan verilerle (örneğin, tren gecikmeleri, istasyon yoğunluğu) simülasyonu güncelleyerek daha gerçekçi sonuçlar elde edilebilir.

3. **Çoklu Kriter Optimizasyonu**: Kullanıcıların farklı kriterlere göre rota seçebilmesi sağlanabilir. Örneğin, en hızlı, en az aktarmalı, en az yürüme mesafeli veya bunların bir kombinasyonu.

4. **Mobil Uygulama**: Simülasyonu bir mobil uygulamaya dönüştürerek, kullanıcıların gerçek zamanlı olarak en iyi rotaları bulmasına yardımcı olunabilir.

5. **Daha Büyük ve Karmaşık Metro Ağları**: Daha fazla hat ve istasyon içeren büyük metro ağları eklenerek, algoritmaların performansı test edilebilir ve iyileştirilebilir.

6. **Yolcu Simülasyonu**: Metro ağındaki yolcu hareketlerini simüle ederek, istasyon ve hat yoğunluklarını tahmin etmek ve buna göre rota önerileri sunmak mümkün olabilir.
