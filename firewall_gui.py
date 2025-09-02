import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import time
import threading
import os
import re

# ----------- VARIABLES FOR AUTO BLOCKING -----------
blocked_ips = set()
failed_attempts = {}
max_failed_attempts = 5
auto_block_running = False
log_monitor_thread = None

# ----------- FUNCTIONS -----------

def export_log():
    try:
        with open("firewall_log.txt", "w") as file:
            file.write(output_text.get("1.0", tk.END))
        messagebox.showinfo("Export Successful", "Log has been exported to 'firewall_log.txt'")
    except Exception as e:
        messagebox.showerror("Export Error", str(e))

def block_ip():
    ip = ip_entry.get()
    port = port_entry.get()
    protocol = protocol_var.get()
    if ip:
        cmd = ["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"]
        if port and protocol:
            cmd = ["sudo", "iptables", "-A", "INPUT", "-s", ip, "-p", protocol, "--dport", port, "-j", "DROP"]
        subprocess.run(cmd)
        output_text.insert(tk.END, f"❌ Blocked IP: {ip}\n")
        output_text.see(tk.END)

def unblock_ip():
    ip = ip_entry.get()
    port = port_entry.get()
    protocol = protocol_var.get()
    if ip:
        cmd = ["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"]
        if port and protocol:
            cmd = ["sudo", "iptables", "-D", "INPUT", "-s", ip, "-p", protocol, "--dport", port, "-j", "DROP"]
        subprocess.run(cmd)
        output_text.insert(tk.END, f"✅ Unblocked IP: {ip}\n")
        output_text.see(tk.END)

def view_rules():
    rules = subprocess.getoutput("sudo iptables -L")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"🔥 Current Rules:\n{rules}\n")
    output_text.see(tk.END)

def view_blocked_ranges():
    ranges = subprocess.getoutput("sudo iptables -L INPUT -v -n | grep DROP")
    output_text.insert(tk.END, f"\n🔍 Blocked IP Ranges:\n{ranges}\n")
    output_text.see(tk.END)

def block_ip_temporarily():
    ip = ip_entry.get()
    duration = duration_entry.get()
    if ip and duration.isdigit():
        try:
            subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
            output_text.insert(tk.END, f"⏱️ Temporarily blocked IP {ip} for {duration} seconds.\n")
            output_text.see(tk.END)

            def unblock_after_delay():
                time.sleep(int(duration))
                subprocess.run(["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"])
                output_text.insert(tk.END, f"✅ IP {ip} automatically unblocked after {duration} seconds.\n")
                output_text.see(tk.END)

            threading.Thread(target=unblock_after_delay, daemon=True).start()

        except Exception as e:
            messagebox.showerror("Error", str(e))

def view_log():
    try:
        with open("firewall_log.txt", "r") as file:
            content = file.read()
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, content)
        output_text.see(tk.END)
    except FileNotFoundError:
        messagebox.showwarning("Not Found", "No log file found.")

def clear_log():
    output_text.delete("1.0", tk.END)

def refresh_rules():
    output_text.insert(tk.END, "\n🔁 Rules refreshed.\n")
    view_rules()

# ----------- AUTO BLOCKING FUNCTIONS -----------

def extract_ip(log_line):
    match = re.search(r'from (\d+\.\d+\.\d+\.\d+)', log_line)
    if match:
        return match.group(1)
    return None

def block_ip_automatically(ip):
    if ip not in blocked_ips:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
        blocked_ips.add(ip)
        output_text.insert(tk.END, f"🛑 Automatically blocked IP: {ip}\n")
        output_text.see(tk.END)

