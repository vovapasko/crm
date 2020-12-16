import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "populates main_app by entities with mock data"

    def handle(self, *args, **kwargs):
        """
                Sends messages via smtp, works fine with attachments as well,
                but requires paid plan and needs some additional configuration:
                 (
                  start protonmail-bridge on machine,
                  add account to protonmail-bridge,
                  copy password for account from protonmail-bridge
                  )
                """
        sender = 'testtsg@protonmail.com'  # need to be in protonmail-bridge
        password = 'IzckO8bbHvMeCwghgLup_Q'  # need to be copied from protonmail-bridge
        receiver = 'testmypu@protonmail.com'
        subject = 'Another test'
        content = 'Hello from AMAZON!!!'
        attachments = ['image.jpg', 'doc.pdf']
        self.send_message(
            sender=sender,
            password=password,
            receiver=receiver,
            subject=subject,
            content=content,
            # attachments=attachments
        )

    def send_message(
            self, sender, password, receiver, subject, content,
            attachments=None, port=1025):
        # configuration
        port_number = port
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = subject
        message = content
        msg.attach(MIMEText(message))

        if attachments:
            # attachments
            files = attachments
            for f in files or []:
                with open(f, "rb") as fil:
                    part = MIMEApplication(
                        fil.read(),
                        Name=basename(f)
                    )
                # After the file is closed
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
                msg.attach(part)

        # sending
        mailserver = smtplib.SMTP('ec2-18-134-198-211.eu-west-2.compute.amazonaws.com', port_number)
        mailserver.login(sender, password)
        mailserver.sendmail(sender, receiver, msg.as_string())

        mailserver.quit()
