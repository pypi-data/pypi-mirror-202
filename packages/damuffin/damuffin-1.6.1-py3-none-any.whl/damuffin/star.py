import subprocess
import winreg
import stat
import os

__all__ = ["ALL", "APP", "COMMANDS", "Startup"]

ALL = (lambda _: _, 1)
APP = (lambda _: _[0], 2)
COMMANDS = (lambda _: _[1], 3)
class SystemStartupError(Exception): pass

def __verify_path(dst):
    if not os.path.exists(dst):
        raise FileNotFoundError(f"Unable to find file or folder with path: {dst}")

def check_hidden_attribute(dst):
    __verify_path(dst)

    return bool(os.stat(dst).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)

def check_system_attribute(dst):
    __verify_path(dst)
    
    return bool(os.stat(dst).st_file_attributes & stat.FILE_ATTRIBUTE_SYSTEM)

def super_hide(dst):
    __verify_path(dst)
    
    try: subprocess.Popen(f"attrib +s +h {dst}", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except: pass

def hide(dst):
    __verify_path(dst)

    try: subprocess.Popen(f"attrib +h {dst}", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except: pass

class StartupTools:
    def get_registries(self, filter=APP):
        if filter[-1] not in [1,2,3]: raise ValueError("Expected 'filter' ALL, APP, or COMMANDS.")
        with winreg.OpenKey(key=winreg.HKEY_CURRENT_USER, sub_key=r'Software\Microsoft\Windows\CurrentVersion\Run', reserved=0, access=winreg.KEY_ALL_ACCESS) as k:
            return [filter[0](winreg.EnumValue(k, i)) for i in range(1, winreg.QueryInfoKey(k)[1])]

    def set_registry(self, app, src=None, autostart=True):
        if src is not None:
            if not os.path.exists(src): raise FileNotFoundError(f"Path '{src}' not found.")

        hkey = winreg.HKEY_CURRENT_USER

        with winreg.OpenKey(key=hkey, sub_key=r'Software\Microsoft\Windows\CurrentVersion\Run', reserved=0, access=winreg.KEY_ALL_ACCESS) as key:
            try:
                if autostart: winreg.SetValueEx(key, app, 0, winreg.REG_SZ, src); return True
                winreg.DeleteValue(key, app)
            except OSError: return False
        return True

class Startup(list):
    __tools = StartupTools()

    def __init__(self, filter=ALL):
        super().__init__(self.__tools.get_registries(filter=filter))
        self.apps = [c[0] for c in self]
        self.commands = [c[1] for c in self]

    def add(self, app, src):
        if not self.__tools.set_registry(app=app, src=src): return
        super().__setitem__(-1, app)

    def remove(self, app):
        if not self.__tools.set_registry(app, src=None, autostart=False): return
        if app in self: super().__delitem__(super().index(app))
    
    def __error(self, *args, **kwargs):
        raise SystemStartupError("Object can only contain the Windows System Startup Apps.")

    pop     = __error
    sort    = __error
    clear   = __error
    insert  = __error
    append  = __error
    extend  = __error
    reverse = __error

    def __getitem__(self, index):
        return self[index]
    
    __setitem__ = __error