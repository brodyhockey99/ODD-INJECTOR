import subprocess
import os
import platform

def detect_vr_headset():
    system = platform.system()
    if system == "Windows":
        if os.path.exists("C:/Program Files (x86)/Steam/steamapps/common/SteamVR"):
            print("✔ SteamVR detected")
            return "PCVR"
        elif os.path.exists("C:/Program Files/Oculus"):
            print("✔ Oculus detected")
            return "PCVR"
        else:
            print("❌ No PCVR detected.")
            return None
    elif system == "Linux":
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
        devices = result.stdout.split("\n")[1:]
        for device in devices:
            if device.strip():
                print(f"✔ Quest detected: {device.split()[0]}")
                return "Quest"
        print("❌ No Quest detected. Make sure it's connected and ADB is enabled.")
        return None
    else:
        print("❌ Unsupported system")
        return None

def list_vr_games():
    games = {
        "1": "Gorilla Tag",
        "2": "Blade and Sorcery",
        "3": "VRChat",
        "4": "BONELAB"
    }
    print("Available games to mod:")
    for key, game in games.items():
        print(f"[{key}] {game}")
    return games

def patch_quest_game(game_name):
    print(f"🔧 Patching {game_name} on Quest...")
    subprocess.run(["adb", "push", "LemonLoader.apk", "/sdcard/Download/"])
    subprocess.run(["adb", "shell", "pm", "install", "/sdcard/Download/LemonLoader.apk"])
    subprocess.run(["adb", "push", "Mods/", "/sdcard/Mods/"])
    print("✔ Mods installed to Quest!")
    print(f"🚀 Launching {game_name} on Quest...")
    subprocess.run(["adb", "shell", "am", "start", "-n", f"{game_name}/.MainActivity"])

def patch_pcvr_game(game_name):
    print(f"🔧 Patching {game_name} on PCVR...")
    game_directory = f"C:/Program Files (x86)/Steam/steamapps/common/{game_name}/"
    subprocess.run(["cp", "-r", "BepInEx/", f"{game_directory}BepInEx/"])
    subprocess.run(["cp", "-r", "Mods/", f"{game_directory}Mods/"])
    print(f"✔ Mods installed to {game_name}!")
    print(f"🚀 Launching {game_name} on PCVR...")
    subprocess.run([f"{game_directory}{game_name}.exe"])

def main():
    print("🎮 VR Mod Loader")
    vr_device = detect_vr_headset()
    if vr_device:
        games = list_vr_games()
        choice = input("Select a game to patch (1-4): ")
        if choice in games:
            game_name = games[choice]
            if vr_device == "Quest":
                patch_quest_game(game_name)
            elif vr_device == "PCVR":
                patch_pcvr_game(game_name)
        else:
            print("❌ Invalid selection.")
    else:
        print("❌ No VR headset detected.")

if __name__ == "__main__":
    main()
