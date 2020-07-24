import os
import smtplib
import random
import email.encoders as Encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailUtil:
    ####################################################################################################################
    SMTP_IP = "10.218.130.60"

    DEFAULT_DIR = os.listdir(os.path.dirname(os.path.realpath(__file__)))
    print(DEFAULT_DIR)

    ####################################################################################################################

    def __init__(self):
        """
        INFO: Default Constructure cannot be Creatable
        WARNING: If attand to create this object, it will raise NotImplementedError
        """
        assert NotImplementedError("This object useing only library, cannot be creatable!!!")

    def __new__(cls):
        """
        INFO: This method was overrided only avoided to __new__ operator
        :return: NOISE_OBJECT
        """
        return object.__new__(cls)

    @staticmethod
    def sendMail(mailFrom, mailTo, mailCc, mailSbj, mailBodyArray, smtpIp = SMTP_IP, attachs=[],
                 dirAttach = DEFAULT_DIR):
        """
        This Function send e-mail with directly
        :raise If any Exception will re-raise this Exception
        :param mailFrom: Mail From part
        :param mailTo: Mail To part
        :param mailCc: Mail Cc part
        :param mailSbj: Mail Subject
        :param mailBodyArray: Mail Body Array, this part should be contain yours html body as list
        :param smtpIp: Mail STMP server IP
        :param attachs: If you have to attach objects, you can naming with array(JPG,TXT,PDF...)
        :return: NONE
        """
        try:
            mail_Text = ""
            eMailFile = "emailFile_" + str(random.randrange(1000, 9999)) + ".html"
            mailBodyFile = open(eMailFile, 'w')
            mailBodyFile.write("<html><head></head><body><p><pre>")
            mail_Text += "<html><head></head><body><p><pre>"
            for body_Line in mailBodyArray:
                mailBodyFile.write(body_Line)
                mail_Text += body_Line
            mailBodyFile.write("</pre></p></body></html>")
            mail_Text += "</pre></p></body></html>"
            mailBodyFile.close()

            mail_TO = mailTo.split(',')
            mail_CC = mailCc.split(',')

            msg = MIMEMultipart('alternative')
            msg['Subject'] = mailSbj
            msg['From'] = mailFrom
            msg['To'] = ', '.join(mail_TO)
            msg['Cc'] = ', '.join(mail_CC)


            for name in attachs:
                for file in dirAttach:
                    if name in file:
                        part = MIMEBase('application', "octet-stream")
                        part.set_payload(open(str(file), "rb").read())
                        Encoders.encode_base64(part)
                        part.add_header('Content-Disposition', 'attachment; filename=' + str(file))
                        msg.attach(part)

            part1 = MIMEText(mail_Text, 'plain')
            part2 = MIMEText(mail_Text, 'html')
            msg.attach(part1)
            msg.attach(part2)

            aggregatesMail = mail_TO + mail_CC
            smtplib.SMTP_PORT = 25
            print("11111111")
            s = smtplib.SMTP(smtpIp)
            print("22222222")
            s.sendmail(mailFrom, aggregatesMail, msg.as_string())
            print("33333333")
            s.quit()
        except Exception as e:
            raise RuntimeError("Unexpected Error : " + str(e))
