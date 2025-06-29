import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import requests
import os
import ctypes
import re
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()

class WiFiConnectorApp:
    def __init__(self, root):
        self.root = root
        self.setup_app()
        self.username = "softwarica"  # Hardcoded for now
        self.password = "coventry2019"  # Hardcoded for now
        self.gateway_url = "http://gateway.example.com/loginpages/userlogin.shtml"

    def setup_app(self):
        self.root.title("College WiFi Connector")
        self.root.geometry("400x350")
        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Available LR Networks:").pack(pady=(0, 5))

        self.network_listbox = tk.Listbox(main_frame, height=10)
        self.network_listbox.pack(fill=tk.BOTH, expand=True, pady=5)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        ttk.Button(btn_frame, text="Scan Networks", command=self.scan_networks).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Connect", command=self.connect_to_network).pack(side=tk.LEFT, padx=5)

        self.status_var = tk.StringVar()
        self.status_var.set("Ready to connect")
        ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN).pack(fill=tk.X)

        self.scan_networks()

    def scan_networks(self):
        self.network_listbox.delete(0, tk.END)
        self.status_var.set("Scanning...")

        try:
            result = subprocess.run(
                'netsh wlan show networks',
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )

            networks = []
            for line in result.stdout.split('\n'):
                if "SSID" in line and not "BSSID" in line:
                    ssid = line.split(":")[1].strip()
                    if re.match(r'^(LR|STWCU_LR)-\d+$|^LR5$', ssid):
                        networks.append(ssid)

            if not networks:
                self.status_var.set("No LR, STWCU_LR, or LR5 networks found")
                return

            for network in sorted(networks):
                self.network_listbox.insert(tk.END, network)

            self.status_var.set(f"Found {len(networks)} networks")

        except subprocess.TimeoutExpired:
            self.status_var.set("Scan timed out")
            messagebox.showerror("Error", "Network scan took too long")
        except Exception as e:
            self.status_var.set("Scan failed")
            messagebox.showerror("Error", f"Failed to scan networks: {str(e)}")

    def connect_to_network(self):
        selection = self.network_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a network first")
            return

        network = self.network_listbox.get(selection[0])
        self.status_var.set(f"Connecting to {network}...")
        threading.Thread(target=self._connect_thread, args=(network,), daemon=True).start()

    def _connect_thread(self, network):
        try:
            # Attempt to connect to the network
            result = subprocess.run(
                f'netsh wlan connect name="{network}"',
                shell=True,
                capture_output=True,
                text=True,
                timeout=15
            )

            if result.returncode != 0:
                raise Exception(result.stderr or "Unknown connection error")

            # Send gateway login request with versatile User-Agent
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',  # Generic modern browser
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'http://gateway.example.com/',
                'Referer': 'http://gateway.example.com/loginpages/login.shtml?ReturnUrl=ZBu4bDqPWyeEeEZgUDdAb/dkVCN8KEu4MDe3V/dkUyewMAtMZA90b053',
                'Cookie': f'username={self.username}%40local; password={self.password}; Session=65f46ff3b04bbae99a26bb3cffd2a209',
            }
            data = {
                'username': self.username,
                'password': self.password,
                'accesscode': '',
                'vlan_id': '135'
            }

            response = requests.post(self.gateway_url, headers=headers, data=data, timeout=30)
            if response.status_code == 200:
                self.status_var.set(f"Connected to {network}")
            else:
                raise Exception(f"Gateway login failed with status {response.status_code}")

        except requests.exceptions.RequestException as e:
            self.status_var.set("Connection failed")
            messagebox.showerror("Error", f"Network authentication failed: {str(e)}")
        except subprocess.TimeoutExpired:
            self.status_var.set("Connection timed out")
            messagebox.showerror("Error", f"Connection to {network} timed out")
        except Exception as e:
            self.status_var.set("Connection failed")
            messagebox.showerror("Error", f"Failed to connect to {network}: {str(e)}")

if __name__ == "__main__":
    run_as_admin()
    if is_admin():
        root = tk.Tk()
        app = WiFiConnectorApp(root)
        root.mainloop()
    else:
        messagebox.showerror("Error", "Administrator rights required")