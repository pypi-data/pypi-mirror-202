from tkinter import DISABLED, NORMAL,filedialog, messagebox
import tkinter
import customtkinter
from src.Database.Model.emailTemplateModel import EmailTemplateModel
from src.Database.Repository.databaseRepository import GetDBRepositorySingletion

from src.Logger.logger import Logger
from src.Utility.ConfigUtility import GetConfigSingletion
from src.Utility.StringUtilityCTK import GetStringSingletionCTK
import shutil

class EditTemplateTopLevel(customtkinter.CTkToplevel):
    __None           = -1
    __AddTemplate    = 0
    __EditTemplate   = 1
    __DeleteTemplate = 2
    __selectedTemplate = None


    def __init__(self, xPos,yPos,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = Logger()

        self.config_obj = GetConfigSingletion()
        self.stringVar = GetStringSingletionCTK()
        self.database = GetDBRepositorySingletion()
        self.geometry(f'+{xPos}+{yPos}')
        self.geometry("800x900")
        self.operationType = self.__None

        customtkinter.CTkFrame.rowconfigure(self,0)
        # customtkinter.CTkFrame.rowconfigure(self,1)
        # customtkinter.CTkFrame.rowconfigure(self,2)
        # customtkinter.CTkFrame.rowconfigure(self,3)
        # customtkinter.CTkFrame.rowconfigure(self,4)
        # customtkinter.CTkFrame.rowconfigure(self,5,weight=10)
        # customtkinter.CTkFrame.rowconfigure(self,6)
        customtkinter.CTkFrame.columnconfigure(self,0,weight=1)
        customtkinter.CTkFrame.columnconfigure(self,1,weight=1)
        customtkinter.CTkFrame.columnconfigure(self,2,weight=1)

        self.addNewTemplate = customtkinter.CTkButton(self,text = self.stringVar.createTemplate.get(),command=self.__AddNewTemplate)
        self.addNewTemplate.grid(row=0, column=0, pady = 10, padx = 10,sticky="nsew")

        self.editTemplate = customtkinter.CTkButton(self,text = self.stringVar.editTemplate.get(),command=self.__EditExistTemplate)
        self.editTemplate.grid(row=0, column=1, pady = 10, padx = 10,sticky="nsew")

        self.deleteTemplate = customtkinter.CTkButton(self,text = self.stringVar.deleteTemplate.get(),command=self.__DeleteExistTemplate)
        self.deleteTemplate.grid(row=0, column=2, pady = 10, padx = 10,sticky="nsew")

        self.grab_set()

    def show(self):
        self.wait_window()
        return self.operationType

    def __AddNewTemplate(self):
        
        self.addNewTemplate.grid_forget()
        self.editTemplate.grid_forget()
        self.deleteTemplate.grid_forget()

        customtkinter.CTkFrame.rowconfigure(self,0)
        customtkinter.CTkFrame.rowconfigure(self,1)
        customtkinter.CTkFrame.rowconfigure(self,2)
        customtkinter.CTkFrame.rowconfigure(self,3)
        customtkinter.CTkFrame.rowconfigure(self,4)
        customtkinter.CTkFrame.rowconfigure(self,5,weight=10)
        customtkinter.CTkFrame.rowconfigure(self,6)
        customtkinter.CTkFrame.columnconfigure(self,0,weight=1)
        customtkinter.CTkFrame.columnconfigure(self,1,weight=1)
        customtkinter.CTkFrame.columnconfigure(self,2,weight=1)

        self.inputTemplateLable = customtkinter.CTkLabel(self, anchor="w",text=self.stringVar.templateName.get())
        self.inputTemplateLable.grid(row=1, column=0, padx=10 ,pady=10,sticky="ew")

        self.inputNameVar = customtkinter.StringVar(self,value='')
        self.inputName = customtkinter.CTkEntry(self,font=("Arial", 15),width=300,textvariable=self.inputNameVar)
        self.inputName.grid(row=1, column=1,columnspan =2, sticky='nwse',padx=10,pady=10)

        self.inputPathLable = customtkinter.CTkLabel(self, anchor="w",text=self.stringVar.templatePath.get())
        self.inputPathLable.grid(row=2, column=0, padx=10 ,pady=10,sticky="ew")

        self.inputPath = customtkinter.StringVar(self,value='')
        self.inputPathTextField = customtkinter.CTkEntry(self,font=("Arial", 15),width=300,textvariable=self.inputPath,state=DISABLED)
        self.inputPathTextField.grid(row=2, column=1, sticky='nwse',padx=10,pady=10)

        self.setInputPathButton = customtkinter.CTkButton(self,text=self.stringVar.selectTemplate.get(),command=self.__selectInputPutDirectory)
        self.setInputPathButton.grid(row=2, column=2, sticky='nsew',padx=10, pady=10)


        self.emailSubjectLable = customtkinter.CTkLabel(self, anchor="w",text=self.stringVar.emailSubject.get())
        self.emailSubjectLable.grid(row=3, column=0, padx=10 ,pady=10,sticky="ew")

        self.inputSubjectVar = customtkinter.StringVar(self,value='')
        self.inputEmailSubject = customtkinter.CTkEntry(self,font=("Arial", 15),width=300,textvariable=self.inputSubjectVar)
        self.inputEmailSubject.grid(row=3, column=1,columnspan =2, sticky='nwse',padx=10,pady=10)

        self.containDataVar = customtkinter.StringVar(self,"Yes")
        self.containDataCheckbox = customtkinter.CTkCheckBox(self, text=self.stringVar.requireData.get(),
                                            variable=self.containDataVar, onvalue="Yes", offvalue="No")
        self.containDataCheckbox.grid(row=4, column=0, sticky='nsew',padx=10, pady=10)

        self.containAttachmentVar = customtkinter.StringVar(self,"Yes")
        self.containAttachmentCheckbox = customtkinter.CTkCheckBox(self, text=self.stringVar.requireAttachment.get(),
                                            variable=self.containAttachmentVar, onvalue="Yes", offvalue="No")
        self.containAttachmentCheckbox.grid(row=4, column=1, sticky='nsew',padx=10, pady=10)

        self.emailPreview = customtkinter.CTkTextbox(self)
        self.emailPreview.configure(state=DISABLED)
        self.emailPreview.grid(row=5, column=0, columnspan = 3,sticky="nsew",padx=10,pady=10)

        self.saveToDb = customtkinter.CTkButton(self,text=self.stringVar.save.get(),command=self.__SaveTemplate)
        self.saveToDb.grid(row=6, column=1, sticky='nsew',padx=10, pady=10)

        self.clearEmail = customtkinter.CTkButton(master=self, text =self.stringVar.resetEmail.get(),command=self.__ClearTemplate,
                                                  fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.clearEmail.grid(row=6, column=2, pady = 10, padx = 10,sticky="nsew")

        pass

    def __EditExistTemplate(self):
        
        self.addNewTemplate.grid_forget()
        self.editTemplate.grid_forget()
        self.deleteTemplate.grid_forget()

        customtkinter.CTkFrame.rowconfigure(self,0)
        customtkinter.CTkFrame.rowconfigure(self,1)
        customtkinter.CTkFrame.rowconfigure(self,2)
        customtkinter.CTkFrame.rowconfigure(self,3)
        customtkinter.CTkFrame.rowconfigure(self,4)
        customtkinter.CTkFrame.rowconfigure(self,5)
        customtkinter.CTkFrame.rowconfigure(self,6,weight=10)
        customtkinter.CTkFrame.rowconfigure(self,7)
        customtkinter.CTkFrame.columnconfigure(self,0,weight=1)
        customtkinter.CTkFrame.columnconfigure(self,1,weight=1)
        customtkinter.CTkFrame.columnconfigure(self,2,weight=1)

        self.template = customtkinter.CTkOptionMenu(self,values=self.database.GetAllEmailTemplateName(),command=self._OnSelectEmailTemplate,dynamic_resizing=False)
        self.template.grid(row=1, column=0, columnspan = 3 ,pady = 10, padx = 10, sticky="nsew")


        self.inputTemplateLable = customtkinter.CTkLabel(self, anchor="w",text=self.stringVar.templateName.get())
        self.inputTemplateLable.grid(row=2, column=0, padx=10 ,pady=10,sticky="ew")

        self.inputNameVar = customtkinter.StringVar(self,value='')
        self.inputName = customtkinter.CTkEntry(self,font=("Arial", 15),width=300,textvariable=self.inputNameVar)
        self.inputName.grid(row=2, column=1,columnspan =2, sticky='nwse',padx=10,pady=10)

        self.inputPathLable = customtkinter.CTkLabel(self, anchor="w",text=self.stringVar.templatePath.get())
        self.inputPathLable.grid(row=3, column=0, padx=10 ,pady=10,sticky="ew")

        self.inputPath = customtkinter.StringVar(self,value='')
        self.inputPathTextField = customtkinter.CTkEntry(self,font=("Arial", 15),width=300,textvariable=self.inputPath,state=DISABLED)
        self.inputPathTextField.grid(row=3, column=1, sticky='nwse',padx=10,pady=10)

        self.setInputPathButton = customtkinter.CTkButton(self,text=self.stringVar.selectTemplate.get(),command=self.__selectInputPutDirectory)
        self.setInputPathButton.grid(row=3, column=2, sticky='nsew',padx=10, pady=10)


        self.emailSubjectLable = customtkinter.CTkLabel(self, anchor="w",text=self.stringVar.emailSubject.get())
        self.emailSubjectLable.grid(row=4, column=0, padx=10 ,pady=10,sticky="ew")

        self.inputSubjectVar = customtkinter.StringVar(self,value='')
        self.inputEmailSubject = customtkinter.CTkEntry(self,font=("Arial", 15),width=300,textvariable=self.inputSubjectVar)
        self.inputEmailSubject.grid(row=4, column=1,columnspan =2, sticky='nwse',padx=10,pady=10)

        self.containDataVar = customtkinter.StringVar(self,"Yes")
        self.containDataCheckbox = customtkinter.CTkCheckBox(self, text=self.stringVar.requireData.get(),
                                            variable=self.containDataVar, onvalue="Yes", offvalue="No")
        self.containDataCheckbox.grid(row=5, column=0, sticky='nsew',padx=10, pady=10)

        self.containAttachmentVar = customtkinter.StringVar(self,"Yes")
        self.containAttachmentCheckbox = customtkinter.CTkCheckBox(self, text=self.stringVar.requireAttachment.get(),
                                            variable=self.containAttachmentVar, onvalue="Yes", offvalue="No")
        self.containAttachmentCheckbox.grid(row=5, column=1, sticky='nsew',padx=10, pady=10)

        self.emailPreview = customtkinter.CTkTextbox(self)
        self.emailPreview.configure(state=DISABLED)
        self.emailPreview.grid(row=6, column=0, columnspan = 3,sticky="nsew",padx=10,pady=10)

        self.saveToDb = customtkinter.CTkButton(self,text=self.stringVar.save.get(),command=self._OnUpdateEmailTemplate)
        self.saveToDb.grid(row=7, column=1, sticky='nsew',padx=10, pady=10)

        self.clearEmail = customtkinter.CTkButton(master=self, text =self.stringVar.resetEmail.get(),command=self.__ClearTemplate,
                                                  fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.clearEmail.grid(row=7, column=2, pady = 10, padx = 10,sticky="nsew")

        pass
    def __DeleteExistTemplate(self):
                
        self.__EditExistTemplate()

        self.saveToDb.configure(command = self._OnDeleteEmailTemplate,)



        pass

    def __selectInputPutDirectory(self):
        path = filedialog.askopenfilename()
        if path == '':
            return
        else:
            self.inputPath.set(path)
            file = open(path,encoding="utf-8")#append mode 
            self.emailPreview.configure(state=NORMAL)
            self.emailPreview.delete("0.0","end")
            self.emailPreview.insert("0.0",file.read())
            self.emailPreview.configure(state=DISABLED)
            file.close()
        return
    
    def __SaveTemplate(self):
        if self.inputNameVar.get() == None or self.inputNameVar.get() == "":
            messagebox.showerror(self.stringVar.createTemplate.get(), self.stringVar.errorMissingName.get())
            return
        elif self.inputPath.get() == None or self.inputPath.get() == "":
            messagebox.showerror(self.stringVar.createTemplate.get(), self.stringVar.errorMissingPath.get())
            return
        elif self.inputSubjectVar.get() == None or self.inputSubjectVar.get() == "":
            messagebox.showerror(self.stringVar.createTemplate.get(), self.stringVar.errorMissingSubject.get())
            return
        
        
        copyResultPath = shutil.copy(self.inputPath.get(), self.config_obj.ReadConfig('resource_path','resourcepath'))

    
        email = EmailTemplateModel(
            path=copyResultPath,
            name=self.inputNameVar.get(),
            containData= 1 if self.containDataCheckbox.get() == "Yes" else 0,
            containAttachment= 1 if self.containAttachmentCheckbox.get() == "Yes" else 0,
            subject=self.inputSubjectVar.get()
            )
        
        if self.database.SaveEmailTemplate(emailTemplateModel=email):
            messagebox.showinfo(self.stringVar.createTemplate.get(), self.stringVar.createTemplateSuccess.get())
            self.operationType = self.__AddTemplate
            self.destroy()
            return
        else:
            messagebox.showerror(self.stringVar.createTemplate.get(),  self.stringVar.createTemplateFailed.get())
            return

    def __ClearTemplate(self):
        self.inputNameVar.set("")
        self.inputPath.set("")
        self.inputSubjectVar.set("")
        self.containDataVar.set("No")
        self.containAttachmentVar.set("No")

        if self.template != None:
            self.template.set(self.stringVar.defaultTemplate.get())
        pass

    def _OnSelectEmailTemplate(self,choice):
        if choice == self.stringVar.defaultTemplate.get():
            pass
        else:
            self.__selectedTemplate = self.database.GetEmailTemplateByName(choice)

            if self.__selectedTemplate != None:
                self.inputNameVar.set(self.__selectedTemplate.GetName())
                self.inputPath.set(self.__selectedTemplate.GetPath())
                self.inputSubjectVar.set(self.__selectedTemplate.GetSubject())
                self.containDataVar.set("Yes" if self.__selectedTemplate.GetContainData() == 1 else "No")
                self.containAttachmentVar.set("Yes" if self.__selectedTemplate.GetContainAttachment() == 1 else "No")
                
                file = open(self.inputPath.get(),encoding="utf-8")#append mode 
                self.emailPreview.configure(state=NORMAL)
                self.emailPreview.delete("0.0","end")
                self.emailPreview.insert("0.0",file.read())
                self.emailPreview.configure(state=DISABLED)
                file.close()
                pass

    def _OnUpdateEmailTemplate(self):
        if self.__selectedTemplate == None:
            return
        
        self.__selectedTemplate.SetName(self.inputNameVar.get())
        self.__selectedTemplate.SetPath(self.inputPath.get())
        self.__selectedTemplate.SetSubject(self.inputSubjectVar.get())
        self.__selectedTemplate.SetContainData(1 if self.containDataVar.get() == "Yes" else 0)
        self.__selectedTemplate.SetContainAttachment(1 if self.containAttachmentVar.get() == "Yes" else 0)

        if self.database.UpdateEmailTemplate(self.__selectedTemplate):
            messagebox.showinfo(self.stringVar.createTemplate.get(), self.stringVar.updateTempalteSuccess.get())
            self.operationType = self.__EditTemplate
            shutil.copy(self.inputPath.get(), self.config_obj.ReadConfig('resource_path','resourcepath'))
            self.destroy()
        else:
            messagebox.showerror(self.stringVar.createTemplate.get(),  self.stringVar.updateTempalteFailed.get())
            return

    def _OnDeleteEmailTemplate(self):
        if self.__selectedTemplate == None:
            return
        
        if self.database.DeleteEmailTemplate(self.__selectedTemplate.GetIdx()):
            messagebox.showinfo(self.stringVar.createTemplate.get(), self.stringVar.deleteTempalteSuccess.get())
            self.operationType = self.__EditTemplate
            self.destroy()
        else:
            messagebox.showerror(self.stringVar.createTemplate.get(),  self.stringVar.deleteTempalteFailed.get())
            return

    
    pass