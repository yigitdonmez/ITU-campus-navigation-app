import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Harita dosya adın (En son kullandığın)
MAP_FILENAME = 'Campus.jpg' 

def onclick(event):
    if event.xdata != None and event.ydata != None:
        # Tıklanan yerin koordinatlarını ekrana bas
        print(f"--------------------------------------------------")
        print(f"TIKLANAN NOKTA KOORDINATI:  X={int(event.xdata)}   Y={int(event.ydata)}")
        print(f"--------------------------------------------------")
        
        # Tıkladığın yere kırmızı çarpı koy ki gör
        plt.plot(event.xdata, event.ydata, 'rx', markersize=12, markeredgewidth=2)
        plt.draw()

try:
    img = mpimg.imread(MAP_FILENAME)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(img)
    ax.set_title("Kalibrasyon: Lutfen istenen noktalara tiklayin")
    
    # Tıklama olayını bağla
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    
    plt.show()
except FileNotFoundError:
    print("Harita resmi bulunamadi!")