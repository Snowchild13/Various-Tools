import subprocess
import platform

def execute_command(command):
#    Executes a shell command and returns the output.
#
#    Args:
#        command (str): The command to execute.
#
#    Returns:
#        str: The output of the command.
    
    try:
        # Execute the command and capture the output
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        # Decode the output bytes to string and strip any leading/trailing whitespace
        return output.decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        # If an error occurs, return the error output
        return e.output.decode("utf-8").strip()

def check_windows_version():
#    Checks the version of Windows.
#    Returns:
# str: The Windows version.
    
    # Get the Windows release version
    return platform.release()

def disable_guest_account():
    # Check if the Windows version is Windows 10
    if check_windows_version() == '10':
        # Disable the guest account
        execute_command("net user guest /active:no")
        print("Guest account disabled.")
    else:
        # Inform user that guest account cannot be disabled on this version of Windows
        print("Guest account cannot be disabled on this version of Windows.")

def enable_firewall():
    # Enable the Windows Firewall for all profiles
    execute_command("netsh advfirewall set allprofiles state on")
    print("Firewall enabled.")

def enable_windows_defender():
    # Check if the Windows version is Windows 10
    if check_windows_version() == '10':
        # Enable Windows Defender's real-time monitoring
        execute_command("Set-MpPreference -DisableRealtimeMonitoring 0")
        print("Windows Defender enabled.")
    else:
        # Inform user that Windows Defender is not available on this version of Windows
        print("Windows Defender is not available on this version of Windows.")

def restrict_remote_desktop_access():
    # Modify registry to deny Remote Desktop connections
    execute_command("reg add \"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server\" /v fDenyTSConnections /t REG_DWORD /d 1 /f")
    print("Remote Desktop access restricted.")

def main():
    print("Starting Windows hardening...")

    # Perform Windows hardening tasks
    disable_guest_account()
    enable_firewall()
    enable_windows_defender()
    restrict_remote_desktop_access()

    print("Windows hardening completed.")

if __name__ == "__main__":
    main()
