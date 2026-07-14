import time
import sys
import socket
import random
import argparse
from datetime import datetime
import numpy as np
import requests
from requests.adapters import HTTPAdapter
import socks
from stem import Signal
from stem.control import Controller

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner

console = Console()

# --- CONFIGURATION & METADATA ---
TOR_SOCKS_PORT = 9050
TOR_CONTROL_PORT = 9051  
DEV_DATE = "July 2026"
DEVELOPERS = "Gemini & raKSum"
DEFAULT_TARGETS = ["example.com", "httpbin.org", "neverssl.com"]
DEFAULT_PORTS = [80, 443]

REAL_EXTERNAL_IP = None


def generate_random_banner():
    """Selects from a massive library of unique high-OPSEC ASCII templates."""
    banners = [
        "        ^__^\n        (oo)\\_______\n        (__)\\       )\\/\\\n            ||----w |\n            ||     ||   > Initializing ghost-route mapping...",
        "  ____  ____   ______ __________ \n / __ \\/ __ \\ / ____// ____/ ___/\n/ / / / /_/ // __/  / __/  \\__ \\ \n/ /_/ / ____// /___ / /___ ___/ /\n\\____/_/    /_____//_____//____/ ",
        "      .---.\n     /     \\\n     \\.微妙./   * Stealth is not an option...\n      |   |     * It is an architectural rule.\n   ---'---'---",
        "    .-''''-.\n   / _    _ \\\n  | (_)  (_) |\n  |    /\\    |\n   \\  ====  /\n    '-____-'   [ SECURE LAYER ACTIVE ]"
    ]
    selected = random.choice(banners)
    meta_text = f"{selected}\n\n[ Codebase: v1.3.0-StrictRotation ]\n[ Team: {DEVELOPERS} | Active Operations Matrix: {DEV_DATE} ]\n"
    return Text(meta_text, style="bold cyan")


def cache_baseline_ip():
    """Establishes the true public IP of the host before activating proxy routing."""
    global REAL_EXTERNAL_IP
    try:
        REAL_EXTERNAL_IP = requests.get("https://api.ipify.org", timeout=5).text
    except Exception:
        console.print("[bold red][!] CRITICAL: Could not establish baseline real IP. Network unreachable. Aborting.[/bold red]")
        sys.exit(1)


# --- DYNAMIC CONTROLLER ROTATION WITH ENFORCED SLEEP ---
def renew_tor_circuit(live_context):
    """Signals Tor to cycle identities using explicit Parrot OS password strings."""
    try:
        with Controller.from_port(port=TOR_CONTROL_PORT) as controller:
            # CHANGED: Authenticate using the explicit password string instead of blank cookies
            controller.authenticate(password="parrot") 
            
            wait_time = controller.get_newnym_wait()
            if wait_time > 0:
                for remaining in range(int(wait_time) + 1, 0, -1):
                    live_context.update(Spinner("dots", text=Text(f" [Tor] Rate limit active. Syncing circuit tracks ({remaining}s)...", style="bold yellow")))
                    time.sleep(1)
            
            controller.signal(Signal.NEWNYM)
    except Exception as e:
        # This will now display clearly if something else is blocking it
        console.print(f"\n[bold dim yellow][!][Tor Control Port Error]: {e}[/bold dim yellow]\n")


# --- ANTI-POOLING LEAK GUARD ---
def verify_leak_guard():
    """Verifies that the proxy is operational using a single-use connection session."""
    proxies = {
        'http': f'socks5h://127.0.0.1:{TOR_SOCKS_PORT}',
        'https': f'socks5h://127.0.0.1:{TOR_SOCKS_PORT}'
    }
    
    # CRITICAL: We spin up a completely isolated Session and destroy the connection pool max size
    session = requests.Session()
    adapter = HTTPAdapter(pool_connections=1, pool_maxsize=1)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    try:
        # Force HTTP headers to close the session explicitly
        current_ip = session.get(
            "https://api.ipify.org", 
            proxies=proxies, 
            headers={'Connection': 'close'}, 
            timeout=5
        ).text
        session.close() # Shred the socket instantly
        
        if current_ip == REAL_EXTERNAL_IP:
            return False, "Leak Detected: Proxy bypassed natively!"
        return True, current_ip
    except Exception:
        return False, "Proxy connection dead/unresponsive."


def passive_preflight_check(domain):
    """Confirms domain validity without touching the target server directly."""
    proxies = {
        'http': f'socks5h://127.0.0.1:{TOR_SOCKS_PORT}',
        'https': f'socks5h://127.0.0.1:{TOR_SOCKS_PORT}'
    }
    try:
        url = f"https://dns.google/resolve?name={domain}"
        response = requests.get(url, proxies=proxies, timeout=5)
        if response.status_code == 200 and "Answer" in response.json():
            return True
        return False
    except Exception:
        return False


def calculate_poisson_delay(lam=4.0):
    """Generates an organic behavioral delay profile mimicking human activity gaps."""
    delay = np.random.poisson(lam)
    return max(2.5, float(delay) + random.uniform(0.1, 0.9))


