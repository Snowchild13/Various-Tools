import subprocess
import platform

def execute_command(command):
    """
    Executes a shell command and returns the output.

    Args:
        command (str): The command to execute.

    Returns:
        str: The output of the command.
    """
    try:
        # Execute the command and capture the output
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        # Decode the output bytes to string and strip any leading/trailing whitespace
        return output.decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        # If an error occurs, return the error output
        return e.output.decode("utf-8").strip()

def check_windows_version():
    # Get the Windows release version
    return platform.release()

def monitor_security_logs():
    """
    Monitors security logs for failed login attempts, successful user logins, and account lockouts.
    """
    # Check if the Windows version is Windows 10
    if check_windows_version() == '10':
        # Use PowerShell to filter security logs for failed login attempts
        command_failed_login = "Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4625} | Select-Object -Property TimeCreated,Message"
        # Use PowerShell to filter security logs for successful logins
        command_successful_login = "Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4624} | Select-Object -Property TimeCreated,Message"
        # Use PowerShell to filter security logs for account lockouts
        command_account_lockout = "Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4625} | Where-Object {$_.Message -like '*Account Lockout*'} | Select-Object -Property TimeCreated,Message"

        # Execute the PowerShell commands
        log_output_failed_login = execute_command(f"powershell -Command \"{command_failed_login}\"")
        log_output_successful_login = execute_command(f"powershell -Command \"{command_successful_login}\"")
        log_output_account_lockout = execute_command(f"powershell -Command \"{command_account_lockout}\"")

        # Print the output
        print("Security log (failed login attempts):\n", log_output_failed_login)
        print("Security log (successful logins):\n", log_output_successful_login)
        print("Security log (account lockouts):\n", log_output_account_lockout)
    else:
        # Inform user that log monitoring is not available on this version of Windows
        print("Log monitoring is not available on this version of Windows.")

def main():
    print("Starting log monitoring...")

    # Perform log monitoring task
    monitor_security_logs()

    print("Log monitoring completed.")

if __name__ == "__main__":
    main()
