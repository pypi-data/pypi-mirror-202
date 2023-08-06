import smtplib


class Gmail:
    def __init__(self, account, app_password):
        """App password can be obtained:
        1. https://myaccount.google.com/
        2. Security
        3. under `How you sign in to Google`, click 2-Step Verification
        4. App passwords

        Reference: https://support.google.com/accounts/answer/185833
        """
        self.account = account if '@' in account else f'{account}@gmail.com'
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(self.account, app_password)

    def send(self, to=None, subject=None, body=None):
        to = self.account if to is None else (to if '@' in to else f'{to}@gmail.com')
        message = body if subject is None else 'Subject: {}\n\n{}'.format(subject, body)
        self.server.sendmail(self.account, to, message)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.quit()
