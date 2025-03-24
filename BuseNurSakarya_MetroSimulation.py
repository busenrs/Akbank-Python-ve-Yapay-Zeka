from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str, x: float = 0, y: float = 0):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları
        self.x = x  # x koordinatı (A* algoritması için)
        self.y = y  # y koordinatı (A* algoritması için)

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))
        
    def oklid_mesafe(self, diger_istasyon: 'Istasyon') -> float:
        """İki istasyon arasındaki Öklid mesafesini hesaplar"""
        return ((self.x - diger_istasyon.x) ** 2 + (self.y - diger_istasyon.y) ** 2) ** 0.5

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str, x: float = 0, y: float = 0) -> None:
        if idx not in self.istasyonlar:  # Fixed 'id' to 'idx'
            istasyon = Istasyon(idx, ad, hat, x, y)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """BFS algoritması kullanarak en az aktarmalı rotayı bulur
        
        Bu fonksiyonu tamamlayın:
        1. Başlangıç ve hedef istasyonların varlığını kontrol edin
        2. BFS algoritmasını kullanarak en az aktarmalı rotayı bulun
        3. Rota bulunamazsa None, bulunursa istasyon listesi döndürün
        """
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        
        # BFS algoritması için kuyruk oluşturma
        kuyruk = deque([(baslangic, [baslangic])])
        ziyaret_edildi = {baslangic}
        
        while kuyruk:
            # Kuyruğun başındaki istasyonu ve rotayı al
            guncel_istasyon, rota = kuyruk.popleft()
            
            # Hedef istasyona ulaşıldıysa rotayı döndür
            if guncel_istasyon == hedef:
                return rota
            
            # Komşu istasyonları keşfet
            for komsu, _ in guncel_istasyon.komsular:
                if komsu not in ziyaret_edildi:
                    # Yeni rotayı oluştur ve kuyruğa ekle
                    yeni_rota = rota + [komsu]
                    kuyruk.append((komsu, yeni_rota))
                    ziyaret_edildi.add(komsu)
        
        # Rota bulunamadıysa None döndür
        return None

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """A* algoritması kullanarak en hızlı rotayı bulur
        
        Bu fonksiyonu tamamlayın:
        1. Başlangıç ve hedef istasyonların varlığını kontrol edin
        2. A* algoritmasını kullanarak en hızlı rotayı bulun
        3. Rota bulunamazsa None, bulunursa (istasyon_listesi, toplam_sure) tuple'ı döndürün
        """
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        
        # A* algoritması için öncelik kuyruğu oluşturma
        # (f_score, istasyon_id, istasyon, rota, g_score)
        # f_score = g_score (gerçek maliyet) + h_score (tahmini maliyet)
        # g_score = başlangıçtan şimdiye kadar geçen süre
        # h_score = şimdiden hedefe tahmini süre (Öklid mesafesi)
        
        # Başlangıç düğümü için f_score = 0 + h_score
        h_score = baslangic.oklid_mesafe(hedef)
        pq = [(h_score, id(baslangic), baslangic, [baslangic], 0)]
        ziyaret_edildi = set()
        
        while pq:
            # En düşük f_score'a sahip rotayı al
            _, _, guncel_istasyon, rota, g_score = heapq.heappop(pq)
            
            # Hedef istasyona ulaşıldıysa rotayı ve toplam süreyi döndür
            if guncel_istasyon == hedef:
                return (rota, g_score)
            
            # İstasyon daha önce ziyaret edildiyse atla
            istasyon_id = id(guncel_istasyon)
            if istasyon_id in ziyaret_edildi:
                continue
            
            ziyaret_edildi.add(istasyon_id)
            
            # Komşu istasyonları keşfet
            for komsu, sure in guncel_istasyon.komsular:
                if id(komsu) not in ziyaret_edildi:
                    # Yeni rotayı ve g_score'u hesapla
                    yeni_rota = rota + [komsu]
                    yeni_g_score = g_score + sure
                    
                    # Hat değişimi varsa ek süre ekle (aktarma süresi)
                    if len(rota) > 0 and rota[-1].hat != komsu.hat:
                        # Aktarma süresi olarak 2 dakika ekleyelim
                        yeni_g_score += 2
                    
                    # Heuristik (h_score) hesapla - Öklid mesafesi
                    h_score = komsu.oklid_mesafe(hedef)
                    
                    # f_score = g_score + h_score
                    f_score = yeni_g_score + h_score
                    
                    # Öncelik kuyruğuna ekle
                    heapq.heappush(pq, (f_score, id(komsu), komsu, yeni_rota, yeni_g_score))
        
        # Rota bulunamadıysa None döndür
        return None

# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme (x, y koordinatları ile)
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat", 50, 50)
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat", 40, 60)
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat", 30, 70)
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat", 20, 80)
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat", 60, 40)
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat", 50, 50)  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat", 60, 60)
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat", 70, 70)
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat", 10, 60)
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat", 30, 70)  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat", 70, 70)  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat", 80, 80)
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    
    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Rota formatını iyileştiren yardımcı fonksiyon
    def rota_formatla(rota):
        formatted_rota = []
        prev_hat = None
        
        for istasyon in rota:
            if prev_hat and istasyon.hat != prev_hat:
                formatted_rota.append(f"{istasyon.ad} ({istasyon.hat})")
            else:
                formatted_rota.append(istasyon.ad)
            prev_hat = istasyon.hat
            
        return " -> ".join(formatted_rota)
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", rota_formatla(rota))
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", rota_formatla(rota))
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", rota_formatla(rota))
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", rota_formatla(rota))
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", rota_formatla(rota))
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", rota_formatla(rota))
