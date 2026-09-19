# IP-Bloger

A Linux firewall management desktop application built with Python and Tkinter for monitoring, blocking, and managing suspicious IP addresses from a simple graphical interface.

IP-Bloger helps administrators quickly respond to repeated failed login attempts, view active firewall rules, and apply temporary or permanent IP blocks without needing to memorize iptables syntax.

## Why this project exists

Managing Linux firewall rules from the command line can be tedious and error-prone, especially when you need to:

- block an IP manually during an incident
- temporarily restrict access for a short duration
- respond to repeated SSH or authentication failures
- review the current state of iptables rules
- keep a lightweight local log of firewall-related actions

IP-Bloger brings these workflows into a single desktop app designed for fast operational use on Linux systems.

## Features

- Manual IP blocking and unblocking
- Temporary IP block support with configurable duration
- View current iptables rules in the app
- Filter by port and protocol when needed
- Automatic blocking based on repeated failed login attempts
- Monitoring of authentication logs for suspicious activity
- Local event log export support
- Clean Tkinter-based user interface for Linux environments

## Supported use cases

- Securing SSH or remote access endpoints
- Responding to repeated brute-force login attempts
- Filtering traffic for a specific IP or protocol
- Reviewing firewall policy changes from one place

## Requirements

- Linux operating system with iptables installed
- Python 3.x
- Tkinter support for Python
- Root or sudo privileges for firewall operations
- Read access to authentication logs such as /var/log/auth.log

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Sandipan2011/IP-Bloger.git
   cd IP-Bloger
   ```

2. Install Tkinter if it is not already available:

   ```bash
   sudo apt update
   sudo apt install python3-tk
   ```

3. Verify that iptables is present:

   ```bash
   sudo iptables -L
   ```

## Running the application

Start the GUI with sudo so the firewall commands can be executed successfully:

```bash
sudo python3 firewall_gui.py
```

## How to use it

1. Enter an IP address in the interface.
2. Optionally provide a port and protocol.
3. Click the action you want:
   - Block IP
   - Unblock IP
   - View Rules
   - View Blocked IP Ranges
   - Block Temporarily
   - Start Auto IP Block
4. Review the output log and export it if needed.

## Auto-blocking behavior

The app can monitor authentication logs for repeated failed attempts and automatically block suspicious IP addresses after a threshold is reached. This is useful against brute-force login patterns and repeated credential abuse.

By default, the script watches for failed password attempts and blocks an IP after several occurrences.

## Security considerations

This project interacts directly with your system firewall. Use it carefully and only on systems where you understand the consequences of blocking traffic.

Important notes:

- Use sudo responsibly.
- Test on a safe or controlled environment before production use.
- Confirm that iptables is installed and configured correctly.
- Make sure the log file being monitored is readable.

## Project layout

```text
IP-Bloger/
├── firewall_gui.py
├── README.md
├── .gitignore
└── docs/
    └── README.md
```

## Roadmap ideas

- Add a settings panel for configurable thresholds and log paths
- Add a clearer rule history and filtering view
- Improve the auto-blocking logic for multiple log formats
- Add a non-root execution mode with safer privilege handling
- Strengthen validation for user input and iptables commands

## Contributing

Contributions are welcome. If you want to improve the GUI, add features, or fix issues, feel free to open a pull request or share suggestions.

## License

This project is open for use and modification. Please check the repository for the current license details before using it in a production or commercial environment.

## Acknowledgements

This project was built to simplify Linux firewall administration and make remediation workflows easier for users who prefer a visual interface over raw terminal commands.