def monitor_auth_log():
    global auto_block_running
    logfile = "/var/log/auth.log"  # আপনার সিস্টেম অনুসারে পরিবর্তন করতে পারেন
    try:
        with subprocess.Popen(['tail', '-F', logfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
            while auto_block_running:
                line = proc.stdout.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                if "Failed password" in line:
                    ip = extract_ip(line)
                    if ip:
                        failed_attempts[ip] = failed_attempts.get(ip, 0) + 1
                        output_text.insert(tk.END, f"⚠️ Failed login attempt from {ip} (Count: {failed_attempts[ip]})\n")
                        output_text.see(tk.END)
                        if failed_attempts[ip] >= max_failed_attempts and ip not in blocked_ips:
                            block_ip_automatically(ip)
    except Exception as e:
        output_text.insert(tk.END, f"❗ Error monitoring log: {e}\n")
        output_text.see(tk.END)

def start_auto_block():
    global auto_block_running, log_monitor_thread
    if not auto_block_running:
        auto_block_running = True
        log_monitor_thread = threading.Thread(target=monitor_auth_log, daemon=True)
        log_monitor_thread.start()
        output_text.insert(tk.END, "▶️ Auto IP Blocking Started.\n")
        output_text.see(tk.END)
    else:
        messagebox.showinfo("Info", "Auto Blocking is already running.")

def stop_auto_block():
    global auto_block_running
    if auto_block_running:
        auto_block_running = False
        output_text.insert(tk.END, "⏸️ Auto IP Blocking Stopped.\n")
        output_text.see(tk.END)
    else:
        messagebox.showinfo("Info", "Auto Blocking is not running.")

# ----------- GUI Setup -----------
root = tk.Tk()
root.title("Firewall Controller with Logging & Auto Block")
root.configure(bg="#222222")

# ----------- Fonts -----------
entry_font = ("Segoe UI", 11)
label_font = ("Segoe UI", 11)

# ----------- Labels and Entries -----------
tk.Label(root, text="Enter IP Address:", fg="#00FF00", bg="#222222", font=label_font).pack(pady=(10, 2))
ip_entry = tk.Entry(root, width=30, font=entry_font)
ip_entry.pack(pady=5)

tk.Label(root, text="Enter Port (optional):", fg="#00FF00", bg="#222222", font=label_font).pack(pady=(10, 2))
port_entry = tk.Entry(root, width=30, font=entry_font)
port_entry.pack(pady=5)

tk.Label(root, text="Duration (in seconds):", fg="#00FF00", bg="#222222", font=label_font).pack(pady=(10, 2))
duration_entry = tk.Entry(root, font=entry_font)
duration_entry.pack(pady=5)

tk.Label(root, text="Select Protocol (optional):", fg="#00FF00", bg="#222222", font=label_font).pack(pady=(10, 2))
protocol_var = tk.StringVar(value="")
protocol_dropdown = tk.OptionMenu(root, protocol_var, "", "tcp", "udp")
protocol_dropdown.config(bg="#444444", fg="white", font=("Segoe UI", 10))
protocol_dropdown.pack(pady=5)

# ----------- Stylish Button Function -----------
def styled_button(master, text, command, bg, fg, hover_bg):
    btn = tk.Button(master, text=text, command=command,
                    font=("Segoe UI", 10, "bold"),
                    bg=bg, fg=fg,
                    activebackground=hover_bg, activeforeground=fg,
                    relief="flat", bd=0,
                    padx=10, pady=5,
                    cursor="hand2")
    btn.pack(pady=5, ipadx=5, ipady=2)
    def on_enter(e): btn.config(bg=hover_bg)
    def on_leave(e): btn.config(bg=bg)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

# ----------- Buttons -----------
styled_button(root, "Export Log", export_log, "#FFD700", "black", "#FFC300")
styled_button(root, "Block IP", block_ip, "#FF4444", "white", "#CC0000")
styled_button(root, "Unblock IP", unblock_ip, "#44FF44", "black", "#22CC22")
styled_button(root, "View Rules", view_rules, "#5555FF", "white", "#3333CC")
styled_button(root, "View Blocked IP Ranges", view_blocked_ranges, "#FFA500", "black", "#FF8800")
styled_button(root, "Block IP Temporarily", block_ip_temporarily, "#FF8888", "white", "#FF6666")
styled_button(root, "View Log", view_log, "#FFAA33", "black", "#FF9900")
styled_button(root, "Clear Log", clear_log, "#AA55FF", "white", "#9933FF")
styled_button(root, "Refresh Rules", refresh_rules, "#00CED1", "black", "#20B2AA")
styled_button(root, "Start Auto IP Block", start_auto_block, "#33AA33", "white", "#228822")
styled_button(root, "Stop Auto IP Block", stop_auto_block, "#AA3333", "white", "#882222")

# ----------- Output Text Box -----------
output_text = scrolledtext.ScrolledText(root, width=65, height=15,
                                        bg="#111111", fg="#00FF00", insertbackground="white",
                                        font=("Consolas", 10))
output_text.pack(pady=15)

# ----------- Mainloop -----------
root.mainloop()
