from customtkinter import StringVar

from src.Utility.ConfigUtility import GetConfigSingletion


class _StringSingletonCTK:
    _stringInstance = None
    

    zhString = [ 
        "狀態: ",
        "離線",
        "線上",
        "電郵地址: ",
        "請選擇範本",
        "請選擇電郵組別",
        "插入數據/附件",
        "編輯範本",
        "新增範本",
        "刪除範本",
        "編輯電郵",
        "寄出",
        "重設",
        "附件: ",

        "範本名稱 (只可英文):",
        "選擇範本",
        "範本路徑",

        "必須附上數據?",
        "必須附上附件?",
        "電郵標題",
        "儲存",

        "請輸入 範本名稱",
        "請輸入 範本路徑",
        "請輸入 電郵標題",

        "新增範本成功",
        "新增範本失敗",

        "更新範本成功",
        "更新範本失敗",

        "刪除範本成功",
        "刪除範本失敗",
    ]

    enString = [
        "Status: ",
        "Offline",
        "Online",
        "Email AC: ",
        "Please Select Email Template",
        "Please Email Group",
        "Add Data/Attachment",
        "Edit Template",
        "Create Template",
        "Delete Template",
        "Edit Email",
        "Send",
        "Reset",
        "Attachment: ",

        "Template Name:",
        "Select Template",
        "Template Path",

        "Require Data?",
        "Require Attachment?",
        "Email Subject",
        "Save",

        "Please input Template Name",
        "Please input Template Path",
        "Please input Email Subject",

        "Create Template Success",
        "Create Template Failed",

        "Update Template Success",
        "Update Template Failed",

        "Delete Template Success",
        "Delete Template Failed",
    ]

    def __init__(self) -> None:
        self.status = StringVar()
        self.offline = StringVar()
        self.online = StringVar()
        self.emailAC = StringVar()
        self.defaultTemplate = StringVar()
        self.defaultEmailGroup = StringVar()
        
        self.attachData = StringVar()
        self.editTemplate = StringVar()
        self.createTemplate = StringVar()
        self.deleteTemplate = StringVar()

        self.editEmailList = StringVar()
        self.sendEmail = StringVar()
        self.resetEmail = StringVar()
        self.attachment = StringVar()

        self.templateName = StringVar()
        self.selectTemplate = StringVar()
        self.templatePath = StringVar()

        self.requireData = StringVar()
        self.requireAttachment = StringVar()
        self.emailSubject = StringVar()
        self.save = StringVar()

        self.errorMissingName = StringVar()
        self.errorMissingPath = StringVar()
        self.errorMissingSubject = StringVar()

        self.createTemplateSuccess = StringVar()
        self.createTemplateFailed = StringVar()

        self.updateTempalteSuccess = StringVar()
        self.updateTempalteFailed = StringVar()

        self.deleteTempalteSuccess = StringVar()
        self.deleteTempalteFailed = StringVar()

        self.SetString()
        pass

    def SetString(self):
        self.config = GetConfigSingletion()

        if self.config.IsConfigExist('language','display') == False:
            self.config.WriteConfig('language','display','zh')


        if self.config.ReadConfig("language","display") == "zh":
            self.status.set(self.zhString[0])
            self.offline.set(self.zhString[1])
            self.online.set(self.zhString[2])
            self.emailAC.set(self.zhString[3])
            self.defaultTemplate.set(self.zhString[4])
            self.defaultEmailGroup.set(self.zhString[5])
            self.attachData.set(self.zhString[6])
            self.editTemplate.set(self.zhString[7])
            self.createTemplate.set(self.zhString[8])
            self.deleteTemplate.set(self.zhString[9])
            self.editEmailList.set(self.zhString[10])
            self.sendEmail.set(self.zhString[11])
            self.resetEmail.set(self.zhString[12])
            self.attachment.set(self.zhString[13])
            self.templateName.set(self.zhString[14])
            self.selectTemplate.set(self.zhString[15])
            self.templatePath.set(self.zhString[16])
            self.requireData.set(self.zhString[17])
            self.requireAttachment.set(self.zhString[18])
            self.emailSubject.set(self.zhString[19])
            self.save.set(self.zhString[20])
            self.errorMissingName.set(self.zhString[21])
            self.errorMissingPath.set(self.zhString[22])
            self.errorMissingSubject.set(self.zhString[23])
            self.createTemplateSuccess.set(self.zhString[24])
            self.createTemplateFailed.set(self.zhString[25])
            self.updateTempalteSuccess.set(self.zhString[26])
            self.updateTempalteFailed.set(self.zhString[27])
            self.deleteTempalteSuccess.set(self.zhString[28])
            self.deleteTempalteFailed.set(self.zhString[29])


        else:
            self.status.set(self.enString[0])
            self.offline.set(self.enString[1])
            self.online.set(self.enString[2])
            self.emailAC.set(self.enString[3])
            self.defaultTemplate.set(self.enString[4])
            self.defaultEmailGroup.set(self.enString[5])
            self.attachData.set(self.enString[6])
            self.editTemplate.set(self.enString[7])
            self.createTemplate.set(self.enString[8])
            self.deleteTemplate.set(self.enString[9])
            self.editEmailList.set(self.enString[10])
            self.sendEmail.set(self.enString[11])
            self.resetEmail.set(self.enString[12])
            self.attachment.set(self.enString[13])
            self.templateName.set(self.enString[14])
            self.selectTemplate.set(self.enString[15])
            self.templatePath.set(self.enString[16])
            self.requireData.set(self.enString[17])
            self.requireAttachment.set(self.enString[18])
            self.emailSubject.set(self.enString[19])
            self.save.set(self.enString[20])
            self.errorMissingName.set(self.enString[21])
            self.errorMissingPath.set(self.enString[22])
            self.errorMissingSubject.set(self.enString[23])
            self.createTemplateSuccess.set(self.enString[24])
            self.createTemplateFailed.set(self.enString[25])
            self.updateTempalteSuccess.set(self.enString[26])
            self.updateTempalteFailed.set(self.enString[27])
            self.deleteTempalteSuccess.set(self.enString[28])
            self.deleteTempalteFailed.set(self.enString[29])





def GetStringSingletionCTK():
    if _StringSingletonCTK._stringInstance is None:
        _StringSingletonCTK._stringInstance = _StringSingletonCTK()

    return _StringSingletonCTK._stringInstance