from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from era.Database.Model.emailTemplateModel import EmailTemplateModel
from era.Database.Model.recipientModel import RecipientModel
from era.Utility.ConfigUtility import GetConfigSingletion
from era.Logger.logger import Logger
import smtplib, ssl

class EmailService:
    def __init__(self) -> None:
        self.config_obj = GetConfigSingletion()
        self.logger = Logger()
        self.emailServer = None
        self.emailContext = ssl.create_default_context()
        self.isLogin = False
        pass


    #DB operation
    def GetAllEmailAccountList(self):
        pass

    def AddNewEmailAccount(self):
        pass

    def UpdateEmailAccount(self):
        pass

    def DeleteEmailAccount(self):
        pass

    def IsLogin(self) -> bool:
        return self.isLogin


    #Email Service
    def ConnectEmailAccount(self)->bool:
        try:
            self.emailServer = smtplib.SMTP(self.config_obj.ReadConfig('email','smptServer'),self.config_obj.ReadConfig('email','port'))
            self.emailServer.starttls(context=self.emailContext) # Secure the connection
            self.emailServer.login(self.config_obj.ReadConfig('email','emailAc'), self.config_obj.ReadConfig('email','emailPw'))
            self.isLogin = True
        except:
            self.isLogin = False
        finally:
            return self.isLogin
        
    def DisconnectEmailAccount(self):
        pass

    def SendEmail(self,emailList:list[RecipientModel], template:EmailTemplateModel) -> list[str]:
        sendError = []

        for recipient in emailList:
            try:
                mimemsg = MIMEMultipart()

                mimemsg['From']=self.config_obj.ReadConfig('email','emailAc')
                mimemsg['To']=recipient.GetRecipientEMail()
                mimemsg['Subject']=template.GetSubject()

                file = open(template.GetPath(),encoding="utf-8")#append mode 
                templateData = file.read()
                file.close()

                mimemsg.attach(MIMEText(templateData, 'plain'))

                self.emailServer.send_message(mimemsg)
            except:
                sendError.append(recipient.GetRecipientEMail())
        
        return sendError

    def GetEmailAccount(self)->str:
        try:
            return self.config_obj.ReadConfig('email','emailAc')
        except:
            return ""



    #Private function
    def __AttachSelfData(self):
        pass

    def __AddSelfAttachment(self):
        pass

    pass