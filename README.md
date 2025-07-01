
---

# 📶 Softwarica WiFi Connector

A lightweight and user-friendly Python-based GUI tool that scans, connects, and authenticates to **Softwarica College Wi-Fi** networks such as `LR-XX`, `STWCU_LR-XX`, and `LR5`. The app is built using `tkinter`, `subprocess`, and `requests`, and is compiled into a standalone `.exe` for easy use on Windows systems.

<p align="center">
  <img src="https://github.com/user-attachments/assets/21077b8d-9d30-444c-838e-0f3748674b77" alt="UI Preview" />
</p>

---

## 🚀 Features

* 📡 **Auto Scan** – Detects nearby LR, STWCU\_LR, and LR5 networks.
* 🔐 **One-Click Login** – Connects and authenticates to the college gateway in one click.
* 🛡️ **Admin Access Check** – Automatically prompts for admin rights if required.
* 🪟 **Graphical Interface** – Simple GUI built with `tkinter` for smooth interaction.
* 🛠️ **Windows Executable** – Delivered as a `.exe` file — no Python installation needed.

---

## 📦 Download

A precompiled `.exe` file is available for download:

👉 [Download from Releases](https://github.com/hyperdargo/SoftwaricaWi-FiConnector/releases/tag/SoftwaricaWi-FiConnector)

Just download, run as administrator, and connect. Simple as that.

---

## 🛠️ Build It Yourself

### Requirements

* Python 3.x
* `pyinstaller`
* `requests`

Install dependencies:

```bash
pip install pyinstaller requests
```

### Build Instructions

Run the following script to create your `.exe`:

```bash
python build_wifi_app.py
```

The script will:

* Remove previous build files
* Create a new `.exe` using PyInstaller
* Save it to the `dist/` directory

---

## ⚙️ How It Works

1. Scans available Wi-Fi networks using `netsh wlan show networks`.
2. Filters the list to match college networks (LR, STWCU\_LR, LR5).
3. Connects using `netsh wlan connect`.
4. Sends an HTTP POST request with login credentials to authenticate to the college gateway.

⚠️ **Note**: The app currently uses hardcoded credentials for demonstration. For security, modify `wifi_connector.py` to take dynamic user input or load credentials from a secure file.

---

## 📁 Project Structure

```
SoftwaricaWiFiConnector/
├── build/                      # Auto-generated build folder
├── dist/                       # Final .exe output
├── wifi_connector.py           # Main GUI application code
├── build_wifi_app.py           # Build script for PyInstaller
├── wifi_icon.ico               # App icon
├── SoftwaricaWiFiConnector.spec
└── README.md
```

---

## 📝 License

This script is for **educational use only**. Do not distribute or misuse it on unauthorized networks.

---

## 🙋 About the Author

I'm **Ankit Gupta** (aka **Dargo Tamber**), a developer and ethical hacker based in Kathmandu, Nepal.
Currently studying at **Softwarica College**, I build tools that solve practical problems — like this Wi-Fi connector made specifically for students.

📫 Contact me at: [ankitstudentid@gmail.com](mailto:ankitstudentid@gmail.com)
🌐 GitHub: [@hyperdargo](https://github.com/hyperdargo)

---

