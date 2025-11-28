#!/usr/bin/env python3
# stegox_gui.py — StegoX Pro GUI (Cyberpunk Dark / Neon Theme)
# Requirements: Pillow, cryptography
# Run: python3 stegox_gui.py

import os
from tkinter import (
    Tk, Frame, Label, Button, Entry, Text, Scrollbar,
    filedialog, messagebox, StringVar, Radiobutton, IntVar
)
from tkinter import ttk
from PIL import Image
from cryptography.fernet import Fernet

# -------------------------
# Core stego & crypto logic
# -------------------------

def generate_key() -> bytes:
    return Fernet.generate_key()

def encrypt_bytes(key: bytes, data: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(data)

def decrypt_bytes(key: bytes, token: bytes) -> bytes:
    f = Fernet(key)
    return f.decrypt(token)

def capacity_bytes(img: Image.Image) -> int:
    w, h = img.size
    channels = 3  # we use R,G,B channels
    return (w * h * channels) // 8  # total bytes we can store with 1 LSB per channel

def _bytes_to_bitstring(b: bytes) -> str:
    return ''.join(format(byte, '08b') for byte in b)

def _bitstring_to_bytes(s: str) -> bytes:
    # pad to multiple of 8
    if len(s) % 8 != 0:
        s = s.ljust((len(s) + 7) // 8 * 8, '0')
    by = bytearray()
    for i in range(0, len(s), 8):
        by.append(int(s[i:i+8], 2))
    return bytes(by)

def embed_bytes_into_image(cover_path: str, out_path: str, payload: bytes):
    img = Image.open(cover_path)
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA")
    # ensure RGB data
    img_rgb = img.convert("RGB")
    w, h = img_rgb.size
    cap = capacity_bytes(img_rgb)
    header = len(payload).to_bytes(4, 'big')  # 4 byte header
    full = header + payload
    if len(full) > cap:
        raise ValueError(f"Payload too large. Capacity: {cap} bytes, required: {len(full)} bytes")

    bits = _bytes_to_bitstring(full)
    pixels = list(img_rgb.getdata())  # list of (r,g,b)
    new_pixels = []
    bit_idx = 0
    total_bits = len(bits)

    for (r, g, b) in pixels:
        if bit_idx < total_bits:
            r = (r & ~1) | int(bits[bit_idx]); bit_idx += 1
        if bit_idx < total_bits:
            g = (g & ~1) | int(bits[bit_idx]); bit_idx += 1
        if bit_idx < total_bits:
            b = (b & ~1) | int(bits[bit_idx]); bit_idx += 1
        new_pixels.append((r, g, b))

    img_stego = Image.new("RGB", (w, h))
    img_stego.putdata(new_pixels)
    img_stego.save(out_path, "PNG")
    return out_path

def extract_bytes_from_image(stego_path: str) -> bytes:
    img = Image.open(stego_path).convert("RGB")
    pixels = list(img.getdata())
    bits = []
    for (r, g, b) in pixels:
        bits.append(str(r & 1))
        bits.append(str(g & 1))
        bits.append(str(b & 1))
    bitstr = ''.join(bits)
    # read first 32 bits => length
    length = int(bitstr[:32], 2)
    total_payload_bits = (length + 4) * 8  # header+payload in bits
    payload_bits = bitstr[32: 32 + (length * 8)]
    payload_bytes = _bitstring_to_bytes(payload_bits)
    return payload_bytes

# -------------------------
# Tkinter GUI (Cyberpunk)
# -------------------------

NEON_BG = "#0f1720"        # very dark blue/black
NEON_PANEL = "#071023"
NEON_ACCENT = "#00e6ff"    # cyan
#!/usr/bin/env python3
# stegox_gui.py — StegoX Pro GUI (Cyberpunk Dark / Neon Theme)

import os
from tkinter import (
    Tk, Frame, Label, Button, Entry, Text,
    filedialog, messagebox, StringVar, Radiobutton, IntVar
)
from tkinter import ttk
from PIL import Image
from cryptography.fernet import Fernet

# -------------------------
# Core Stego & Crypto Logic
# -------------------------

def generate_key() -> bytes:
    return Fernet.generate_key()

def encrypt_bytes(key: bytes, data: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(data)

def decrypt_bytes(key: bytes, token: bytes) -> bytes:
    f = Fernet(key)
    return f.decrypt(token)

def capacity_bytes(img: Image.Image) -> int:
    w, h = img.size
    channels = 3
    return (w * h * channels) // 8

def _bytes_to_bitstring(b: bytes) -> str:
    return ''.join(format(byte, '08b') for byte in b)

def _bitstring_to_bytes(s: str) -> bytes:
    if len(s) % 8 != 0:
        s = s.ljust((len(s) + 7) // 8 * 8, '0')
    return bytes(int(s[i:i+8], 2) for i in range(0, len(s), 8))

def embed_bytes_into_image(cover_path: str, out_path: str, payload: bytes):
    img = Image.open(cover_path)
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA")

    img_rgb = img.convert("RGB")
    w, h = img_rgb.size

    cap = capacity_bytes(img_rgb)
    header = len(payload).to_bytes(4, 'big')
    full = header + payload

    if len(full) > cap:
        raise ValueError(f"Payload too large. Capacity: {cap} bytes, required: {len(full)} bytes")

    bits = _bytes_to_bitstring(full)
    pixels = list(img_rgb.getdata())
    new_pixels, bit_idx, total_bits = [], 0, len(bits)

    for (r, g, b) in pixels:
        if bit_idx < total_bits:
            r = (r & ~1) | int(bits[bit_idx]); bit_idx += 1
        if bit_idx < total_bits:
            g = (g & ~1) | int(bits[bit_idx]); bit_idx += 1
        if bit_idx < total_bits:
            b = (b & ~1) | int(bits[bit_idx]); bit_idx += 1
        new_pixels.append((r, g, b))

    img_stego = Image.new("RGB", (w, h))
    img_stego.putdata(new_pixels)
    img_stego.save(out_path, "PNG")
    return out_path

def extract_bytes_from_image(stego_path: str) -> bytes:
    img = Image.open(stego_path).convert("RGB")
    pixels = list(img.getdata())

    bits = ''.join(str(channel & 1) for pixel in pixels for channel in pixel)
    length = int(bits[:32], 2)
    payload_bits = bits[32: 32 + length * 8]

    return _bitstring_to_bytes(payload_bits)

# -------------------------
# GUI Section
# -------------------------

NEON_BG = "#0f1720"
NEON_PANEL = "#071023"
NEON_ACCENT = "#00e6ff"
NEON_ACCENT2 = "#8a00ff"
NEON_TEXT = "#cfeefd"

class StegoGUI:
    def __init__(self, root):
        self.root = root
        root.title("StegoX Pro — Cyberpunk Stego Toolkit")
        root.geometry("900x600")
        root.minsize(900, 600)
        root.configure(bg=NEON_BG)

        self.cover_path = StringVar()
        self.payload_path = StringVar()
        self.out_path = StringVar(value="stego_output.png")
        self.key_text = StringVar()
        self.mode = IntVar(value=0)

        self.build_ui()

    def build_ui(self):
        Label(self.root, text="StegoX Pro", font=("Consolas", 24, "bold"),
              fg=NEON_ACCENT, bg=NEON_BG).place(x=20, y=10)

        Label(self.root, text="Encrypted Steganography — Cyberpunk Edition",
              font=("Consolas", 10), fg=NEON_ACCENT2, bg=NEON_BG).place(x=20, y=50)

        left = Frame(self.root, bg=NEON_PANEL, width=380, height=420)
        left.place(x=20, y=90)

        right = Frame(self.root, bg=NEON_PANEL, width=380, height=420)
        right.place(x=420, y=90)

        Label(left, text="Cover Image:", bg=NEON_PANEL, fg=NEON_TEXT).place(x=12, y=12)
        Entry(left, textvariable=self.cover_path, width=38, bg="#071827", fg=NEON_TEXT).place(x=12, y=36)
        Button(left, text="Browse", command=self.browse_cover, bg=NEON_ACCENT).place(x=290, y=34)

        Label(left, text="Mode:", bg=NEON_PANEL, fg=NEON_TEXT).place(x=12, y=76)
        Radiobutton(left, text="Text", variable=self.mode, value=0, bg=NEON_PANEL, fg=NEON_TEXT).place(x=70, y=74)
        Radiobutton(left, text="File", variable=self.mode, value=1, bg=NEON_PANEL, fg=NEON_TEXT).place(x=170, y=74)

        Label(left, text="Secret Message:", bg=NEON_PANEL, fg=NEON_TEXT).place(x=12, y=110)
        self.msg_box = Text(left, height=6, width=44, bg="#02121a", fg=NEON_TEXT)
        self.msg_box.place(x=12, y=132)

        Label(left, text="Payload File:", bg=NEON_PANEL, fg=NEON_TEXT).place(x=12, y=260)
        Entry(left, textvariable=self.payload_path, width=30, bg="#071827", fg=NEON_TEXT).place(x=12, y=284)
        Button(left, text="Browse", command=self.browse_payload, bg=NEON_ACCENT).place(x=260, y=282)

        Label(left, text="Output Image:", bg=NEON_PANEL, fg=NEON_TEXT).place(x=12, y=320)
        Entry(left, textvariable=self.out_path, width=30, bg="#071827", fg=NEON_TEXT).place(x=12, y=344)
        Button(left, text="Generate Key", command=self.generate_key_ui, bg=NEON_ACCENT).place(x=260, y=340)

        Button(left, text="EMBED", command=self.embed_action, bg=NEON_ACCENT2, width=20).place(x=30, y=388)
        Button(left, text="EXTRACT", command=self.extract_action, bg=NEON_ACCENT, width=20).place(x=200, y=388)

        Label(right, text="Log:", bg=NEON_PANEL, fg=NEON_TEXT).place(x=12, y=12)
        self.log = Text(right, height=20, width=44, bg="#02121a", fg=NEON_TEXT)
        self.log.place(x=12, y=36)
        self.log.insert("end", "StegoX Ready...\n")

        Button(right, text="Choose Stego Image", command=self.browse_stego, bg=NEON_ACCENT).place(x=12, y=385)
        Button(right, text="Load Key", command=self.load_keyfile, bg=NEON_ACCENT).place(x=180, y=385)

        Label(self.root, text="Key:", bg=NEON_BG, fg=NEON_ACCENT).place(x=20, y=560-10)
        self.key_entry = Entry(self.root, textvariable=self.key_text, width=80, bg="#071827", fg=NEON_TEXT)
        self.key_entry.place(x=60, y=560-10)

    def log_msg(self, msg):
        self.log.insert("end", msg + "\n")
        self.log.see("end")

    def browse_cover(self):
        p = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg")])
        if p: self.cover_path.set(p)

    def browse_payload(self):
        p = filedialog.askopenfilename()
        if p: self.payload_path.set(p)

    def browse_stego(self):
        p = filedialog.askopenfilename(filetypes=[("PNG", "*.png")])
        if p: self.cover_path.set(p)

    def generate_key_ui(self):
        key = generate_key()
        self.key_text.set(key.decode())
        self.log_msg("[+] Generated new key.")

    def load_keyfile(self):
        p = filedialog.askopenfilename(filetypes=[("Key Files", "*.key")])
        if p:
            with open(p, "rb") as f:
                self.key_text.set(f.read().decode())

    def embed_action(self):
        if not os.path.isfile(self.cover_path.get()):
            messagebox.showerror("Error", "Select a valid cover image.")
            return

        key = self.key_text.get().encode() if self.key_text.get() else generate_key()
        self.key_text.set(key.decode())

        if self.mode.get() == 1:
            with open(self.payload_path.get(), "rb") as f:
                payload = f.read()
        else:
            payload = self.msg_box.get("1.0", "end").strip().encode()

        enc = encrypt_bytes(key, payload)

        try:
            embed_bytes_into_image(self.cover_path.get(), self.out_path.get(), enc)
            self.log_msg(f"[+] Embedded successfully: {self.out_path.get()}")
            messagebox.showinfo("Success", "Data embedded successfully!")
        except Exception as e:
            self.log_msg(f"[-] Error: {e}")
            messagebox.showerror("Error", str(e))

    def extract_action(self):
        try:
            raw = extract_bytes_from_image(self.cover_path.get())
            dec = decrypt_bytes(self.key_text.get().encode(), raw)
            save_path = filedialog.asksaveasfilename()
            if save_path:
                with open(save_path, "wb") as f:
                    f.write(dec)
            self.log_msg("[+] Extraction successful!")
            messagebox.showinfo("Success", "Payload extracted successfully!")
        except Exception as e:
            self.log_msg(f"[-] Error: {e}")
            messagebox.showerror("Error", "Invalid key or corrupted stego image.")


def main():
    root = Tk()
    style = ttk.Style(root)
    try: style.theme_use("clam")
    except: pass
    StegoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