def apply_stealth_socket_options(s):
    """Spoofs Time-To-Live (TTL) to simulate varying operating systems."""
    spoofed_ttl = random.choice([64, 128])
    s.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, spoofed_ttl)
    return spoofed_ttl


# --- CORE SCANNING ENGINE ---
def execute_bulletproof_scan(targets=None, ports=None):
    cache_baseline_ip()
    
    console.print(Panel(generate_random_banner(), border_style="red", padding=(1, 2)))
    
    hosts_pool = list(targets) if targets else list(DEFAULT_TARGETS)
    ports_pool = list(ports) if ports else list(DEFAULT_PORTS)
    
    pairs_pool = []
    for host in hosts_pool:
        for port in ports_pool:
            pairs_pool.append((host, port))
            
    random.shuffle(pairs_pool)
    results = []

    with Live(Spinner("dots", text="Initializing Safeguards..."), refresh_per_second=10, console=console) as live:
        for target_host, target_port in pairs_pool:
            
            # Pass the live visual context straight into the circuit controller
            live.update(Spinner("dots", text=Text(f" [Tor] Requesting brand new identity...", style="bold purple")))
            renew_tor_circuit(live)

            # 1. Run Kill Switch Guard Checking (Now drops sockets immediately)
            live.update(Spinner("runner", text=Text(" [Guard] Verifying proxy containment & IP masking...", style="bold green")))
            secure, status_or_ip = verify_leak_guard()
            if not secure:
                live.stop()
                console.print(f"\n[bold red][███] EMERGENCY STOP activated: {status_or_ip}[/bold red]\n")
                sys.exit(1)
            
            # 2. Run Passive Pre-Flight Checklist
            live.update(Spinner("dots", text=Text(f" [Passive] Querying global records for {target_host}...", style="cyan")))
            is_alive = passive_preflight_check(target_host)
            if not is_alive:
                console.print(f"[{datetime.now().strftime('%H:%M:%S')}] [bold dim yellow][!][/bold dim yellow] Host {target_host} failed passive validation. Skipping.")
                continue

            # 3. Apply Poisson Jitter Wait
            delay = calculate_poisson_delay(lam=3)
            live.update(Spinner("runner", text=Text(f" [Poisson] Enforcing pacing gap ({delay:.2f}s)...", style="yellow")))
            time.sleep(delay)

            # 4. Connect with Dynamic TTL Options via SOCKS5h
            live.update(Spinner("dots", text=Text(f" [Routing] Opening spoofed tunnel to {target_host}:{target_port}...", style="purple")))
            
            socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", TOR_SOCKS_PORT, rdns=True)
            socket.socket = socks.socksocket

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4.0)
            
            active_ttl = apply_stealth_socket_options(s)

            try:
                s.connect((target_host, int(target_port)))
                status_str = "[bold green]OPEN / RESPONDING[/bold green]"
                console.print(f"[{datetime.now().strftime('%H:%M:%S')}] [bold green][+][/bold green] Host: {target_host:<18} Port: {target_port:<5} Status: {status_str}")
                s.close()
            except Exception:
                status_str = "[bold dim red]FILTERED / CLOSED[/bold dim red]"
                console.print(f"[{datetime.now().strftime('%H:%M:%S')}] [bold dim red][-][/bold dim red] Host: {target_host:<18} Port: {target_port:<5} Status: {status_str}")

            results.append((target_host, target_port, status_or_ip, active_ttl, status_str))

        live.update(Text("🎉 Complete target matrix processed safely.", style="bold green"))

    # Summary Generation Matrix
    summary_table = Table(title="\n[bold reverse] Post-Operation Metrics Summary [/bold reverse]", title_style="bold gold1", box=None)
    summary_table.add_column("Assigned Host", style="cyan")
    summary_table.add_column("Target Port", style="orange1", justify="center")
    summary_table.add_column("Exit Broker Identity", style="purple")
    summary_table.add_column("Spoofed TTL", style="orange1", justify="center")
    summary_table.add_column("Operational Status")

    for row in results:
        summary_table.add_row(row[0], str(row[1]), row[2], str(row[3]), row[4])

    console.print("\n")
    console.print(Panel(summary_table, border_style="gold1"))


def main():
    """Handles the CLI interface layer parsing."""
    parser = argparse.ArgumentParser(
        description="🛡️ High-OPSEC Tor-Routed Network Probing Engine.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-t', '--targets', nargs='+', help="Custom list of domains.")
    parser.add_argument('-p', '--ports', nargs='+', type=int, help="List of application ports.")
    args = parser.parse_args()

    try:
        execute_bulletproof_scan(targets=args.targets, ports=args.ports)
    except KeyboardInterrupt:
        console.print("\n[bold red][!] Intercept received. Clearing execution buffers safely.[/bold red]")
        sys.exit(0)


if __name__ == "__main__":
    main()