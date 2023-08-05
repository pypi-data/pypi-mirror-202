from abc import abstractclassmethod
from src.Database.Model.emailTemplateModel import EmailTemplateModel
from src.Utility.ConfigUtility import GetConfigSingletion
from src.Database.Repository.sqliteRepository import SqliteRepository
from src.Utility.StringUtilityCTK import GetStringSingletionCTK


class _DatabaseRepository:

    _SQLITE = 'SQLITE'


    _dbInstance = None
    _databaseRepository = None


    def __init__(self) -> None:
        #Get config and check what db is using
        self.config_obj = GetConfigSingletion()
        self.stringValue = GetStringSingletionCTK()
        self.__CreateDBRepository(self.config_obj.ReadConfig('database','type'),self.config_obj.ReadConfig('database','repository'))
        pass



    def __CreateDBRepository(self, dbType,pathOrRepository):
        if dbType == self._SQLITE:
            self._databaseRepository = SqliteRepository(pathOrRepository)
            pass
        elif dbType == 1:
            pass
        else:
            pass
    
    def DisconnectDatabase(self):
        self._databaseRepository.DisconnectDatabase()
        pass

    def GetAllEmailTemplateName(self)->list:
        listOfTemplateName = self._databaseRepository.GetAllEmailTemplateName()
        listOfTemplateName.insert(0,self.stringValue.defaultTemplate.get())
        return listOfTemplateName
        

    def GetAllRecipientGroupName(self)->list:
        listOfGroupName = self._databaseRepository.GetAllRecipientGroupName()
        listOfGroupName.insert(0,self.stringValue.defaultEmailGroup.get())
        return listOfGroupName
    
    def SaveEmailTemplate(self,emailTemplateModel:EmailTemplateModel):
        return self._databaseRepository.SaveEmailTemplate(emailModel=emailTemplateModel)
    
    def GetEmailTemplateByName(self, templateName ) -> EmailTemplateModel:
        return self._databaseRepository.GetEmailTemplateByName(name=templateName)
    
    def UpdateEmailTemplate(self, emailTemplateModel:EmailTemplateModel) -> bool:
        return self._databaseRepository.UpdateEmailTemplate(emailTemplateModel)
    
    def DeleteEmailTemplate(self, emailIdx) -> bool:
        return self._databaseRepository.DeleteEmailTemplate(emailIdx)
        

def GetDBRepositorySingletion():
    if _DatabaseRepository._dbInstance is None:
        _DatabaseRepository._dbInstance = _DatabaseRepository()
    return _DatabaseRepository._dbInstance