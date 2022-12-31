# Gauntlet

A tool that uses the Gmail API to send account deletetion requests to sites you want to remove from your digital footprint.

## How it works

Gauntlet takes in a `accounts.csv` file that contains data about different accounts.
Then using the domain name of the account, Gauntlet sends emails to various potential addresses (see full list of email prefixes below) in an attempt to reach the support helpdesk of the website.

Note: It will only send emails for accounts using the same email as it's `username` (see `accounts.csv` structure below).

### Full Email Prefix List
```
"contact",
"support",
"help",
"hello",
"account",
"accounts"
```

## Getting Started

First, clone the repo.
```
git clone https://github.com/helloitsian/gauntlet.git
cd gauntlet
```

Second, get your credentials from Google Developer Console.
1. Create a Project
2. Add the Gmail API to the project
3. Configure an Oauth2 consent screen for **"Desktop Applications"**

Third, create a file called `accounts.csv` in the root directory of this repo.
An easy way to retrieve a file already made for you is to exporter your Chrome/Brave/Chromium passwords and **remove the password column** in an offline spreadsheet editor. 
Then just add the `should_delete` column and go to town!

Uses this structure, **header row names matter**.
The `should_delete` column can contain the values: `y, yes, true, n, no, false` 
Alternatively the script will ask you if you want to delete accounts that don't have a `should_delete` field filled in.

#### accounts.csv structure
| name    | url                 | username           | should_delete |
|---------|---------------------|--------------------|---------------|
| Example | https://example.org | gauntlet@gmail.com | y             |
| Google  | https://google.com  | gauntlet@gmail.com | n             |

### Run on Windows (Powershell)
```
./env/Scripts/activate.ps1
pip install -r requirements.txt
python main.py
```

### Run on Windows (Command Prompt)
```
./env/Scripts/activate.bat
pip install -r requirements.txt
python main.py
```

### Run on Linux & MacOS
```
source /env/bin/activate
pip install -r requirements.txt
python main.py
```

### Oauth2 Authentication

In your terminal you'll receive a URL to sign into your Google Developer Console application with a Google Account. Click on it and sign in, let Gauntlet do the rest.

### Enjoy Your Cleaner Digital Footprint!

A helpfil tip is to create a filter on Gmail for email replies confirming the email Gauntlet tried to send to doesn't exist.
Set the filter to delete the email, this way, your inbox clutter is lessened. 

#### How to set filters in Gmail
[https://support.google.com/mail/answer/6579?hl=en#zippy=](https://support.google.com/mail/answer/6579?hl=en#zippy=)

#### Search term I use

```
is:unread Address not found 
```