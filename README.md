# Firewall GUI Controller

A Python-based graphical user interface (GUI) application for managing firewall rules on Linux systems using iptables. This tool allows users to block/unblock IP addresses, view current rules, monitor logs, and automatically block IPs based on failed login attempts.

## Features

- **Manual IP Blocking/Unblocking**: Block or unblock specific IP addresses with optional port and protocol filtering.
- **Temporary Blocking**: Block an IP for a specified duration.
- **View Rules**: Display current iptables rules.
- **Auto Blocking**: Automatically block IPs after a configurable number of failed login attempts (monitors /var/log/auth.log).
- **Logging**: Export and view logs of actions performed.
- **GUI Interface**: User-friendly Tkinter-based interface.

## Requirements

- Python 3.x
- Tkinter (usually included with Python, but install if missing)
- iptables (standard on Linux systems)
- sudo privileges for iptables commands

## Installation

1. **Clone or Download the Repository**:
   ```
   git clone https://github.com/yourusername/firewall-gui-controller.git
   cd firewall-gui-controller
   ```

2. **Install Dependencies** (if needed):
   - On Debian-based systems (like Kali Linux):
     ```
     sudo apt update
     sudo apt install python3-tk
     ```
   - Tkinter is usually pre-installed with Python 3. If not, the above command will install it.

3. **Ensure iptables is available**:
   - iptables is typically installed by default on Linux. Verify with:
     ```
     sudo iptables -L
     ```

## Usage

1. **Run the Application**:
   - To run the GUI:
     ```
     sudo python3 firewall_gui.py
     ```
     **Note**: sudo is required because the script executes iptables commands, which need root privileges.

2. **Using the GUI**:
   - Enter an IP address in the input field.
   - Optionally specify port and protocol (tcp/udp).
   - Click buttons to block/unblock IPs, view rules, etc.
   - For auto-blocking: Click "Start Auto IP Block" to begin monitoring failed login attempts.
   - Logs are displayed in the text area and can be exported to a file.

3. **Auto Blocking Configuration**:
   - The script monitors `/var/log/auth.log` for failed password attempts.
   - After 5 failed attempts from the same IP, it automatically blocks that IP.
   - You can adjust `max_failed_attempts` in the code if needed.

## Important Notes

- **Security**: This tool modifies firewall rules. Use with caution and ensure you understand the implications of blocking IPs.
- **Log File**: The auto-blocking feature reads from `/var/log/auth.log`. Ensure this file exists and is readable.
- **Sudo Requirements**: All iptables commands require sudo. If you prefer not to run the entire script as root, you could modify the code to prompt for password or use sudo only for specific commands.
- **Testing**: Test in a safe environment before using in production.

## Troubleshooting

- If Tkinter is not found: Install with `sudo apt install python3-tk`
- If iptables commands fail: Ensure you have sudo privileges and iptables is installed.
- Permission issues with log file: The script needs read access to `/var/log/auth.log`. If issues arise, check file permissions.

## Contributing

Feel free to submit issues, feature requests, or pull requests.

## License

This project is open-source. Please check the license file for details.
# IP-Bloger
