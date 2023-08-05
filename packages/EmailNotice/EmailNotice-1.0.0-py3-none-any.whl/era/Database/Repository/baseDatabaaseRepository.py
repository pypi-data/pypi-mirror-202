
from abc import abstractmethod

from era.Database.Model import emailTemplateModel
from era.Database.Model.recipientModel import RecipientModel


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

    @abstractmethod
    def GetAllEmailTemplateName(self)->list:
        return []

    @abstractmethod
    def GetAllRecipientGroupName(self)->list:
        return []
    
    @abstractmethod
    def SaveEmailTemplate(self,emailModel)->bool:
        pass

    @abstractmethod
    def GetEmailTemplateByName(self,name)->emailTemplateModel:
        pass

    @abstractmethod
    def UpdateEmailTemplate(self,template:emailTemplateModel)->bool:
        pass

    @abstractmethod
    def DeleteEmailTemplate(self, idx)->bool:
        pass

    @abstractmethod
    def SaveRecipient(self, emailRecipient: RecipientModel) -> bool:
        pass

    @abstractmethod
    def SaveEmailListName(self, name) ->int:
        pass

    @abstractmethod 
    def SaveEmailGroup(self, email, groupId) -> bool:
        pass

    @abstractmethod
    def GetRecipientByGroupName(self,name) -> list:
        pass

    pass