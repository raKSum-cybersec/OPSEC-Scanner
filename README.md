# 🛡️ High-OPSEC Tor-Routed Network Scanner

A stealth-focused, highly resilient network reconnaissance and application probing framework built to completely disrupt behavioral signature analysis and timing-based IDS tracking.

Developed by **Gemini & raKSum** • *July 2026*

---

## 🌟 Advanced OPSEC Features Included

Unlike traditional scanning utilities that generate heavy, sequential packet spikes, this framework utilizes a four-tier defense architecture:

* **Proxy Leak-Guard (Kill Switch):** Pre-flights every single probe by checking its routing state against a cached baseline IP. If Tor drops out or leaks your true external IP, the framework triggers an instantaneous, hard exit.
* **Poisson-Distributed Jitter:** Replaces predictable linear random delays with a natural mathematical distribution curve. Probes are bunched into erratic clusters and long "think-time" pauses, effectively mimicking organic human web browsing patterns.
* **Passive Pre-Flight Checks:** Queries historical, global DNS replication caches over Tor to confirm a host's existence *before* initiating a direct port handshake—preventing dead-host infrastructure alerts.
* **Dynamic Layer-3 TTL Spoofing:** Randomly alters the Time-to-Live (`TTL`) socket header options between common operating system signatures (e.g., Windows vs. Linux) on a per-probe basis.
* **SOCKS5h Remote Name Resolution:** Prevents local DNS leakage by completely disabling local host lookup. All destination URL hostnames are securely passed across the proxy stream to be resolved at the final Tor Exit Node.

---

## 🚀 Installation & Setup

### Prerequisites

You must have the Tor daemon installed locally and configured to accept controller signals.

#### 1. Install Tor Daemon
* **Debian/Ubuntu:** `sudo apt install tor`
* **macOS (Homebrew):** `brew install tor`

#### 2. Configure the Tor Control Port
Open your `torrc` file (typically found at `/etc/tor/torrc` or `/usr/local/etc/tor/torrc`) and ensure the following options are uncommented and active:
```text
ControlPort 9051
CookieAuthentication 1