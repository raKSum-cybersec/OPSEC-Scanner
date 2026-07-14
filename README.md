Here is a complete, production-ready `README.md` file tailored specifically for your project. It consolidates the setup requirements, architecture features, troubleshooting steps for Parrot OS, and usage guides into a clean, professional documentation layout.

---

# 🛡️ High-OPSEC Tor-Routed Network Probing Engine

An advanced, high-stealth network reconnaissance tool designed to perform target and port evaluation over the Tor network. By utilizing strict proxy isolation, programmatic circuit rotation, randomized operating system signatures (TTL), and human-like timing distributions, this scanner minimizes passive and active detection profiles.

---

## ✨ Architectural Features

* **🔄 Programmatic IP Rotation:** Dynamically signals your local Tor daemon to negotiate a brand new circuit and exit node IP before scanning every target and port combination.
* **🔌 Zero-Pool Socket Isolation:** Destroys Python's connection pooling mechanism on every iteration. This forces the host operating system to close old TCP streams immediately and prevents SOCKS5 "Keep-Alive" leak profiles.
* **🐢 Poisson Jitter Delay:** Avoids predictable timing thresholds by utilizing a mathematical Poisson distribution curve to generate irregular, human-like delay intervals between checks.
* **🕶️ Operating System Spoofing:** Randomly alters Socket Time-To-Live (`TTL`) properties (64 vs. 128) on a per-probe basis to emulate different operating systems.
* **⛔ Hard Kill-Switch (Leak Guard):** Establishes your public IP signature before execution. If the proxy fails or a connection leaks natively, the script triggers an emergency shutdown instantly.
* **🎨 Metasploit-Style Randomized Banners:** Features a collection of 20 unique high-OPSEC ASCII art templates rotating dynamically on startup.

---

## 🛠️ Environment Setup & Installation

### 1. System Dependencies Installation

The tool requires a local Tor daemon and development tools to interface with the network control port.

#### For Parrot OS / Kali Linux / Debian / Ubuntu:

```bash
sudo apt update
sudo apt install tor tor-geoipdb torsocks python3-pip python3-venv -y

```

#### For macOS (via Homebrew):

```bash
brew install tor
brew services start tor

```

---

### 2. Python Virtual Environment Configuration

Avoid conflicts with system-wide python environments by running the tool inside an isolated sandbox:

```bash
# Initialize a clean virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

```

#### Dependencies (`requirements.txt`):

```text
certifi==2026.6.17
charset-normalizer==3.4.9
idna==3.18
markdown-it-py==4.2.0
mdurl==0.1.2
numpy==2.5.1
Pygments==2.20.0
PySocks==1.7.1
requests==2.34.2
rich==15.0.0
stem==1.8.2
urllib3==2.7.0

```

---

### 3. Configuring the Tor Daemon (`torrc`)

For the dynamic IP rotation feature to work, you must instruct your local Tor daemon to accept external control commands.

1. Open your Tor configuration file as a superuser:
```bash
sudo nano /etc/tor/torrc

```


2. Scroll to the bottom of the file and add the following lines:
```text
# Bind SOCKS5 proxy local handler
SocksPort 9050

# Open local interface for dynamic circuit rotation
ControlPort 9051

# Authentication Choice:
# Option A: Standard Cookie Authentication (Recommended for Kali/Debian/macOS)
# CookieAuthentication 1

# Option B: Hashed Password Authentication (Required for Parrot OS due to sandboxing)
# Generate your hashed token using: tor --hash-password yourpassword
HashedControlPassword 16:872C55... # <- Replace with your hash output

```


3. Save and close the file (`Ctrl+O`, `Enter`, `Ctrl+X`).
4. Restart your native system service:
```bash
# On Linux:
sudo systemctl restart tor

# On macOS:
brew services restart tor

```



---

### 4. Permissions & OS Specific Troubleshooting

#### Debian / Ubuntu / Kali Linux (Permission Denied)

If your script throws permission errors trying to read Tor's auth cookies, add your system user to the Tor system group:

```bash
sudo usermod -a -G debian-tor $USER

```

> ⚠️ **CRITICAL:** You must log out of your system completely or restart your terminal window for this change to take effect.

#### Parrot OS (SOCKS Socket error 0x01)

Parrot OS manages traffic using **Anonsurf**, which overrides system routing and locks downstream control ports.

1. Turn off Anonsurf temporarily before using this script's independent rotation engine:
```bash
sudo anonsurf stop

```


2. Start standard system Tor:
```bash
sudo systemctl start tor

```



---

## 🚀 Usage Guide

Once your environment is configured, you can launch the scanner directly.

```bash
# Basic run with default staging targets on Ports 80 and 443
python -m opsec_scanner.scanner

# Advanced target and multi-port scanning matrix
python -m opsec_scanner.scanner --targets example.com nmap.org --ports 80 443 22 8080

```

### Argument Reference

* `-t, --targets` : Space-separated list of domain names/URLs to probe.
* `-p, --ports`   : Space-separated list of ports to test on the targets (e.g., `80 443 22`).

---

## 📂 Project Structure

```text
opsec_scanner/
├── __init__.py
├── scanner.py             # Main scanning engine & CLI parsing
├── requirements.txt       # Python dependencies list
└── README.md              # Project documentation (this file)

```

---

## ⚖️ Disclaimer

This tool is designed purely for educational purposes, authorization-verified security audits, and privacy-enhancing system administration verification. Users are solely responsible for ensuring compliance with local laws and network-testing policies. Use responsibly.