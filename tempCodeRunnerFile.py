import os
import shutil
import PyInstaller.__main__

# Clean previous builds
if os.path.exists('build'):
    shutil.rmtree('build')
if os.path.exists('dist'):
    shutil.rmtree('dist')
if os.path.exists('SoftwaricaWiFiConnector.spec'):
    os.remove('SoftwaricaWiFiConnector.spec')

# Build command
PyInstaller.__main__.run([
    'wifi_connector.py',
    '--onefile',
    '--windowed',
    '--name=SoftwaricaWiFiConnector',
    '--icon=wifi_icon.ico',
    '--clean',
    '--noconfirm'
])