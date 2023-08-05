import ctypes
import os
import subprocess


def am_i_admin() -> bool:
    try:
        return os.getuid() == 0
    except Exception:
        pass
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() == 1
    except Exception:
        p = subprocess.run(
            r'''%systemroot%\system32\Reg.exe query "HKU\S-1-5-19\Environment"''',
            shell=True,
        )
        if p.returncode == 0:
            return True
    return False
