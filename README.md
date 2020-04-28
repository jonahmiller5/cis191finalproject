The mail scheduler tool is used for scheduling and sending emails from the command line. Before mailtime can be used, the mail command must be funtioning on the user’s machine. If your cannot currently send mail from the command line, use the following instructions to set up postfix.

#apt-get install postfix mailutils

#nano /etc/postfix/sasl_passwd
Edit the file to correspond with your email provider:
[smtp.gmail.com]:587 yourusername@gmail.com:yourpassword
[smtp.mail.yahoo.com]:587 yourusername@yahoo.com:yourpassword

#chmod 600 /etc/postfix/sasl_passwd
Because your password is written in plaintext, change  the permissions
#nano /etc/postfix/main.cf
If you have an existing postfix configuration file, update the following values, if you do not, you can use the sample postfix configuration file

relayhost = [smtp.gmail.com]:587
smtp_use_tls = yes
smtp_sasl_auth_enable = yes
smtp_sasl_security_options = noanonymous
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt

#postmap /etc/postfix/sasl_passwd
This will create a hash of you password to be stored in the postfix configuration files

#systemctl restart postfix.service

This concludes the command line email set up. To send from a gmail account, you must ensure go into your gmail setings and enable “Less Secure apps”

mailtime uses python3
Mailtime also has the following package dependenceis

Python packages
re
os
datetime
random

Debian packages
at

The following services must be running
atd.service
postfix.service


To run type in ./mailtime.py and follow the directions, make sure the email adresses and dates you enter are valid to you will be reprompted


