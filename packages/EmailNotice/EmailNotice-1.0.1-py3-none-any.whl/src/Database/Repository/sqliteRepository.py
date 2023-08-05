import sqlite3
from src.Database.Model.emailTemplateModel import EmailTemplateModel

from src.Database.Repository.baseDatabaaseRepository import BaseRepository
class SqliteRepository(BaseRepository):
    
    _databaseConnection = None

    checkTableExisitQuery = """SELECT name FROM sqlite_master WHERE type='table' AND name='{0}'; """
    createRecipientGroupNameQuery = """CREATE TABLE "RECIPIENTGROUPNAME" ("groupId"	INTEGER,"groupName"	TEXT NOT NULL,PRIMARY KEY("groupId" AUTOINCREMENT));"""
    createRecipientGroupQuery = """
    CREATE TABLE "RECIPIENTGROUP" (
	"recipientId"	INTEGER NOT NULL,
	"recipientGroupId"	INTEGER NOT NULL
    );"""
    createRecipientQuery = """
    CREATE TABLE "RECIPIENT" (
	"recipientId"	INTEGER,
	"recipientEmail"	TEXT NOT NULL,
	"displayNameEn"	TEXT NOT NULL,
	"displayNameZh"	TEXT NOT NULL,
	"displayNameCn"	TEXT NOT NULL,
	"fullNameEn"	TEXT NOT NULL,
	"fullNameZh"	TEXT NOT NULL,
	"fullNameCn"	TEXT NOT NULL,
	PRIMARY KEY("recipientId" AUTOINCREMENT)
    );"""
    createEmailTemplateQuery = """
    CREATE TABLE "EMAILTEMPLATE" (
	"templateId"	INTEGER,
	"templateName"	TEXT NOT NULL,
	"templatePath"	TEXT NOT NULL,
    "containAttachment"	INTEGER,
	"containData"	INTEGER,
    "subject"	TEXT NOT NULL,
	PRIMARY KEY("templateId" AUTOINCREMENT)
    );
    """

    insertEmailTemplateQuery = """
    INSERT INTO EMAILTEMPLATE (templateName,templatePath,containAttachment,containData,subject)
    VALUES( '{0}','{1}',{2},{3},'{4}');
    """

    getAllTemplateNamQuery = """
    Select templateName from EMAILTEMPLATE ORDER BY templateId DESC
    """

    getTemplateByName = """
    SELECT * FROM EMAILTEMPLATE WHERE templateName = '{0}' ORDER BY templateId DESC LIMIT 1
    """

    updateTemplateQuery = """UPDATE EMAILTEMPLATE SET templateName = '{0}', templatePath = '{1}', containAttachment = {2}, containData = {3}, subject = '{4}' WHERE templateId = {5}"""

    deleteTemplateQuery = """DELETE FROM EMAILTEMPLATE WHERE templateId = {0}"""

    def __init__(self,path):
        try:
            self._databaseConnection = sqlite3.connect(path)
            self.CheckTableExisit()

        except Exception as ex :
            print(ex)
            pass


    def DisconnectDatabase(self):
        self._databaseConnection.close()

    def CheckTableExisit(self)->bool:
        for tableName in self.workingTableList:
            cursor = self._databaseConnection.cursor()
            listOfTables = cursor.execute(self.checkTableExisitQuery.format(tableName)).fetchall()
            cursor.close()
            if listOfTables == []:
                self.CreateTable(tableName)
        pass

    def CreateTable(self,tableName):
        cursor = self._databaseConnection.cursor()
        if tableName == self.workingTableList[0]:
            #'RECIPIENTGROUPNAME',
            cursor.execute(self.createRecipientGroupNameQuery)
            pass
        elif tableName == self.workingTableList[1]:
            #'RECIPIENTGROUP',
            cursor.execute(self.createRecipientGroupQuery)
            pass
        elif tableName == self.workingTableList[2]:
            #'RECIPIENT',
            cursor.execute(self.createRecipientQuery)
            pass
        elif tableName == self.workingTableList[3]:
            #'EMAILTEMPLATE'
            cursor.execute(self.createEmailTemplateQuery)
            pass
        cursor.close()

    def GetAllEmailTemplateName(self)->list:
        cursor = self._databaseConnection.cursor()
        cursor.row_factory = lambda cursor, row: row[0]
        listOfTables = cursor.execute(self.getAllTemplateNamQuery).fetchall()
        cursor.close()
        return listOfTables

    def GetAllRecipientGroupName(self)->list:
        return ['Test2']
    
    def SaveEmailTemplate(self,emailModel:EmailTemplateModel)->bool:
        try:
            cursor = self._databaseConnection.cursor()
            insertFinalQuery = self.insertEmailTemplateQuery.format(
                emailModel.GetName(),emailModel.GetPath(),emailModel.GetContainData(),emailModel.GetContainAttachment(),emailModel.GetSubject())
            
            cursor.execute(insertFinalQuery)
            self._databaseConnection.commit()
            return True
        except Exception as e:
            return False
    
    pass

    def GetEmailTemplateByName(self,name)->EmailTemplateModel:
        cursor = self._databaseConnection.cursor()
        listOfTables = cursor.execute(self.getTemplateByName.format(name)).fetchall()
        cursor.close()

        return EmailTemplateModel(listOfTables[0][2],listOfTables[0][1],listOfTables[0][4],listOfTables[0][3],listOfTables[0][5],listOfTables[0][0])
    

    def UpdateEmailTemplate(self, template: EmailTemplateModel) -> bool:
        try:
            updateFinalQuery = self.updateTemplateQuery.format(template.GetName(),template.GetPath(),
                                                            template.GetContainAttachment(),
                                                            template.GetContainData(),
                                                            template.GetSubject(),
                                                            template.GetIdx())

            cursor = self._databaseConnection.cursor()
            cursor.execute(updateFinalQuery)
            self._databaseConnection.commit()
            
            cursor.close()
            return True
        except Exception as e:
            print(str(e))
            return False
    
    def DeleteEmailTemplate(self, idx) -> bool:
        try:
            deleteFinalQuery = self.deleteTemplateQuery.format(idx)
            cursor = self._databaseConnection.cursor()
            cursor.execute(deleteFinalQuery)
            self._databaseConnection.commit()
            
            cursor.close()
            return True

        except Exception as e:
            return False