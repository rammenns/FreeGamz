import sys
from subprocess import Popen
import psutil
from socket import socket, AF_INET, SOCK_STREAM, error
from PyQt5.QtWidgets import QApplication
from UI import MainWindow
import platform
from pathlib import Path
syst = platform.system()
oneinstance = None

def autostartx():
    script = dr() / "GamzScript"

    if not script.exists():
        return

    autostart = Path.home() / ".config" / "autostart"
    autostart.mkdir(parents = True, exist_ok = True)

    desktop = autostart / "GamzScript.desktop"

    if desktop.exists() and f'Exec="{script}"' in desktop.read_text(encoding = "utf-8"):
        return

    desktop.write_text(
f"""[Desktop Entry]
Type=Application
Version=1.0
Name=GamzScript
Comment=Gamzy background checker
Exec="{script}"
Terminal=False
X-GNOME-Autostart-enabled=true
""",
        encoding = "utf-8"
    )

def dr():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent

def gamzscript():
    return "GamzScript.exe" if syst == "Windows" else "GamzScript"

def uirun():
    global oneinstance
    oneinstance = socket(AF_INET, SOCK_STREAM)
    try:
        oneinstance.bind(("127.0.0.1", 65432))
        return False
    except error:
        return True

def scriptrun():

    for p in psutil.process_iter(['name']):
        if p.info['name'] == gamzscript():
            return True

    return False

def main():
    app = QApplication(sys.argv)

    if uirun():
        return

    if syst == "Linux":
        autostartx()

    if not scriptrun():
        if syst in {"Windows", "Linux"}
            Popen([str(dr() / gamzscript())])
        elif syst == "Darwin":
            Popen(["open", "/Applications/GamzScript.app"])

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
