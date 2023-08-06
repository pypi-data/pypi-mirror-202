from src.Utility.ConfigUtility import GetConfigSingletion
from src.Logger.logger import Logger
import smtplib, ssl

class EmailService:
    def __init__(self) -> None:
        self.config_obj = GetConfigSingletion()
        self.logger = Logger()
        self.emailServer = None
        self.emailContext = ssl.create_default_context()
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


    #Email Service
    def ConnectEmailAccount(self)->bool:
        try:
            self.emailServer = smtplib.SMTP(self.config_obj.ReadConfig('email','smptServer'),self.config_obj.ReadConfig('email','port'))
            self.emailServer.starttls(context=self.emailContext) # Secure the connection
            self.emailServer.login(self.config_obj.ReadConfig('email','emailAc'), self.config_obj.ReadConfig('email','emailPw'))
        except:
            return False
        finally:
            return True
        
    def DisconnectEmailAccount(self):
        pass

    def SendEmail(self):
        pass

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