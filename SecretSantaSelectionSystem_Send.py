import sys, csv, smtplib, ssl, re, getpass, datetime

print("*** Secret Santa Selection System: Send ***")
print()

if len(sys.argv) != 3 or (len(sys.argv) >= 2 and sys.argv[1].lower() in ["?", "-?", "/?", "-h", "/h"]):
    print("Usage: SecretSantaSelectionSystem_Send santa_file go|dry")
    exit()

if sys.argv[2].lower() not in ["go", "dry"]:
    print("The last command-line argument must be 'go' to send emails or 'dry' for a dry-run")
    exit()

input_filename = sys.argv[1]
DRY_RUN = (sys.argv[2].lower() != "go")

print(f"INPUT : {input_filename}")
print(f"ACTION: {('dry run' if DRY_RUN else 'GO!')}")
print()

year = datetime.datetime.now().year

# --------------------------------------------------------------------------------

config_vars = {}

with open("SecretSanta_CONFIG.txt", "r") as config_file:
    for line in config_file:
        key, val = line.partition("=")[::2]
        config_vars[key.strip()] = val.strip()

smtp_server = config_vars["smtp_server"]
from_address = config_vars["from_address"]
from_name = config_vars["from_name"]
saved_password = config_vars["password"]
from_name_and_address = f"{from_name} <{from_address}>" if from_name != "" else from_address

message_template = """\
From: {from_name_and_address}
To: {to_name_and_address}
Subject: {to_name}, Your {year} Family Secret Santa Info

Hi {to_name}!

This year you are the Secret Santa for...

***  {recv_name}  ***

Merry Christmas!"""

# --------------------------------------------------------------------------------

def get_family_info(family_filename):
    family = {}
    print("Checking family info (names, email addresses)...")
    check1_errors = 0
    with open(family_filename, "r") as family_file:
        # please note that the email regular expression used below is very basic!
        email_regex = "^[A-Za-z0-9]+[\._]?[A-Za-z0-9]+[@]\w+[.]\w{2,3}$"
        reader = csv.reader(family_file)
        unique_names = set()
        for key_name, to_name, to_address, _ in reader:
            key_name = key_name.strip()
            to_name = key_name if to_name.strip() == "" else to_name.strip()
            to_address = to_address.strip()
            if key_name == "":
                print(" ! empty (key) name found in list")
                exit()
            elif key_name.lower() in unique_names:
                print(f" ! duplicate (key) name found in list: {key_name}")
                exit()
            elif to_address == "":
                check1_errors += 1
                print(f" ? {key_name} [{to_name}]: missing email address")
            elif not re.search(email_regex, to_address):
                check1_errors += 1
                print(f" ? {key_name} [{to_name}]: bad email address: {to_address}")
            else:
                family[key_name] = { "to_name": to_name, "to_address": to_address }
                print(f" . {key_name} [{to_name}]: OK ({to_address})")
            unique_names.add(key_name.lower())
    print()
    return family

def check_details_and_write_emails(santa_filename, family):
    emails = []
    print("Checking details and writing emails to be sent to...")
    check2_errors = 0
    with open(santa_filename, "r") as santa_file:
        reader = csv.reader(santa_file)
        for santa_name, buying_for, recv_name in reader:
            if santa_name in family:
                email = write_email(family, santa_name, recv_name)
                emails.append(email)
                print(f" * {santa_name} at {email['to_address']}")
            else:
                check2_errors += 1
                print(f" ! Can't send to {santa_name} due to email address issue")
    if check2_errors > 0:
        print()
        print("Errors detected; send halted.")
        exit()
    print()
    return emails

def write_email(family, santa_name, recv_name):
    member = family[santa_name]
    to_name = member["to_name"]
    to_address = member["to_address"]
    return { 
        "santa_name": santa_name,
        "to_address": member["to_address"], 
        "msg_body": message_template.format(
            from_name_and_address=from_name_and_address,
            to_name_and_address=f"{to_name} <{to_address}>", 
            year=year,
            to_name=to_name,
            recv_name=recv_name
        )
    }

def send_emails(emails, password):
    if len(emails) == 0:
        return
    smtp_port = 587  # starttls
    send_count = 0
    context = ssl.create_default_context()
    try:
        print("Sending emails now...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()  # needed?
            server.starttls(context=context)
            server.ehlo()  # needed?
            server.login(from_address, password)
            for email in emails:
                santa_name = email["santa_name"]
                to_address = email["to_address"]
                print(f" * Sending email to {santa_name} at {to_address} ...")
                server.sendmail(from_address, to_address, email["msg_body"])
                print("   OK")
                send_count += 1
            server.quit() 
    except Exception as e:
        print(e)
    print()
    print(f"Done: {send_count} email{('s' if send_count != 1 else '')} sent.")

def dry_run(emails):
    print("*******")
    print("DRY RUN")
    print("*******")
    print()
    for email in emails:
        print(email["msg_body"])
        print()
        print("-" * 72)
        print()

def go_time(emails):
    if len(emails) == 0:
        print("No emails provided to be sent")
        return
    if smtp_server.strip() == "":
        print("! smtp_server not set")
        exit()
    print(f"SMTP: {smtp_server}")
    print(f"From: {from_name_and_address}")
    print()
    if saved_password == "":
        print("Type your password and press ENTER (or leave blank to halt):")
        password = getpass.getpass("")
        if password == "" or password == "q" or password == "Q":
            print("Halting.")
            exit()
    else:
        password = saved_password
    print("READY? Type go and press ENTER (or leave blank to halt):")
    go = input()
    if go != "go":
        print("Halting.")
        exit()
    print()
    send_emails(emails, password)

def run(family_filename):
    family = get_family_info(family_filename)
    emails = check_details_and_write_emails(input_filename, family)
    if DRY_RUN:
        dry_run(emails)
    else:
        go_time(emails)

# --------------------------------------------------------------------------------

run("SecretSanta_FAMILY.txt")
