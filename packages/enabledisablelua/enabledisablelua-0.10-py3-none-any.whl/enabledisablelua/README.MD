# Enables or disables User Account Control (UAC) on Windows


```python
pip install enabledisablelua
```

```python

More about disabling LUA/UAC on Windows 
# https://winaero.com/how-to-turn-off-and-disable-uac-in-windows-10/?utm_source=software&utm_medium=in-app&utm_campaign=winaerotweaker&utm_content=uac


from enabledisablelua import enableLUA_disableLUA

enableLUA_disableLUA(enable=True)

enableLUA_disableLUA(enable=False)

    Enable or disable User Account Control (UAC) on Windows by modifying the registry key.

    Args:
        enable (bool, optional): If True, enable UAC. If False, disable UAC. Defaults to True.

    Raises:
        WindowsError: If any of the Windows API calls fail.

    Returns:
        None
		
		
```