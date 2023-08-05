import ctypes
import os


def enableLUA_disableLUA(enable:bool=True) ->type(None):
    """
    Enable or disable User Account Control (UAC) in Windows by modifying the registry key.

    Args:
        enable (bool, optional): If True, enable UAC. If False, disable UAC. Defaults to True.

    Raises:
        WindowsError: If any of the Windows API calls fail.

    Returns:
        None
    """
    command = ""
    if enable is False:
        command = r"""reg.exe ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 0 /f"""
    if enable is True:
        command = r"""reg.exe ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 1 /f"""

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)

    # define constants
    HKEY_LOCAL_MACHINE = 0x80000002
    KEY_WRITE = 0x20006
    REG_DWORD = 4

    # open registry key
    hkey = ctypes.c_void_p()
    res = advapi32.RegOpenKeyExW(
        HKEY_LOCAL_MACHINE,
        "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System",
        0,
        KEY_WRITE,
        ctypes.byref(hkey),
    )
    if res != 0:
        raise WindowsError(f"RegOpenKeyExW failed with error {res}")

    # set value
    value = 0 if not enable else 1
    res = advapi32.RegSetValueExW(
        hkey, "EnableLUA", 0, REG_DWORD, ctypes.byref(ctypes.c_uint32(value)), 4
    )
    if res != 0:
        advapi32.RegCloseKey(hkey)
        raise WindowsError(f"RegSetValueExW failed with error {res}")

    # close registry key
    res = advapi32.RegCloseKey(hkey)
    if res != 0:
        raise WindowsError(f"RegCloseKey failed with error {res}")

    # run command to refresh the policy
    res = kernel32.Wow64DisableWow64FsRedirection(ctypes.byref(ctypes.c_void_p()))
    if res != 0:
        raise WindowsError(
            f"Wow64DisableWow64FsRedirection failed with error {kernel32.GetLastError()}"
        )

    os.system(command)

    res = kernel32.Wow64RevertWow64FsRedirection(ctypes.byref(ctypes.c_void_p()))
    if res != 0:
        raise WindowsError(
            f"Wow64RevertWow64FsRedirection failed with error {kernel32.GetLastError()}"
        )
