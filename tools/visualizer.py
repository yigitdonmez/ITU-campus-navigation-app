import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# ==========================================
# AYARLAR: NOKTALARI (NODES) TAŞIMA KUMANDASI
# ==========================================

# 1. ÖLÇEKLEME (ZOOM)
# Harita resminle bizim 2000'lik koordinat sistemimiz uyuşmayabilir.
# Eğer noktalar haritaya göre çok KÜÇÜK kalıyorsa (bir araya toplanmışsa) -> Artır (Örn: 1.5)
# Eğer noktalar haritaya göre çok DAĞINIKSA (dışarı taşıyorsa) -> Küçült (Örn: 0.8)
NODE_SCALE = 1.0

# 2. KAYDIRMA (SHIFT)
# Noktaları haritanın üzerine denk getirmek için sağa/sola/yukarı/aşağı it.
# Noktalar haritanın SOLUNDA kalıyorsa -> X'i ARTIR (+)
# Noktalar haritanın YUKARISINDA kalıyorsa -> Y'yi ARTIR (+)
NODE_SHIFT_X = 0
NODE_SHIFT_Y = 0

# Harita dosya adı (Değiştiyse burayı güncelle)
MAP_FILENAME = 'Campus_8K.jpg' 

# ==========================================

def visualize():
    fig, ax = plt.subplots(figsize=(14, 10))

    # 1. Harita Resmini Yükle (SABİT)
    try:
        img = mpimg.imread(MAP_FILENAME)
        # Resmin kendi boyutlarını (pixel) al
        img_h, img_w, _ = img.shape
        
        # Haritayı olduğu gibi (0,0)'dan başlayarak çiz. Hiçbir extent oynaması yapmıyoruz.
        ax.imshow(img) 
        
        # Grafik sınırlarını resim boyutuna eşitle
        ax.set_xlim(0, img_w)
        ax.set_ylim(img_h, 0) # Y ekseni ters (0 yukarıda)
        
    except FileNotFoundError:
        print(f"HATA: {MAP_FILENAME} bulunamadi!")
        return

    # 2. Nodelari Oku, ÖLÇEKLE ve KAYDIR
    nodes = {}
    try:
        with open('nodes.txt', 'r') as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 4:
                    id = int(parts[0])
                    # Orijinal koordinatları al
                    raw_x = int(parts[2])
                    raw_y = int(parts[3])
                    
                    # === FORMÜL: Önce Ölçekle, Sonra Kaydır ===
                    x = (raw_x * NODE_SCALE) + NODE_SHIFT_X
                    y = (raw_y * NODE_SCALE) + NODE_SHIFT_Y
                    
                    nodes[id] = (x, y)
                    
                    # Binalar
                    if id < 100: 
                        ax.plot(x, y, 'bo', markersize=6, markeredgecolor='white', zorder=3)
                        ax.text(x, y-15, str(id), color='white', fontsize=9, fontweight='bold', 
                                 bbox=dict(facecolor='black', alpha=0.6, pad=1), ha='center', zorder=4)
                    else: # Kavşaklar
                        ax.plot(x, y, 'r+', markersize=4, alpha=0.7, zorder=2)

    except FileNotFoundError:
        print("nodes.txt bulunamadi.")
        return


    # 4. Rotayı (path.txt) Ciz
    try:
        path_x = []
        path_y = []
        with open('path.txt', 'r') as f:
            for line in f:
                parts = line.split()
                # Rota noktalarını da aynı formülle dönüştür
                raw_px = int(parts[1])
                raw_py = int(parts[2])
                
                px = (raw_px * NODE_SCALE) + NODE_SHIFT_X
                py = (raw_py * NODE_SCALE) + NODE_SHIFT_Y
                
                path_x.append(px)
                path_y.append(py)
        
        if path_x:
            ax.plot(path_x, path_y, color='#39FF14', linewidth=5, alpha=0.9, zorder=5)
            ax.plot(path_x, path_y, color='black', linewidth=7, alpha=0.3, zorder=4.5)
            ax.plot(path_x[-1], path_y[-1], 'go', markersize=10, markeredgecolor='white', label="Baslangic", zorder=6)
            ax.plot(path_x[0], path_y[0], 'ro', markersize=10, markeredgecolor='white', label="Bitis", zorder=6)

    except FileNotFoundError:
        pass

    plt.title(f"Ayar Modu: SCALE={NODE_SCALE}, X_SHIFT={NODE_SHIFT_X}, Y_SHIFT={NODE_SHIFT_Y}")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    visualize()