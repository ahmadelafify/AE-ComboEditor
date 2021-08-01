from win32 import win32api
import os, shutil
import sys
from winregistry import WinRegistry as Reg

MODULE_NAMES = ['ComboEditor.All', 'ComboEditor.Normalize', 'ComboEditor.Randomize', 'ComboEditor.RemoveDupes', 'ComboEditor.Uninstall']

def uninstall():
    try:
        """Directories"""
        PROGRAM_DIR = os.path.expandvars(r"%userprofile%") + r'\AppData\Local\VirtualStore\Program Files (x86)\Combo Editor'
        if os.path.exists(PROGRAM_DIR):
            try:
                shutil.rmtree(PROGRAM_DIR) # removes all files in folder except uninstall since being used
            except:
                pass

        """Registry"""
        reg = Reg()
        SHELL_PATH = r'HKEY_CLASSES_ROOT\*\shell'
        COMBO_EDITOR_PATH = f'{SHELL_PATH}\Combo Editor'
        COMMANDS_PATH = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell'
        try:
            # reg.read_key(COMBO_EDITOR_PATH)
            reg.delete_key(COMBO_EDITOR_PATH)
        except Exception as e:
            pass

        for MODULE_NAME in MODULE_NAMES:
            try:
                reg.read_key(f'{COMMANDS_PATH}\{MODULE_NAME}')
                reg.delete_key(f'{COMMANDS_PATH}\{MODULE_NAME}')
            except Exception as e:
                pass
    except Exception as e:
        pass

def main():
    try:
        arg = sys.argv[2]
    except:
        win32api.MessageBox(0, 'Error: Uninstall only from the menu.', 'Combo Editor')
        return
    if arg == "-uninstall":
        uninstall()
        win32api.MessageBox(0, 'Uninstalled C_EDITOR.', 'Combo Editor')

main()