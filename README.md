# StegoX-Pro
StegoX Pro is a Python-based steganography tool that securely embeds and extracts hidden messages inside image files using AES-256 encryption. It supports both Graphical User Interface (GUI) and Command-Line Interface (CLI) — making it easy for beginners and powerful for technical users.

🛡️ StegoX Pro
🔐 Advanced Steganography Tool with AES Encryption | GUI + CLI

StegoX Pro is a Python-based steganography tool that securely embeds and extracts hidden messages inside image files using AES-256 encryption.
It supports both Graphical User Interface (GUI) and Command-Line Interface (CLI) — making it easy for beginners and powerful for technical users.

🚀 Features

✔️ AES-256 Encryption for secure messaging
✔️ Embed text inside image files without visible changes
✔️ Extract hidden text using the correct encryption key
✔️ Lightweight, fast, and user-friendly
✔️ Dual-mode access: GUI (Tkinter) & CLI (Terminal)
✔️ Error handling for wrong keys or corrupted files
✔️ Works offline — full privacy

🖼️ Demo Preview

🔽 The video demonstration showcases:
Running StegoX Pro in GUI mode
Running StegoX Pro in CLI mode
Encrypting a message
Embedding the encrypted text inside an image
Extracting the hidden message using a secure key
Both modes are shown step-by-step in the demo.

🔧 Installation
git clone https://github.com/shailesh302/StegoX-Pro.git
cd StegoX-Pro
pip install -r requirements.txt

🖥️ Run Modes

▶️ GUI Mode
python stego_gui.py

💻 CLI Mode
python stego_cli.py --mode hide --image input.png --output encoded.png --message "Hello World" --key MySecretKey

To extract:
python stego_cli.py --mode extract --image encoded.png --key MySecretKey

📂 Project Structure
📁 StegoX-Pro
 ┣ 📄 stego_gui.py
 ┣ 📄 stego_cli.py
 ┣ 📄 encryption.py
 ┣ 📄 stego_engine.py
 ┣ 📂 assets
 ┗ 📄 requirements.txt

🛠️ Technologies Used
Python
Tkinter (GUI)
Cryptography (AES Encryption)
Pillow (Image Processing)
Argparse (CLI support)

🔒 Security Note
Without the correct key, the hidden message cannot be extracted, ensuring complete privacy and confidentiality.

🧪 Future Enhancements (Planned)
Support for audio and video steganography
Multi-language support
Password strength checker
Drag-and-drop UI

🌟 Author
👤 Shailesh Wagh
💼 Cybersecurity & Software Development Enthusiast
📍 Diploma in Computer Engineering

⭐ Support This Project
If you like StegoX Pro, please star the repository ⭐ and share feedback!
