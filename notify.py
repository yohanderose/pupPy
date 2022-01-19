from login import email_addr, email_pwd

# TODO: Add text functionality through spark or vodafone gateway


def send_msg(destination, message, subject, sender_credentials, smtp_server, smtp_port) -> int:
    """
    Send an SMS or email message from an email address via the specified gateway provider.
    :param destination: The destination number or email address.
    :param message: The message to send.
    :param subject: The subject of the email message.
    :param sender_credentials: The sender's email address and password.
    :param smtp_server: The SMTP server to use.
    :param smtp_port: The SMTP port to use.
    :return: The status code of the message send operation.
    """

    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders

    try:
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender_credentials['email']
        msg['To'] = destination

        # Create the body of the message (a plain-text and an HTML version).
        text = message
        html = """\
        <html>
          <head></head>
          <body>
            <p>""" + message + """</p>
          </body>
        </html>
        """

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        # Send the message via an SMTP server.
        s = smtplib.SMTP(smtp_server, smtp_port)
        # s.set_debuglevel(1)
        s.starttls()
        s.login(sender_credentials['email'], sender_credentials['password'])
        s.sendmail(sender_credentials['email'], destination, msg.as_string())
        s.quit()
    except Exception as e:
        print(e)
        return 1
    return 0


# number = '640273045445'
# provider = 'etxt.co.nz'
# to = f'{number}@{provider}'
# to = 'yohanderose@gmail.com'

# send_msg(to, 'test message', 'test subject',
#          {'email': email_addr, 'password': email_pwd},  'smtp.gmail.com', 587)
