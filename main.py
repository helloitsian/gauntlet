# python modules
import re
import base64
import time
from email.mime.text import MIMEText
# vendor
import pandas
import tldextract
# google vendor
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# google constants
GOOGLE_CREDENTIALS_PATH = "credentials.json"
GOOGLE_SCOPES = ['https://mail.google.com/']
# constants
ACCOUNTS_CSV_PATH = r"./accounts.csv"

def build_gmail_service(credentials):
  return build("gmail", "v1", credentials = credentials)

def google_authenticate():
  flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CREDENTIALS_PATH, GOOGLE_SCOPES)
  credentials = flow.run_local_server(port=0)

  return credentials

def send_email(gmail_service, message):
  raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
  return gmail_service.users().messages().send(
    userId="me",
    body={ "raw": raw }
  ).execute()

def send_emails(messages):
  message_index = 0
  for message in messages:
    message_index += 1
    print("Sending email {}/{}...".format(message_index, len(messages)))
    time.sleep(5)
    send_email(gmail_service, message)

def build_emails(email_objects):
  emails = []

  for obj in email_objects:
    for to in obj["to"]:
      email = MIMEText(obj["body"])
      email["to"] = to
      email["from"] = obj["from"]
      email["subject"] = obj["subject"]

      emails.append(email)
  
  return emails

def create_email_to_list(domain):
  email_prefixes = [
    "contact",
    "support",
    "help",
    "hello",
    "account",
    "accounts",
  ]

  email_tos = []

  for prefix in email_prefixes:
    email_tos.append(prefix + "@" + domain)

  return email_tos

def create_email_body(target_domain, email):
  return "Hello, I'd like to delete my account for {} under the email: {}".format(target_domain, email)

def create_email_objects(to_delete):
  email_objects = []

  for key in to_delete:
    item = to_delete[key]
    domain = item["domain"]
    email = item["username"]

    email_senders = create_email_to_list(domain)
    email_subject = "Account Deletion for {}".format(email)
    email_body = create_email_body(domain, email)

    email_objects.append({
      "from": email,
      "to": email_senders,
      "subject": email_subject,
      "body": email_body
    })

  return email_objects

def get_domain_name(url):
  url_list = tldextract.extract(url)
  
  domain_list = url_list.domain.split('.')
  parent_domain = domain_list[len(domain_list) - 1]

  return parent_domain + "." + url_list.suffix

def ask_should_delete(name, domain, username):
  answer = input("Should we delete name: '{}' @ '{}' with username '{}'? (y/n) ".format(name, domain, username))

  if (answer == "y"):
    return True
  elif(answer == "n"):
    return False
  else:
    ask_should_delete()

def main():
  google_credentials = google_authenticate()
  gmail_service = build_gmail_service(google_credentials)
  
  user_email = gmail_service.users().getProfile(userId='me').execute()["emailAddress"]

  csv_file = pandas.read_csv(ACCOUNTS_CSV_PATH).to_dict()

  to_delete = {}

  account_index = 0

  for key in csv_file["name"]:
    index = key
    name = csv_file["name"][index]
    url = csv_file["url"][index]
    username = csv_file["username"][index]
    should_delete_field = csv_file["should_delete"][index]

    account_index += 1
    print("Account {}/{}".format(account_index, len(csv_file["name"])))
    
    if (not should_delete_field or (type(should_delete_field) != str)):
      if username == user_email:
        domain = get_domain_name(url)

        if (domain in to_delete):
          continue
        else:
          should_delete = ask_should_delete(name, domain, username)

          if should_delete:
            to_delete[domain] = { "name": name, "url": url, "domain": domain, "username": username }
            print("Added '{}' to accounts to delete!".format(domain))
    elif(should_delete_field == "y" or should_delete_field == "yes" or should_delete_field == "true"):
      if username == user_email:
        domain = get_domain_name(url)

        if (domain in to_delete):
          continue
        else:
          to_delete[domain] = { "name": name, "url": url, "domain": domain, "username": username }
          print("Added '{}' to accounts to delete!".format(domain))

  email_objects = create_email_objects(to_delete)
  emails = build_emails(email_objects)
  send_emails(emails)

  print("Emails finished sending! Enjoy your cleaner digital footprint :)")

if __name__ == "__main__":
  main()