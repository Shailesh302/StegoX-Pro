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

def encrypt_message(message):
    key = Fernet.generate_key()
    cipher = Fernet(key)
    encrypted = cipher.encrypt(message.encode())
    return encrypted, key

def encode_data(data):
    length = len(data).to_bytes(4, "big")  # first 4 bytes store encrypted data length
    full_data = length + data
    return ''.join(format(byte, '08b') for byte in full_data)

def hide_data(image_path, data, output_path):
    img = Image.open(image_path)
    bin_data = encode_data(data)
    pixels = img.load()

    data_index = 0
    data_len = len(bin_data)

    for x in range(img.width):
        for y in range(img.height):
            if data_index < data_len:
                r, g, b = pixels[x, y]
                r = (r & ~1) | int(bin_data[data_index])
                pixels[x, y] = (r, g, b)
                data_index += 1
            else:
                break

    img.save(output_path)

message = input(colored("📝 Enter message to hide: ", "yellow"))
image_path = input(colored("📁 Enter input image (png/jpg): ", "yellow"))
output_path = input(colored("💾 Enter output filename (example: secret.png): ", "yellow"))

encrypted, key = encrypt_message(message)
hide_data(image_path, encrypted, output_path)

print(colored("\n✔ Message successfully hidden inside image!", "green"))
print(colored("🔑 SAVE THIS KEY (required to extract message):", "yellow"))
print(colored(key.decode(), "cyan"))
print(colored("\n📂 Output file created: " + output_path, "green"))

