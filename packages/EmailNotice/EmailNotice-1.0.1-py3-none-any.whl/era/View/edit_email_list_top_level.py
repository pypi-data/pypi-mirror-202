from tkinter import filedialog, messagebox, ttk
import customtkinter
from era.Database.Model.recipientModel import RecipientModel
from era.Logger.logger import Logger
from era.Utility.ConfigUtility import GetConfigSingletion
from era.Utility.FileUtility import GetFileUtilitySingletion
from era.Utility.StringUtilityCTK import GetStringSingletionCTK
from era.Database.Repository.databaseRepository import GetDBRepositorySingletion

class EditEmailListTopLevel(customtkinter.CTkToplevel):
    __None           = -1
    __AddTemplate    = 0
    __EditTemplate   = 1
    __DeleteTemplate = 2
    __selectedTemplate = None
    __recipientList = None
    __selectedEmailName = None

    def __init__(self, xPos,yPos,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = Logger()

        self.config_obj = GetConfigSingletion()
        self.stringVar = GetStringSingletionCTK()
        self.database = GetDBRepositorySingletion()
        self.fileUtility = GetFileUtilitySingletion()
        self.geometry(f'+{xPos}+{yPos}')
        self.geometry("800x900")
        self.operationType = self.__None

        customtkinter.CTkFrame.rowconfigure(self,0)

        customtkinter.CTkFrame.columnconfigure(self,0,weight=1)
        customtkinter.CTkFrame.columnconfigure(self,1,weight=1)
        customtkinter.CTkFrame.columnconfigure(self,2,weight=1)

        self.addNewTemplate = customtkinter.CTkButton(self,text = self.stringVar.createEmailList.get(),command=self.__AddNewTemplate)
        self.addNewTemplate.grid(row=0, column=0, pady = 10, padx = 10,sticky="nsew")

        # self.editTemplate = customtkinter.CTkButton(self,text = self.stringVar.editTemplate.get(),command=self.__EditExistTemplate)
        # self.editTemplate.grid(row=0, column=1, pady = 10, padx = 10,sticky="nsew")

        self.deleteTemplate = customtkinter.CTkButton(self,text = self.stringVar.deleteEmailList.get(),command=self.__DeleteExistTemplate)
        self.deleteTemplate.grid(row=0, column=2, pady = 10, padx = 10,sticky="nsew")

        self.grab_set()

    def show(self):
        self.wait_window()
        return self.operationType
    

    def __AddNewTemplate(self):
        self.addNewTemplate.grid_forget()
        self.deleteTemplate.grid_forget()

        customtkinter.CTkFrame.rowconfigure(self,0)
        customtkinter.CTkFrame.rowconfigure(self,1)
        customtkinter.CTkFrame.rowconfigure(self,2)
        customtkinter.CTkFrame.rowconfigure(self,3,weight=10)
        customtkinter.CTkFrame.rowconfigure(self,4)
        customtkinter.CTkFrame.columnconfigure(self,0,weight=1)
        customtkinter.CTkFrame.columnconfigure(self,1,weight=1)


        self.inputTemplateLable = customtkinter.CTkLabel(self, anchor="w",text=self.stringVar.emailListName.get())
        self.inputTemplateLable.grid(row=1, column=0, padx=10 ,pady=10,sticky="ew")

        self.inputNameVar = customtkinter.StringVar(self,value='')
        self.inputName = customtkinter.CTkEntry(self,font=("Arial", 15),width=300,textvariable=self.inputNameVar)
        self.inputName.grid(row=1, column=1,columnspan =2, sticky='nwse',padx=10,pady=10)

        self.setInputPathButton = customtkinter.CTkButton(self,text=self.stringVar.selecEmailList.get(),command=self.__selectInputPutDirectory)
        self.setInputPathButton.grid(row=2, column=1, sticky='nsew',padx=10, pady=10)

        self.tree = ttk.Treeview(self,show='headings')
        self.tree["column"]=("fullNameEn","fullNameZh","displayNameEn","displayNameZh","recipientEmail")
        self.tree.grid(row=3, column=0, columnspan = 3,sticky="nsew",padx=10,pady=10)
        col_width = self.tree.winfo_width()
        self.tree.column("fullNameEn",width=col_width)
        self.tree.column("fullNameZh",width=col_width)
        self.tree.column("displayNameEn",width=col_width)
        self.tree.column("displayNameZh",width=col_width)
        self.tree.column("recipientEmail",width=col_width)
        self.tree.heading("fullNameEn",text=self.stringVar.fullNameEn.get())
        self.tree.heading("fullNameZh",text=self.stringVar.fullNameZh.get())
        self.tree.heading("displayNameEn",text=self.stringVar.displayNameEn.get())
        self.tree.heading("displayNameZh",text=self.stringVar.displayNameZh.get())
        self.tree.heading("recipientEmail",text=self.stringVar.recipientEmail.get())

        self.saveToDb = customtkinter.CTkButton(self,text=self.stringVar.save.get(),command=self.__SaveList)
        self.saveToDb.grid(row=4, column=1, sticky='nsew',padx=10, pady=10)

        self.clearEmail = customtkinter.CTkButton(master=self, text =self.stringVar.resetEmail.get(),command=self.__ClearList,
                                                  fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.clearEmail.grid(row=4, column=2, pady = 10, padx = 10,sticky="nsew")

        pass

    # def __EditExistTemplate(self):
    #     pass

    def __DeleteExistTemplate(self):
        self.addNewTemplate.grid_forget()
        self.deleteTemplate.grid_forget()

        customtkinter.CTkFrame.rowconfigure(self,0)
        customtkinter.CTkFrame.rowconfigure(self,1)
        customtkinter.CTkFrame.rowconfigure(self,2,weight=10)
        customtkinter.CTkFrame.rowconfigure(self,3)
        customtkinter.CTkFrame.columnconfigure(self,0,weight=1)
        customtkinter.CTkFrame.columnconfigure(self,1,weight=1)

        self.inputTemplateLable = customtkinter.CTkLabel(self, anchor="w",text=self.stringVar.emailListName.get())
        self.inputTemplateLable.grid(row=1, column=0, padx=10 ,pady=10,sticky="ew")

        self.inputNameOptionMenu = customtkinter.CTkOptionMenu(self,values=self.database.GetAllRecipientGroupName(),command=self._OnSelectEmailList,dynamic_resizing=False)
        self.inputNameOptionMenu.grid(row=1, column=1,columnspan =2, sticky='nwse',padx=10,pady=10)

        self.tree = ttk.Treeview(self,show='headings')
        self.tree["column"]=("fullNameEn","fullNameZh","displayNameEn","displayNameZh","recipientEmail")
        self.tree.grid(row=2, column=0, columnspan = 3,sticky="nsew",padx=10,pady=10)
        col_width = self.tree.winfo_width()
        self.tree.column("fullNameEn",width=col_width)
        self.tree.column("fullNameZh",width=col_width)
        self.tree.column("displayNameEn",width=col_width)
        self.tree.column("displayNameZh",width=col_width)
        self.tree.column("recipientEmail",width=col_width)
        self.tree.heading("fullNameEn",text=self.stringVar.fullNameEn.get())
        self.tree.heading("fullNameZh",text=self.stringVar.fullNameZh.get())
        self.tree.heading("displayNameEn",text=self.stringVar.displayNameEn.get())
        self.tree.heading("displayNameZh",text=self.stringVar.displayNameZh.get())
        self.tree.heading("recipientEmail",text=self.stringVar.recipientEmail.get())

        self.saveToDb = customtkinter.CTkButton(self,text=self.stringVar.save.get(),command=self.__SaveList)
        self.saveToDb.grid(row=3, column=1, sticky='nsew',padx=10, pady=10)

        self.clearEmail = customtkinter.CTkButton(master=self, text =self.stringVar.resetEmail.get(),command=self.__DeleteList,
                                                  fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.clearEmail.grid(row=3, column=2, pady = 10, padx = 10,sticky="nsew")

        pass

    def __selectInputPutDirectory(self):
        path = filedialog.askopenfilename()
        if path == '':
            return
        else:
            self.__recipientList = self.fileUtility.ReadEmailList(path)

            if self.__recipientList != None:
                for recipient in self.__recipientList:
                    self.tree.insert('','end',values=recipient)
    
    def __SaveList(self):

        if self.inputNameVar.get() == "" or self.inputNameVar.get() == None:
            messagebox.showerror(self.stringVar.errorMissingListName.get(), self.stringVar.errorMissingListName.get())
            return

        
        if self.tree.get_children == None or len(self.tree.get_children()) == 0:
            messagebox.showerror(self.stringVar.errorMissingList.get(), self.stringVar.errorMissingList.get())
            return
        

        idx = self.database.SaveEmailListName(self.inputNameVar.get())
        if idx == None or len(idx) == 0:
            messagebox.showerror(self.stringVar.errorInputListName.get(), self.stringVar.errorInputListName.get())
            return
        
        idx = idx[0]
        failed = []
        
        if self.__recipientList != None:
            for recipient in self.__recipientList:
                saveGroup  = self.database.SaveEmailGroup(recipient[4],idx)
                saveRecipient = self.database.SaveEmailRecipient(RecipientModel(recipient[0],recipient[1],recipient[2],recipient[3],recipient[4]))

                if not saveGroup or not saveRecipient:
                    failed.append(recipient[4])

            if len(failed) == 0:
                messagebox.showinfo(self.stringVar.createEmailListSuccess.get(), self.stringVar.createEmailListSuccess.get())
                self.operationType = self.__AddTemplate
                self.destroy()
                return
            else:
                displayString = self.stringVar.createEmailListFailed.get() + "\n"

                for email in failed:
                    displayString += email + "\n"

                displayString += self.stringVar.retry.get()

                messagebox.showerror(self.stringVar.createEmailListFailed.get(), displayString)
                return


        pass

    def __ClearList(self):
        self.inputNameVar.set("")

        for i in self.tree.get_children():
            self.tree.delete(i)

        try:
            self.inputNameOptionMenu.set(self.stringVar.defaultEmailGroup.get())
        except:
            pass

    def __DeleteList(self):
        if self.inputNameOptionMenu.get() == self.stringVar.defaultEmailGroup.get():
            messagebox.showerror(self.stringVar.defaultEmailGroup.get(), self.stringVar.defaultEmailGroup.get())
            return
        

        


    def _OnSelectEmailList(self,choice):
        if choice == self.stringVar.defaultTemplate.get():
            self.__selectedEmailName = choice
            pass
        else:
            recipientList = self.database.GetRecipientByGroupName(choice)

            if recipientList != None and len(recipientList) > 0:
                for recipient in recipientList:
                    self.tree.insert('','end',values=recipient.toList())
                pass
            else:
                pass
    pass