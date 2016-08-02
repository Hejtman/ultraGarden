import smtplib


def send_mail(address_from, password, address_to, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(address_from, password)

    message = "From:{}\nTo:{}\nSubject:garden daily report\n\n{}".format(address_from, address_to, message)
    server.sendmail(address_from, address_to, message)
    server.quit()
