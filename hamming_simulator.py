import tkinter as tk
from tkinter import messagebox
import random
import math

class HammingSECDEDSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Hamming SEC-DED Simülatörü (8/16/32 bit)")

        #  Veri Girişi 
        tk.Label(root, text="Veri (8, 16 veya 32 bit):").pack()
        self.data_entry = tk.Entry(root, width=40)
        self.data_entry.pack()

        self.encode_button = tk.Button(root, text="Belleğe Yaz (Kodla)", command=self.encode_and_store)
        self.encode_button.pack()

        # Bellek Çıktısı 
        tk.Label(root, text="Bellekte Saklanan (Kodlanmış) Veri:").pack()
        self.output_frame = tk.Frame(root)
        self.output_frame.pack()

        # Hata Girişi 
        tk.Label(root, text="Bozmak istediğiniz bit numaralarını girin (örn: 3,5,7):").pack()
        self.bit_entry = tk.Entry(root, width=20)
        self.bit_entry.pack()

        self.error_button = tk.Button(root, text="Yapay Hata(lar) Oluştur", command=self.inject_error)
        self.error_button.pack()

        # Bozulmuş Veri 
        tk.Label(root, text="Bozulmuş Bellek Verisi:").pack()
        self.corrupted_frame = tk.Frame(root)
        self.corrupted_frame.pack()

        # Hata Düzeltme ve Analiz 
        self.correct_button = tk.Button(root, text="Hata Tespit Et ve Düzelt", command=self.analyze_and_correct)
        self.correct_button.pack()

        tk.Label(root, text="Düzeltilmiş Bellek Verisi:").pack()
        self.result_frame = tk.Frame(root)
        self.result_frame.pack()

        self.message_label = tk.Label(root, text="", fg="blue")
        self.message_label.pack()

        self.original_data = ""
        self.encoded_bits = []
        self.corrupted_bits = []

    def encode_and_store(self):
        data = self.data_entry.get().strip()
        if not all(c in '01' for c in data) or len(data) not in (8, 16, 32):
            messagebox.showerror("Hata", "Lütfen sadece 0 ve 1 içeren 8, 16 veya 32 bitlik bir veri girin.")
            return

        self.original_data = data
        self.encoded_bits = self.hamming_sec_ded_encode(data)
        self.corrupted_bits = []

        self.show_bits(self.output_frame, self.encoded_bits)
        self.show_bits(self.corrupted_frame, [])
        self.show_bits(self.result_frame, [])
        self.message_label.config(text="Veri belleğe yazıldı ve Hamming kodu hesaplandı.")

    def hamming_sec_ded_encode(self, data):
        d = list(map(int, data))
        m = len(d)
        r = 0
        while (2 ** r) < (m + r + 1):
            r += 1

        codeword = [0] * (m + r + 1)
        j = 0
        for i in range(1, len(codeword)):
            if i & (i - 1) == 0:
                continue
            codeword[i] = d[j]
            j += 1

        for i in range(r):
            pos = 2 ** i
            parity = 0
            for j in range(1, len(codeword)):
                if j & pos:
                    parity ^= codeword[j]
            codeword[pos] = parity

        overall_parity = sum(codeword[1:]) % 2
        codeword[0] = overall_parity

        return list(map(str, codeword))

    def inject_error(self):
        if not self.encoded_bits:
            messagebox.showwarning("Uyarı", "Önce belleğe veri yazın.")
            return

        bit_str = self.bit_entry.get()
        bit_indices = []
        try:
            bit_indices = [int(b.strip()) - 1 for b in bit_str.split(',') if b.strip()]
        except ValueError:
            messagebox.showerror("Hata", "Geçerli bit numaraları girin, örn: 1,3,5")
            return

        if any(b < 0 or b >= len(self.encoded_bits) for b in bit_indices):
            messagebox.showerror("Hata", f"Bit numaraları 1 ile {len(self.encoded_bits)} arasında olmalı.")
            return

        corrupted = self.encoded_bits.copy()
        for idx in bit_indices:
            corrupted[idx] = '1' if corrupted[idx] == '0' else '0'

        self.corrupted_bits = corrupted

        self.show_bits(self.corrupted_frame, corrupted, highlight_index=bit_indices, highlight_color="red")
        self.show_bits(self.result_frame, [])
        self.message_label.config(text=f"Yapay olarak {len(bit_indices)} bit bozuldu: {', '.join(str(i+1) for i in bit_indices)}")

    def analyze_and_correct(self):
        if not self.corrupted_bits:
            messagebox.showwarning("Uyarı", "Önce yapay hata oluşturun.")
            return

        bits = list(map(int, self.corrupted_bits))
        n = len(bits)
        r = int(math.log2(n)) + 1
        syndrome = 0

        for i in range(r):
            pos = 2 ** i
            parity = 0
            for j in range(1, n):
                if j & pos:
                    parity ^= bits[j]
            if parity:
                syndrome |= pos

        total_parity = sum(bits[1:]) % 2
        overall_parity = bits[0]

        result = bits.copy()
        msg = ""

        if syndrome == 0 and total_parity == overall_parity:
            msg = "Bellek verisinde hata yok."
        elif syndrome != 0 and (total_parity ^ overall_parity) == 1:
            idx = syndrome
            if 0 < idx < len(bits):
                result[idx] ^= 1
                msg = f"Tekli hata tespit edildi. Bit {idx+1} düzeltildi."
                self.show_bits(self.result_frame, list(map(str, result)), highlight_index=idx, highlight_color="lightgreen")
            else:
                msg = "Geçersiz hata konumu. Kod çözümünde sorun olabilir."
        elif syndrome != 0 and (total_parity ^ overall_parity) == 0:
            msg = f"Çift hata tespit edildi. DÜZELTİLEMEZ!"
            self.show_bits(self.result_frame, list(map(str, bits)))
        else:
            msg = "Parity uyuşmazlığı. Veri ciddi şekilde bozulmuş olabilir."

        self.message_label.config(text=msg)

    def show_bits(self, frame, bits, highlight_index=None, highlight_color="red"):
        for widget in frame.winfo_children():
            widget.destroy()
        for i, bit in enumerate(bits):
            color = "lightgray"
            if highlight_index is not None:
                if isinstance(highlight_index, list) and i in highlight_index:
                    color = highlight_color
                elif i == highlight_index:
                    color = highlight_color
            label = tk.Label(frame, text=bit, width=2, height=1, borderwidth=1, relief="solid", bg=color)
            label.pack(side=tk.LEFT, padx=1, pady=2)


# Arayüzü Başlatma 
if __name__ == "__main__":
    root = tk.Tk()
    app = HammingSECDEDSimulator(root)
    root.mainloop()
