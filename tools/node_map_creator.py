import matplotlib.pyplot as plt
import matplotlib.image as mpimg

MAP_FILENAME = 'Campus_8K.jpg'

# İTÜ Binalar Listesi
NODE_LIST = [
    (1, "Akademik_Kapi"), (2, "Ari_Kapi"), (3, "1773_Kapi"),
    (4, "Rektorluk"), (5, "Mustafa_Inan_Kutuphane"), (6, "Bilgisayar_Bilisim_Fak"), 
    (7, "Elektrik_Elektronik_Fak"), (8, "Insaat_Fakultesi"), (9, "Maden_Fakultesi"), 
    (10, "Kimya_Metalurji_Fak"), (11, "Ucak_Uzay_Fakultesi"), (12, "Gemi_Insaat_Fakultesi"), 
    (13, "Fen_Edebiyat_Fakultesi"), (14, "MED"), (15, "MED_C"), 
    (16, "Yabanci_Diller_Binasi"), (17, "SDKM_Kultur_Merkezi"), (18, "Yemekhane_75_Yil"), 
    (19, "Ogrenci_Isleri"), (20, "Bilgi_Islem_Daire"), (21, "Etiler_Kapisi"), 
    (22, "Deprem_Enstitusu"), (23, "Enerji_Enstitusu"), (24, "Avrasya_Yer_Bilimleri"),
    (25, "Junior_Bee_Kres"), (26, "ARI_Teknokent_1"), (27, "ARI_Teknokent_2"), 
    (28, "ARI_Teknokent_3"), (29, "ARI_Teknokent_4"), (30, "ARI_Teknokent_6"), 
    (31, "Kapali_Spor_Salonu"), (32, "Olimpik_Stadyum"), (33, "Barca_Saha"),
    (34, "Basket_sahalari"), (35, "Olimpik_Havuz"), (36, "Tenis_Kortlari"), 
    (37, "Golet_Yurtlari"), (38, "Vadi_Yurtlari"), (39, "Ayazaga_Kiz_Yurdu"), 
    (40, "Ferhunde_Birkan_Yurdu"), (41, "Gok_Yurdu"), (42, "Mezunlar_Yurdu"), 
    (43, "Yilmaz_Akdoruk_Evi"), (44, "ITU_Camii"), (45, "Gratis"),
    (46, "Sok_Market"), (47, "Migros_Market"), (48, "A101_Market"),
    (49, "Mekansal"), (50, "Selfis"), (51, "Kovan"),
    (52, "FanFan"), (53, "Cajun_Corner"), (54, "Unkapani_Pilavcisi"),
    
    # Kavşaklar (Junctions) - Bunları göz kararı yol ayrımlarına tıkla
    (100, "Kavsak_Akademik_Kapi"), (101, "Kavsak_Ari_Kapi"), (102, "Kavsak_1773_Kapi"),
    (103, "Kavsak_1773_2"), (104, "Kavsak_Vadi"), (105, "Kavsak_Golet_2"),
    (106, "Kavsak_Golet"), (107, "Kavsak_BBF"), (108, "Kavsak_Olimpik_Havuz"),
    (109, "Kavsak_Stadyum"), (110, "Kavsak_Etiler"), (111, "Kavsak_Kiz_Yurtlari"),
    (112, "Kavsak_MED_C"), (113, "Kavsak_Kovan"), (114, "Kavsak_Mustafa_Inan"),
    (115, "Kavsak_Konuk_Evi"), (116, "Kavsak_Insaat_Fak"), (117, "Kavsak_Sok"),
    (118, "Kavsak_Rektorluk"), (119, "Kavsak_SDKM"), (120, "Kavsak_MED"),
    (121, "Kavsak_Fakulteler"), (122, "Kavsak_Rektor_Yolu"), (123, "Kavsak_Stadyum_2")
]

current_index = 0
collected_nodes = []

def save_to_file():
    print("\n--- nodes.txt KAYDEDILIYOR ---")
    with open("nodes.txt", "w") as f:
        for node in collected_nodes:
            f.write(f"{node[0]}   {node[1]}   {node[2]}   {node[3]}\n")
    print("BASARILI! nodes.txt dosyan hazir.")
    plt.close()

def onclick(event):
    global current_index
    
    if event.xdata != None and event.ydata != None:
        x, y = int(event.xdata), int(event.ydata)
        node_id, node_name = NODE_LIST[current_index]
        
        collected_nodes.append((node_id, node_name, x, y))
        print(f"KAYDEDILDI: {node_name} -> X:{x} Y:{y}")
        
        plt.plot(x, y, 'ro', markersize=5)
        plt.text(x+5, y, str(node_id), color='yellow', fontsize=8, fontweight='bold')
        plt.draw()
        
        current_index += 1
        
        if current_index >= len(NODE_LIST):
            save_to_file()
        else:
            next_id, next_name = NODE_LIST[current_index]
            plt.title(f"TIKLA: {next_name} (ID: {next_id}) - ({current_index}/{len(NODE_LIST)})")
            plt.draw()

try:
    img = mpimg.imread(MAP_FILENAME)
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.imshow(img)
    
    first_id, first_name = NODE_LIST[0]
    plt.title(f"TIKLA: {first_name} (ID: {first_id}) - Baslamak icin haritaya tikla")
    
    try:
        mng = plt.get_current_fig_manager()
        mng.window.state('zoomed') 
    except:
        pass

    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

except FileNotFoundError:
    print(f"HATA: {MAP_FILENAME} bulunamadi! Kodun basindaki dosya adini kontrol et.")