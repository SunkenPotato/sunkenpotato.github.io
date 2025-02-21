+++
title = "Storing Passwords in SQL"
date = "2024-09-04T17:09:48+02:00"
author = ""
authorTwitter = "" #do not include @
cover = ""
tags = ["", ""]
keywords = ["", ""]
description = "A hacky way to keep your backup codes and passwords safe"
showFullContent = false
readingTime = false
hideComments = false
+++

## Intro 
I'm sure everyone has had that moment where you create an account
for something and then you have to write down the password somewhere, or store it in a password manager. 

Or, you had to store those backup keys for 2FA, and those are very annoying to remember,
and even when they do give you a file to download, they're always named \
`backup-keys-discord.txt` or something.
Those are really annoying to store in my opinion, and today, since I'm too cheap to use a password manager, \
and too good to write them down, I'm storing in them in an SQL database.

## Setting it up
Since I now use windows, and nobody wants to deal with `cmd` in windows, I fired up WSL and installed PostgreSQL (just my preference). \
At first I had some problems with the installation and starting the server, but it was alright in the end.

So then, I created created a database (amn't I special :)) and connected to it.
```sql
CREATE DATABASE passwords;
\c passwords
```

Once there, I made a table called `passwords` where I plan on (from now on) storing my passwords.
```sql
-- I prefer non-nullables, they're optional though.
CREATE TABLE passwords(
    id SERIAL PRIMARY KEY,
    key TEXT NOT NULL,
    value TEXT NOT NULL
);
-- Just an example
INSERT INTO passwords(key, value) VALUES ('discord.com', '****************');
```
It's very simple, and frankly, I don't think there's any other data to store.

I don't have a table for backup codes yet, since I don't need it, but this is what it could look like: \
We're going to need two tables, one for services that give out backup codes, and the other for the actual backup codes.
```sql
CREATE TABLE backupcode_services(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE backup_codes(
    id SERIAL PRIMARY KEY,
    service INTEGER REFERENCES backupcode_services(id) NOT NULL,
    value TEXT NOT NULL
);

-- Let's create two services
INSERT INTO backupcode_services(name) VALUES ('discord.com'); -- 1
INSERT INTO backupcode_services(name) VALUES ('github.com'); -- 2
-- and some codes
INSERT INTO backup_codes (service, value) VALUES (1, 'aXMgYW55b25lIGdvaW5nIHRvIGRlY29kZSB0aGlzPw==');
INSERT INTO backup_codes (service, value) VALUES (1, 'R29vZCBqb2IsIHlvdSd2ZSBkZWNvZGVkIHR3b1wh');
INSERT INTO backup_codes (service, value) VALUES (2, 'RG8gbWUgYSBmYXZvciBhbmQgam9pbiBteSBkaXNjb3JkIDop')
```
And now, we can filter them by ID / name using SQL's `LEFT JOIN`
```sql
SELECT backup_codes.service, backup_codes.value, backupcode_services.name 
    FROM backup_codes
    LEFT JOIN backupcode_services 
        ON backupcode_services.id=backup_codes.service
    WHERE backupcode_services.name='discord.com'; -- Or by id

-- This returns the following table:
 service |                    value                     |    name     
---------+----------------------------------------------+-------------
       1 | aXMgYW55b25lIGdvaW5nIHRvIGRlY29kZSB0aGlzPw== | discord.com
       1 | R29vZCBqb2IsIHlvdSd2ZSBkZWNvZGVkIHR3b1wh     | discord.com
```
It's not a very nice query, but you could write a function for it, which I'm not going to do here, as this article is **way** longer than usual already.

Is this secure? I don't know, probably a bit.

Is this useful? No, probably not.

Is it **cool**? Yes.


