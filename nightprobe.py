import os
import socket
import base64
from time import sleep

console = None

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich import box
    console = Console()
except ModuleNotFoundError:
    print("[!] 'rich' module not found. Please install it with: pip install rich")
    exit()

def print_banner():
    banner = """
  ▐ ▄ ▪   ▄▄ •  ▄ .▄▄▄▄▄▄ ▄▄▄·▄▄▄        ▄▄▄▄· ▄▄▄ .
•█▌▐███ ▐█ ▀ ▪██▪▐█•██  ▐█ ▄█▀▄ █·▪     ▐█ ▀█▪▀▄.▀·
▐█▐▐▌▐█·▄█ ▀█▄██▀▐█ ▐█.▪ ██▀·▐▀▀▄  ▄█▀▄ ▐█▀▀█▄▐▀▀▪▄
██▐█▌▐█▌▐█▄▪▐███▌▐▀ ▐█▌·▐█▪·•▐█•█▌▐█▌.▐▌██▄▪▐█▐█▄▄▌
▀▀ █▪▀▀▀·▀▀▀▀ ▀▀▀ · ▀▀▀ .▀   .▀  ▀ ▀█▄▀▪·▀▀▀▀  ▀▀▀ """
    console.print(banner, style="bold red")
    console.print(Panel("[red]NightProbe[/red] - Tactical Red Team Toolkit", box=box.DOUBLE, style="bold red"))

def recon_scanner():
    target = console.input("[bold red][*] Enter target IP/Domain: [/bold red]")
    ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389]
    console.print(f"\n[bold red]Scanning {target}...[/bold red]\n")
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target, port))
        if result == 0:
            console.print(f"[green][+] Port {port} is open[/green]")
        sock.close()

def payload_encoder():
    payload = console.input("[bold red][*] Enter the payload to encode: [/bold red]")
    encoded = base64.b64encode(payload.encode()).decode()
    console.print(f"[green]\n[+] Base64 Encoded Payload: {encoded}[/green]")

def hash_cracker():
    hash_value = console.input("[bold red][*] Enter the hash to crack: [/bold red]")
    wordlist = console.input("[bold red][*] Enter path to wordlist file: [/bold red]")
    algo = console.input("[bold red][*] Algorithm (md5/sha1/sha256): [/bold red]").lower()

    import hashlib
    try:
        with open(wordlist, 'r') as f:
            for line in f:
                word = line.strip()
                if algo == 'md5':
                    hashed = hashlib.md5(word.encode()).hexdigest()
                elif algo == 'sha1':
                    hashed = hashlib.sha1(word.encode()).hexdigest()
                elif algo == 'sha256':
                    hashed = hashlib.sha256(word.encode()).hexdigest()
                else:
                    console.print("[red]Unsupported algorithm.[/red]")
                    return

                if hashed == hash_value:
                    console.print(f"[green][+] Match found: {word}[/green]")
                    return
            console.print("[yellow][-] No match found in wordlist.[/yellow]")
    except FileNotFoundError:
        console.print("[red]Wordlist file not found.[/red]")

def whois_lookup():
    import whois
    domain = console.input("[bold red][*] Enter domain for WHOIS lookup: [/bold red]")
    try:
        info = whois.whois(domain)
        console.print(f"[green]{info}[/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def subdomain_finder():
    domain = console.input("[bold red][*] Enter domain to scan for subdomains: [/bold red]")
    wordlist = console.input("[bold red][*] Enter path to subdomain wordlist: [/bold red]")
    try:
        with open(wordlist, 'r') as f:
            for sub in f:
                sub = sub.strip()
                full_domain = f"{sub}.{domain}"
                try:
                    socket.gethostbyname(full_domain)
                    console.print(f"[green][+] Found: {full_domain}[/green]")
                except:
                    pass
    except FileNotFoundError:
        console.print("[red]Wordlist file not found.[/red]")

def menu():
    while True:
        console.print("\n[bold red]Select an option:[/bold red]", style="bold red")
        console.print("[1] Recon Scanner")
        console.print("[2] Payload Encoder")
        console.print("[3] Hash Cracker")
        console.print("[4] Subdomain Finder")
        console.print("[5] WHOIS Lookup")
        console.print("[6] Exit")
        choice = console.input("[bold red][>>] Choice: [/bold red]")

        if choice == '1':
            recon_scanner()
        elif choice == '2':
            payload_encoder()
        elif choice == '3':
            hash_cracker()
        elif choice == '4':
            subdomain_finder()
        elif choice == '5':
            whois_lookup()
        elif choice == '6':
            console.print("[bold red]Exiting NightProbe...[/bold red]")
            sleep(1)
            break
        else:
            console.print("[red]Invalid option![/red]")

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()
    menu()
