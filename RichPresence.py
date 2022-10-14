import socket
import json
import time
import os
import PIL.Image
import ctypes
import requests

host, port = "127.0.0.1", 24981
clientId = "1029652193193762816"

#check pypresence install
print("Checking for PyPresence & PyStray")
try:
    from pypresence import Presence
    import pystray
except:
    print("PyPresence or PyStray isn't installed. Installing...")
    os.system("py -m pip install "+ "pystray")
    os.system("py -m pip install "+ "pypresence")
    os.system('cls')
    print("PyPresence and PyStray installed.")
    from pypresence import Presence
    import pystray

#discord
richPresence = Presence(clientId)
richPresence.connect()
startTime = time.time()

#minimize
def trayOnClick(icon, item):
    trayIcon.stop()
    os.system('cls')
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
    print("Closing...")
    time.sleep(3)
    os._exit(0)

iconImage = PIL.Image.open(requests.get("https://raw.githubusercontent.com/alpharmi/Roblox-Studio-Rich-Presence/main/logo.png", stream=True).raw)
trayIcon = pystray.Icon("RobloxStudioRichPresence", iconImage, menu=pystray.Menu(
    pystray.MenuItem("Close", trayOnClick)
))
print("Roblox Studio Rich Presence started. Minimizing to tray in 3s.")
time.sleep(3)
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
trayIcon.run_detached()


#server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen()

    while 1:
        connection, adress = server.accept()
        
        data = connection.recv(1024).decode("utf-8").splitlines()[11]
        jsonData = json.loads(data)

        if jsonData:
            editingText = None
            if jsonData["scriptType"] == "Workspace":
                editingText = "Editing {}".format(jsonData["scriptType"].upper())
            else:
                editingText = "Editing a {}".format(jsonData["scriptType"].upper())


            richPresence.update(
                state = "Game: {}".format(jsonData["gameName"].split("@")[0]), 
                details = "Editing: {}".format(jsonData["scriptName"]),
                start = startTime,

                large_image = jsonData["scriptType"].lower(),
                large_text = editingText,
                small_image = "logo",
                small_text = "Roblox Studio"
            )
        else:
            richPresence.clear()

        connection.close()