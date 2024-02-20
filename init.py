import subprocess

def installLibs():
    libraries = ['pyautogui', 'neo4j','pickle']
    for library in libraries:
        try:
            subprocess.check_call(['pip', 'install', library])
            print(f"Successfully installed {library}")
        except subprocess.CalledProcessError:
            print(f"Failed to install {library}")

if __name__ == "__main__":
    installLibs()