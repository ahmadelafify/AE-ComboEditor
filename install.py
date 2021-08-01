from winregistry import WinRegistry as Reg
from win32 import win32api
import os, shutil

MODULE_NAMES = ['ComboEditor.All', 'ComboEditor.Normalize', 'ComboEditor.Randomize', 'ComboEditor.RemoveDupes', 'ComboEditor.Uninstall']

def install():
    try:
        """Make Directories Files"""
        LOCAL = os.path.expandvars(r"%userprofile%") + r'\AppData\Local'
        VSTORE = os.path.expandvars(r"%userprofile%") + r'\AppData\Local\VirtualStore'
        PROGRAM_FILES = os.path.expandvars(r"%userprofile%") + r'\AppData\Local\VirtualStore\Program Files (x86)'
        PROGRAM_DIR = os.path.expandvars(r"%userprofile%") + r'\AppData\Local\VirtualStore\Program Files (x86)\Combo Editor'
        PROGRAM_PATH = f'{PROGRAM_DIR}\\c_editor.exe'
        PROGRAM_TEMP_DIR = PROGRAM_DIR + r'\temp'
        UNINSTALL_PATH = f'{PROGRAM_DIR}\\uninstall.exe'
        if os.path.exists(VSTORE) == False:
            os.mkdir(VSTORE)
        if os.path.exists(PROGRAM_FILES) == False:
            os.mkdir(PROGRAM_FILES)
        if os.path.exists(PROGRAM_DIR) == False:
            os.mkdir(PROGRAM_DIR)
        if os.path.exists(PROGRAM_TEMP_DIR) == False:
            os.mkdir(PROGRAM_TEMP_DIR)
        if os.path.exists(PROGRAM_PATH) == False:
            shutil.copy("c_editor.exe", PROGRAM_PATH)
            shutil.copy("uninstall.exe", UNINSTALL_PATH)

        """Registry"""
        reg = Reg()
        SHELL_PATH = r'HKEY_CLASSES_ROOT\*\shell'
        COMBO_EDITOR_PATH = f'{SHELL_PATH}\Combo Editor'
        COMMANDS_PATH = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell'
        reg.create_key(COMBO_EDITOR_PATH)
        reg.write_value(COMBO_EDITOR_PATH, 'Icon', f'"{PROGRAM_PATH}"', 'REG_SZ')
        reg.write_value(COMBO_EDITOR_PATH, 'MUIVerb', r'Combo Editor', 'REG_SZ')
        MODS = ''
        for i, mod in enumerate(MODULE_NAMES):
            MODS += f'{mod};'
        reg.write_value(COMBO_EDITOR_PATH, 'SubCommands', MODS, 'REG_SZ')
        for MODULE_NAME in MODULE_NAMES:
            if MODULE_NAME == 'ComboEditor.Uninstall':
                reg.create_key(f'{COMMANDS_PATH}\{MODULE_NAME}')
                NAME = MODULE_NAME.replace('ComboEditor.', '')
                reg.write_value(f'{COMMANDS_PATH}\{MODULE_NAME}', '', NAME, 'REG_SZ')
                reg.create_key(f'{COMMANDS_PATH}\{MODULE_NAME}\command')
                reg.write_value(f'{COMMANDS_PATH}\{MODULE_NAME}\command', '', f'"{UNINSTALL_PATH}" "%1" -{NAME.lower()}', 'REG_SZ')
            else:
                reg.create_key(f'{COMMANDS_PATH}\{MODULE_NAME}')
                NAME = MODULE_NAME.replace('ComboEditor.', '')
                reg.write_value(f'{COMMANDS_PATH}\{MODULE_NAME}', '', NAME, 'REG_SZ')
                reg.create_key(f'{COMMANDS_PATH}\{MODULE_NAME}\command')
                reg.write_value(f'{COMMANDS_PATH}\{MODULE_NAME}\command', '', f'"{PROGRAM_PATH}" "%1" -{NAME.lower()}', 'REG_SZ')
        win32api.MessageBox(0, 'Installed C_EDITOR.', 'Combo Editor')
    except Exception as e:
        pass

install()
