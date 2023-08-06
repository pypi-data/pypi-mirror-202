
from abc import abstractmethod

from src.Database.Model import emailTemplateModel


class BaseRepository:

    workingTableList = [
        'RECIPIENTGROUPNAME',
        'RECIPIENTGROUP',
        'RECIPIENT',
        'EMAILTEMPLATE'
    ]

    def __init__(self,path):
        pass

    @abstractmethod
    def DisconnectDatabase(self):
        pass

    @abstractmethod
    def CheckTableExisit(self):
        pass

    @abstractmethod
    def CreateTable(self):
        pass

    def GetAllEmailTemplateName(self)->list:
        return []

    def GetAllRecipientGroupName(self)->list:
        return []
    
    def SaveEmailTemplate(self,emailModel)->bool:
        pass

    def GetEmailTemplateByName(self,name)->emailTemplateModel:
        pass

    def UpdateEmailTemplate(self,template:emailTemplateModel)->bool:
        pass

    def DeleteEmailTemplate(self, idx)->bool:
        pass

    pass