import subprocess
# It is a easy way to use sendmail program in kali
# open account in sendgrid, confirm email and 
# go to -> Integrate using our Web API or SMTP relay / SMTP Relay
# create a new key
# put your password in line 10

server = "smtp.sendgrid.net:25"
username = "apikey"
password = "your sendgrid password"

print("Welcome to Helton Wernik Mail spoofing!!!! Lets Start  ")
to_email = raw_input("To email: ")
from_email = raw_input("from email: ")
message_header = raw_input("Enter the name of the sender email you want to spoof ")
subject = raw_input("Enter the subject: ")
message = raw_input("Finally, the message: ")
result = subprocess.check_output(["sendemail", "-s", server, "-xu", username, "-xp", password, "-f", from_email, "-t", to_email, "-u", subject, "-m", message, "-o", "message-header=From:" + message_header + " <" + from_email + ">"])
print(result)