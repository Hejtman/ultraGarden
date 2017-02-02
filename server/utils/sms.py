import smtplib

from config import GMail


def send_sms(message):
    server = smtplib.SMTP(GMail.SERVER, GMail.PORT)
    server.starttls()
    server.login(GMail.ADDRESS, GMail.PASSWORD)
    msg = "From:{}\nTo:{}\nSubject:Garden: \n\n{}".format(GMail.ADDRESS, GMail.SMS_GATEWAY, message)
    server.sendmail(GMail.ADDRESS, GMail.SMS_GATEWAY, msg)
    server.quit()


# UNIT TESTS:
if __name__ == '__main__':
    send_sms("testing sms")
