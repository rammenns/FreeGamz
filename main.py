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

    else:

        uid = subprocess.check_output(["id", "-u"], text=True).strip()
        service = f"gui/{uid}/com.gamzy.GamzScript"

        check = subprocess.run(
            ["launchctl", "print", service],
            capture_output=True
        )

        if check.returncode == 0:
            return True

        script = Path("/Applications/Gamzy.app/Contents/MacOS/GamzScript")

        if not script.exists():
            return False

        launchagents = Path.home() / "Library" / "LaunchAgents"
        launchagents.mkdir(parents=True, exist_ok=True)

        plist = launchagents / "com.gamzy.GamzScript.plist"

        plist.write_text(
f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN"
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.gamzy.GamzScript</string>
    <key>ProgramArguments</key>
    <array>
        <string>{script}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
""",
            encoding="utf-8"
        )

        resultz = subprocess.run([
            "launchctl",
            "bootstrap",
            f"gui/{uid}",
            str(plist)
        ])
        return resultz.returncode == 0

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

    if syst in {"Linux", "Darwin"}:
        autoxbool = autostartx() if syst == "Darwin" else None

    if not scriptrun():
        if syst in {"Windows", "Linux"}:
            subprocess.Popen([str(dr() / gamzscript())])
        elif syst == "Darwin" and not autoxbool:
            subprocess.Popen(["/Applications/Gamzy.app/Contents/MacOS/GamzScript"])

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
