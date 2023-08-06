from sys import platform

if platform == 'win32':
    from .os_utils.win32_utils import make_shortcut
elif platform == 'darwin':
    from .os_utils.mac_utils import make_shortcut
else:
    from .os_utils.linux_utils import make_shortcut


