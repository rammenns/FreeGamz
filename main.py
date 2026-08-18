import sys
import subprocess
import psutil
from socket import socket, AF_INET, SOCK_STREAM, error
from PyQt5.QtWidgets import QApplication
from UI import MainWindow
import platform
from pathlib import Path
syst = platform.system()
oneinstance = None

def autostartx():

    if syst == "Linux":

        script = dr() / "GamzScript"

        if not script.exists():
            return None

        autostart = Path.home() / ".config" / "autostart"
        autostart.mkdir(parents = True, exist_ok = True)

        desktop = autostart / "GamzScript.desktop"

        if desktop.exists() and f'Exec="{script}"' in desktop.read_text(encoding = "utf-8"):
            return None

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

    elif syst == "Darwin":

        uid = subprocess.check_output(["id", "-u"], text=True).strip()
        service = f"gui/{uid}/com.gamzy.GamzScript"

        check = subprocess.run(
            ["launchctl", "print", service],
            capture_output=True
        )

        if check.returncode == 0:
            return True

        script = dr() / "GamzScript"

        if not script.exists():
            return False

        launchagents = Path.home() / "Library" / "LaunchAgents"
        launchagents.mkdir(parents=True, exist_ok=True)

        source_plist = Path(sys._MEIPASS) / "com.gamzy.GamzScript.plist"
        plist = launchagents / "com.gamzy.GamzScript.plist"

        try:
            plist.write_bytes(source_plist.read_bytes())
        except FileNotFoundError:
            return False

        resultz = subprocess.run([
            "launchctl",
            "bootstrap",
            f"gui/{uid}",
            str(plist)
        ])
        return resultz.returncode == 0

    return None


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

    autoxbool = True
    if syst == "Darwin":
        autoxbool = autostartx()

    if not scriptrun() and (syst != "Darwin" or not autoxbool):
        subprocess.Popen([str(dr() / gamzscript())])

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
