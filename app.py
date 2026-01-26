import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# settings
C_EXECUTABLE = 'main.exe' if os.name == 'nt' else './main'
MAP_FILENAME = 'Campus_8K.jpg'
NODE_FILENAME = 'nodes.txt'
PATH_FILENAME = 'path.txt'

NODE_SCALE = 1.0
NODE_SHIFT_X = 0
NODE_SHIFT_Y = 0

FONT_LABEL = ("Segoe UI", 12)
FONT_COMBO = ("Segoe UI", 12)
FONT_BUTTON = ("Segoe UI", 13, "bold")
FONT_INFO = ("Consolas", 11)

class MapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("İTÜ Kampüs Rota Bulucu")
        self.root.geometry("1920x850")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure("Big.TButton", font=FONT_BUTTON, padding=10)

        self.nodes = self.load_nodes()
        self.node_names = {v[2]: k for k, v in self.nodes.items() if k < 100}
        self.sorted_names = sorted(self.node_names.keys())

        control_frame = tk.Frame(root, width=350, bg="#f0f0f0", padx=20, pady=20)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)
        control_frame.pack_propagate(False) 

        lbl_start = ttk.Label(control_frame, text="Başlangıç Noktası:", font=FONT_LABEL, background="#f0f0f0")
        lbl_start.pack(pady=(0, 5), anchor="w")

        self.start_combo = ttk.Combobox(control_frame, values=self.sorted_names, state="readonly", font=FONT_COMBO)
        self.start_combo.pack(pady=(0, 20), fill=tk.X)
        self.start_combo.set("Ari_Kapi")
        root.option_add('*TCombobox*Listbox.font', FONT_COMBO)

        lbl_end = ttk.Label(control_frame, text="Varış Noktası:", font=FONT_LABEL, background="#f0f0f0")
        lbl_end.pack(pady=(0, 5), anchor="w")

        self.end_combo = ttk.Combobox(control_frame, values=self.sorted_names, state="readonly", font=FONT_COMBO)
        self.end_combo.pack(pady=(0, 30), fill=tk.X)
        self.end_combo.set("MED")

        self.btn_calc = ttk.Button(control_frame, text="ROTAYI GÖSTER", command=self.run_pathfinding, style="Big.TButton")
        self.btn_calc.pack(pady=10, fill=tk.X)

        inner_frame = tk.Frame(control_frame, bg="#f0f0f0", padx=20)
        inner_frame.pack(expand=True, fill=tk.BOTH)

        info_frame = tk.Frame(inner_frame, bg="#f0f0f0")
        info_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(info_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.result_text = tk.Text(info_frame, height=15, width=40, font=("Consolas", 10), bg="white", fg="#333", yscrollcommand=self.scrollbar.set, relief="sunken", bd=1)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar.config(command=self.result_text.yview)

        self.insert_text("Rota bekleniyor...")

        map_frame = ttk.Frame(root)
        map_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(12, 10))
        self.fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
        self.canvas = FigureCanvasTkAgg(self.fig, master=map_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.root.update()
        self.draw_map()

    def load_nodes(self):
        data = {}
        if not os.path.exists(NODE_FILENAME):
            messagebox.showerror("Hata", f"{NODE_FILENAME} bulunamadı!")
            return data 
        with open(NODE_FILENAME, 'r') as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 4:
                    nid = int(parts[0])
                    name = parts[1]
                    rx = int(parts[2])
                    ry = int(parts[3])
                    x = (rx * NODE_SCALE) + NODE_SHIFT_X
                    y = (ry * NODE_SCALE) + NODE_SHIFT_Y
                    data[nid] = (x, y, name)
        return data

    def run_pathfinding(self):
            start_name = self.start_combo.get()
            end_name = self.end_combo.get()

            if not start_name or not end_name:
                messagebox.showwarning("Uyarı", "Lütfen iki nokta seçiniz.")
                return

            start_id = self.node_names[start_name]
            end_id = self.node_names[end_name]

            try:
                executable_path = os.path.join(os.getcwd(), C_EXECUTABLE)
                subprocess.run([executable_path, str(start_id), str(end_id)], check=True)
                
                self.draw_map(show_path=True)
                
                distance_val = 0
                if os.path.exists("path_info.txt"):
                    with open("path_info.txt", "r") as f:
                        try:
                            content = f.read().strip()
                            distance_val = float(content)
                        except ValueError:
                            pass
                estimated_minutes = distance_val * 0.025 
                
                path_names = []
                if os.path.exists(PATH_FILENAME):
                    with open(PATH_FILENAME, 'r') as f:
                        lines = f.readlines()
                        for line in reversed(lines):
                            parts = line.split()
                            node_id = int(parts[0])
                            if node_id in self.nodes:
                                node_name = self.nodes[node_id][2]
                                path_names.append(node_name)
                            else:
                                path_names.append(f"Kavsak({node_id})")

                vertical_path_str = ""                
                for i, name in enumerate(path_names):
                    if i == 0:
                        vertical_path_str += f"📍 BAŞLANGIÇ: {name}\n"
                        vertical_path_str += "      ⬇\n"
                    elif i == len(path_names) - 1:
                        vertical_path_str += f"🏁 VARIŞ: {name}"
                    else:
                        vertical_path_str += f"  • {name}\n"
                        vertical_path_str += "      ⬇\n"

                final_message = f"✅ ROTA HESAPLANDI\n" \
                                f"──────────────────────────\n" \
                                f"🚶 Tahmini Süre: {estimated_minutes:.1f} dk\n" \
                                f"📏 Mesafe: {distance_val:.0f} m\n" \
                                f"──────────────────────────\n" \
                                f"{vertical_path_str}"
                            
                self.insert_text(final_message, color="#004d00")
                
            except FileNotFoundError:
                messagebox.showerror("Hata", f"C programı ({C_EXECUTABLE}) bulunamadı.")
            except subprocess.CalledProcessError:
                self.insert_text("❌ HATA: Rota bulunamadı.", color="red")

    def draw_map(self, show_path=False):
        self.ax.clear()
        
        if os.path.exists(MAP_FILENAME):
            img = mpimg.imread(MAP_FILENAME)
            img_h, img_w, _ = img.shape
            self.ax.imshow(img)
            self.ax.set_xlim(0, img_w)
            self.ax.set_ylim(img_h, 0)
            self.ax.axis('off')
        else:
            self.ax.text(0.5, 0.5, "Harita Resmi Bulunamadı", ha='center')

        for nid, (x, y, name) in self.nodes.items():
            if nid < 100: 
                self.ax.plot(x, y, 'bo', markersize=4.5, alpha=0.6)

        if show_path and os.path.exists(PATH_FILENAME):
            path_x = []
            path_y = []
            with open(PATH_FILENAME, 'r') as f:
                for line in f:
                    parts = line.split()
                    raw_px = int(parts[1])
                    raw_py = int(parts[2])
                    px = (raw_px * NODE_SCALE) + NODE_SHIFT_X
                    py = (raw_py * NODE_SCALE) + NODE_SHIFT_Y
                    path_x.append(px)
                    path_y.append(py)
            
            if path_x:
                self.ax.plot(path_x, path_y, color='#39FF14', linewidth=5, alpha=0.8, label='Rota')
                self.ax.plot(path_x[-1], path_y[-1], 'go', markersize=12, markeredgecolor='white', label='Başlangıç')
                self.ax.plot(path_x[0], path_y[0], 'ro', markersize=12, markeredgecolor='white', label='Varış')

        self.canvas.draw()

    def insert_text(self, message, color="black"):
        """Metin kutusuna güvenli şekilde yazı yazar."""
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, message)
        self.result_text.config(fg=color)
        self.result_text.config(state="disabled")

def on_closing():
    print("Program closing...")
    root.quit()
    root.destroy()
    exit()

if __name__ == "__main__":
    root = tk.Tk()
    
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
        
    app = MapApp(root)
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()