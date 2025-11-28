from cryptography.fernet import Fernet
from PIL import Image
from termcolor import colored
import pyfiglet

# Banner
banner = pyfiglet.figlet_format("StegoX", font="slant")
print(colored(banner, "cyan"))
print(colored("🔥 Python Steganography & Encryption Toolkit", "yellow"))
print(colored("Author: Shadow02", "green"))
print("-" * 60)

def extract_bits(img):
    pixels = img.load()
    bits = ""

    for x in range(img.width):
        for y in range(img.height):
            r, g, b = pixels[x, y]
            bits += str(r & 1)

    return bits

def bits_to_bytes(bits):
    return int(bits, 2).to_bytes(len(bits) // 8, "big")

image_path = input(colored("📁 Enter Stego image filename: ", "yellow"))
key = input(colored("🔑 Enter decryption key: ", "yellow")).encode()

cipher = Fernet(key)
img = Image.open(image_path)

# Extract LSB bitstream
bits = extract_bits(img)

# Extract stored message length (first 32 bits)
length = int(bits[:32], 2)

# Extract encrypted payload based on detected length
encrypted_bits = bits[32: 32 + (length * 8)]
encrypted_data = bits_to_bytes(encrypted_bits)

try:
    decrypted_message = cipher.decrypt(encrypted_data).decode()
    print(colored("\n✔ Secret message recovered:", "green"))
    print(colored(decrypted_message, "cyan"))

except:
    print(colored("\n❌ Decryption failed — wrong key or corrupted file.", "red"))

