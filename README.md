# 🛡️ IP-Bloger

> A lightweight Linux firewall management desktop application built with **Python**, **Tkinter**, and **iptables**.

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Linux](https://img.shields.io/badge/Platform-Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)](https://www.linux.org/)
[![Firewall](https://img.shields.io/badge/Firewall-iptables-red?style=for-the-badge)](https://www.netfilter.org/projects/iptables/index.html)
[![GUI](https://img.shields.io/badge/GUI-Tkinter-2E8B57?style=for-the-badge)](https://docs.python.org/3/library/tkinter.html)

IP-Bloger provides a simple graphical interface for managing Linux firewall rules without requiring users to remember complex `iptables` commands. It supports manual IP blocking, temporary blocks, rule inspection, action logging, and automatic blocking after repeated failed authentication attempts.

> [!WARNING]
> This application changes your system firewall and requires elevated privileges. Test it in a safe environment first. Incorrect rules can interrupt SSH access or other network services.

---

## ✨ Features

- 🚫 **Block IP addresses** manually with optional port and protocol filtering.
- ✅ **Unblock IP addresses** by removing matching `iptables` rules.
- ⏱️ **Temporary blocking** with automatic removal after a configurable duration.
- 🔍 **View active firewall rules** and blocked IP ranges.
- 🤖 **Automatic IP blocking** after repeated failed login attempts.
- 📖 **Authentication-log monitoring** using `/var/log/auth.log`.
- 📝 **Local activity logging** with log viewing, clearing, and export support.
- 🖥️ **Dark-themed Tkinter interface** with interactive controls.

## 🧰 Tech stack

| Technology | Purpose |
| --- | --- |
| [Python 3](https://www.python.org/) | Application logic |
| [Tkinter](https://docs.python.org/3/library/tkinter.html) | Desktop graphical interface |
| [iptables](https://www.netfilter.org/projects/iptables/index.html) | Linux firewall rule management |
| `threading` | Background log monitoring and temporary blocks |

## ✅ Requirements

- Linux operating system
- Python 3.x
- `iptables` installed and available on `PATH`
- Tkinter support for Python
- `sudo` privileges for firewall operations
- Read access to an authentication log, normally `/var/log/auth.log`

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Sandipan2011/IP-Bloger.git
cd IP-Bloger
```

### 2. Install Tkinter

On Debian-based distributions such as Ubuntu, Debian, or Kali Linux:

```bash
sudo apt update
sudo apt install -y python3-tk iptables
```

> Package names may differ on Fedora, Arch, and other distributions. Install the equivalent Python Tkinter package for your system.

### 3. Verify the firewall dependency

```bash
sudo iptables -L
```

## ▶️ Run the application

Start the GUI with elevated privileges because the application executes firewall commands:

```bash
sudo python3 firewall_gui.py
```

## 🖱️ How to use

1. Enter an IP address.
2. Optionally enter a destination port and choose `tcp` or `udp`.
3. Select an action:
   - **Block IP** — add a permanent `DROP` rule.
   - **Unblock IP** — remove the matching `DROP` rule.
   - **Block IP Temporarily** — block an IP for a number of seconds.
   - **View Rules** — display the current `iptables` rules.
   - **View Blocked IP Ranges** — show rules containing `DROP`.
   - **Start Auto IP Block** — monitor authentication failures.
   - **Stop Auto IP Block** — stop background monitoring.
4. Use **Export Log** to save the current output to `firewall_log.txt`.

## 🤖 Automatic blocking

When automatic blocking is enabled, the application follows `/var/log/auth.log` and looks for `Failed password` entries. It extracts IPv4 addresses and tracks failed attempts in memory. An address is automatically blocked after **5 failed attempts** by default.

To change the threshold, update `max_failed_attempts` in `firewall_gui.py`:

```python
max_failed_attempts = 5
```

> [!NOTE]
> Automatic blocking currently expects authentication messages in a format containing `from <IPv4 address>` and is primarily designed for Linux systems that use `/var/log/auth.log`. Systems using another log path or format may require configuration changes.

## 📁 Project structure

```text
IP-Bloger/
├── firewall_gui.py       # Main Tkinter application
├── README.md             # Project documentation
├── docs/
│   └── README.md         # Additional documentation
└── .gitignore
```

## 🔐 Security considerations

- Review every rule before applying it to a production machine.
- Keep a second administrative session available when testing firewall changes remotely.
- Be careful not to block your own management IP address.
- Use `sudo` only when necessary and understand the commands being executed.
- Validate IP addresses, ports, and protocols before using the application.
- Test temporary and automatic blocking in an isolated environment.
- Remember that firewall rules may not persist after a reboot unless your distribution is configured to save them.

## 🐛 Troubleshooting

### Tkinter is unavailable

```bash
sudo apt install -y python3-tk
```

### `iptables` commands fail

Confirm that `iptables` is installed and that the application is started with `sudo`:

```bash
command -v iptables
sudo iptables -L
sudo python3 firewall_gui.py
```

### Authentication-log monitoring does not work

Check that the expected log file exists and is readable:

```bash
ls -l /var/log/auth.log
sudo tail -f /var/log/auth.log
```

Some distributions use `/var/log/secure` or a systemd journal instead. Update the log path and parsing logic in `firewall_gui.py` when necessary.

## 🗺️ Roadmap

- [ ] Add input validation for IP addresses, ports, and protocols.
- [ ] Add configurable authentication-log paths and failure thresholds.
- [ ] Improve support for different Linux authentication-log formats.
- [ ] Add safer privilege handling without running the full GUI as root.
- [ ] Add rule persistence and restoration support.
- [ ] Add automated tests for firewall command construction.

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-change`
3. Make and test your changes in a safe Linux environment.
4. Commit your changes: `git commit -m "Add my change"`
5. Push the branch and open a pull request.

For bugs and feature requests, please open a [GitHub issue](https://github.com/Sandipan2011/IP-Bloger/issues).

## 📄 License

No license file is currently included in the repository. Add a `LICENSE` file before distributing or reusing this project so that permissions are clearly defined.

## ⭐ Support

If IP-Bloger is useful to you, consider starring the repository and sharing feedback through [issues](https://github.com/Sandipan2011/IP-Bloger/issues).
