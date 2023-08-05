
import threading
import customtkinter
from tkinter import DISABLED, NORMAL, messagebox ,ttk

from PIL import Image

from pkg_resources import resource_stream
from era.Database.Repository.databaseRepository import GetDBRepositorySingletion

from era.Service.emailService import EmailService
from era.Logger.logger import Logger
from era.Utility.ConfigUtility import GetConfigSingletion
from era.Utility.StringUtilityCTK import GetStringSingletionCTK
from era.View.edit_email_list_top_level import EditEmailListTopLevel
from era.View.edit_template_top_level import EditTemplateTopLevel

class MainView(customtkinter.CTkFrame):

    editTemplateTopLevel = None
    editEmailTopLevel = None
    _selectedEmailTemplate = None
    _selectedEmailGroup = None

    def __init__(self,app):
        super().__init__(master=app,corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        customtkinter.CTkFrame.rowconfigure(self,0)
        customtkinter.CTkFrame.rowconfigure(self,1)
        customtkinter.CTkFrame.rowconfigure(self,2)
        customtkinter.CTkFrame.rowconfigure(self,3,weight=10)
        customtkinter.CTkFrame.rowconfigure(self,4)
        customtkinter.CTkFrame.rowconfigure(self,5)

        customtkinter.CTkFrame.columnconfigure(self,0,weight=1)
        customtkinter.CTkFrame.columnconfigure(self,1,weight=1)
        customtkinter.CTkFrame.columnconfigure(self,2,weight=1)
        customtkinter.CTkFrame.columnconfigure(self,3,weight=1)

        self.emailService = EmailService()
        self.logger = Logger()
        self.configParser = GetConfigSingletion()
        self.stringValue = GetStringSingletionCTK()
        self.database = GetDBRepositorySingletion()


        #ROW0
        # self.emailAc = customtkinter.CTkOptionMenu(self,values=["Gmail", "Microsoft"],dynamic_resizing=False)
        # self.emailAc.grid(row=0, column=0, pady = 10, padx = 10, sticky="nsew")
        self.emailAcLabel = customtkinter.CTkLabel(self, text=self.stringValue.emailAC.get()+self.emailService.GetEmailAccount(),font=("Arial bold", 15))
        self.emailAcLabel.grid(row=0, column=0, pady = 10, padx = 10,sticky="w")


        self.emailLoginStatusString = customtkinter.StringVar()
        self.refresh_image = customtkinter.CTkImage(light_image=Image.open(resource_stream('era', 'Assets/refresh-icon.png')),
                                            dark_image=Image.open(resource_stream('era', 'Assets/refresh-icon.png')), size=(30, 30))

        self.refresh_button = customtkinter.CTkButton(self, corner_radius=5, border_spacing=10,fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   command=self.RefreshEmailLoginStatus,image=self.refresh_image,textvariable=self.emailLoginStatusString,font=("Arial bold", 15))
        self.refresh_button.grid(row=0, column=3, sticky="e",pady = 5, padx = 10)


        # self.emailLoginStatus = customtkinter.CTkLabel(self, textvariable = self.emailLoginStatusString ,font=("Arial bold", 15))
        # self.emailLoginStatus.grid(row=0, column=3, pady = 10, padx = 10,sticky="e")

        # self.loginEmail = customtkinter.CTkButton(self,text = "Connect")
        # self.loginEmail.grid(row=0, column=2, pady = 10, padx = 10,sticky="nsew")

        # self.editEmail = customtkinter.CTkButton(self,text = "Edit")
        # self.editEmail.grid(row=0, column=3, pady = 10, padx = 10,sticky="nsew")


        #ROW1
        self.template = customtkinter.CTkOptionMenu(self,values=self.database.GetAllEmailTemplateName(),command=self._OnSelectEmailTemplate,dynamic_resizing=False)
        self.template.grid(row=1, column=0, pady = 10, padx = 10, sticky="nsew")

        # self.attachData = customtkinter.CTkButton(self,text = self.stringValue.attachData.get())
        # self.attachData.grid(row=1, column=1, pady = 10, padx = 10,sticky="nsew")

        self.editEmail = customtkinter.CTkButton(self,text = self.stringValue.editTemplate.get(),command=self._CreateEditTemplateTopLevel)
        self.editEmail.grid(row=1, column=3, pady = 10, padx = 10,sticky="nsew")


        #ROW2
        self.recipient = customtkinter.CTkOptionMenu(self,values=self.database.GetAllRecipientGroupName(),command=self._OnSelectEmailList,dynamic_resizing=False)
        self.recipient.grid(row=2, column=0, pady = 10, padx = 10, sticky="nsew")

        self.editRecipient = customtkinter.CTkButton(self,text = self.stringValue.editEmailList.get(),command=self.__CreateEditEmailTopLevel)
        self.editRecipient.grid(row=2, column=3, pady = 10, padx = 10,sticky="nsew")


        #ROW3
        self.leftFrame = customtkinter.CTkFrame(self)
        self.leftFrame.grid(row=3, column=0, columnspan=2, padx=(10,5), pady=(10,0), sticky="nsew")

        self.tree = ttk.Treeview(self.leftFrame,show='headings')
        self.tree["column"]=("fullNameEn","fullNameZh","displayNameEn","displayNameZh","recipientEmail")
        self.tree.grid(row=0,column=0,rowspan=2,sticky='nsew')
        col_width = self.tree.winfo_width()
        self.tree.column("fullNameEn",width=col_width)
        self.tree.column("fullNameZh",width=col_width)
        self.tree.column("displayNameEn",width=col_width)
        self.tree.column("displayNameZh",width=col_width)
        self.tree.column("recipientEmail",width=col_width)
        self.tree.heading("fullNameEn",text=self.stringValue.fullNameEn.get())
        self.tree.heading("fullNameZh",text=self.stringValue.fullNameZh.get())
        self.tree.heading("displayNameEn",text=self.stringValue.displayNameEn.get())
        self.tree.heading("displayNameZh",text=self.stringValue.displayNameZh.get())
        self.tree.heading("recipientEmail",text=self.stringValue.recipientEmail.get())

        self.tree.pack(fill='both',expand=1)

        self.rightFrame = customtkinter.CTkFrame(self)
        self.rightFrame.grid(row=3, column=2, columnspan=2, padx=(5,10), pady=(10,0), sticky="nsew")
        self.rightFrame.grid_columnconfigure(0, weight=1)
        self.rightFrame.grid_rowconfigure(0, weight=1)

        self.emailPreview = customtkinter.CTkTextbox(self.rightFrame)
        self.emailPreview.configure(state=DISABLED)
        self.emailPreview.grid(row=0, column=0,sticky="nsew")


        #ROW4
        # self.attachmentStatus = customtkinter.CTkLabel(self, text=self.stringValue.attachment.get(),padx = 10)
        # self.attachmentStatus.grid(row=4, column=3, columnspan=2,sticky="e")

        #ROW5
        self.sendEmail = customtkinter.CTkButton(self,text = self.stringValue.sendEmail.get(),command = self.__Send)
        self.sendEmail.grid(row=5, column=2, pady = 10, padx = 10,sticky="nsew")

        self.clearEmail = customtkinter.CTkButton(master=self, text = self.stringValue.resetEmail.get(),fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),command = self.__Clear)
        self.clearEmail.grid(row=5, column=3, pady = 10, padx = 10,sticky="nsew")
        self.InitView()

    pass


    def InitView(self):
        if self.emailService.ConnectEmailAccount():
            self.emailLoginStatusString.set(self.stringValue.status.get()+self.stringValue.online.get())
            pass
        else:
            self.emailLoginStatusString.set(self.stringValue.status.get()+self.stringValue.offline.get())
            pass
        pass

    def RefreshEmailLoginStatus(self):
        threading.Thread(target=self.__RefreshEmailLogin).start()


    def __RefreshEmailLogin(self):
        self.configParser.ReloadConfig()
        if self.emailService.ConnectEmailAccount():
            self.emailLoginStatusString.set(self.stringValue.status.get()+self.stringValue.online.get())
            #self.emailLoginStatus.after(100,self.emailLoginStatus.configure(text=self.stringValue.status.get()+self.stringValue.online.get()))
            pass
        else:
            self.emailLoginStatusString.set(self.stringValue.status.get()+self.stringValue.offline.get())
            #self.emailLoginStatus.after(100,self.emailLoginStatus.configure(text=self.stringValue.status.get()+self.stringValue.offline.get()))
            pass
        pass


    def _CreateEditTemplateTopLevel(self):
        if self.editTemplateTopLevel is None or not self.editTemplateTopLevel.winfo_exists():
            self.editTemplateTopLevel = EditTemplateTopLevel(xPos=self.winfo_rootx(),yPos=self.winfo_rooty())  # create window if its None or destroyed
            operation = self.editTemplateTopLevel.show()

            if operation != -1:
                self.template.configure(values = self.database.GetAllEmailTemplateName()) 
                self.template.set(self.stringValue.defaultTemplate.get())
                self.emailPreview.configure(state=NORMAL)
                self.emailPreview.delete("0.0","end")
                self.emailPreview.configure(state=DISABLED)
                return
            else:
                pass
        else:
            self.editTemplateTopLevel.focus()  # if window exists focus it
        
        pass

    def _OnSelectEmailTemplate(self,choice):
        if choice == self.stringValue.defaultTemplate.get():
            self._selectedEmailTemplate = None
            pass
        else:
            emailTemplate = self.database.GetEmailTemplateByName(choice)
            self._selectedEmailTemplate = emailTemplate

            if emailTemplate != None:
                file = open(emailTemplate.GetPath(),encoding="utf-8")#append mode 

                self.emailPreview.configure(state=NORMAL)
                self.emailPreview.delete("0.0","end")
                self.emailPreview.insert("0.0",file.read())
                self.emailPreview.configure(state=DISABLED)


                file.close()
                pass
    
    def _OnSelectEmailList(self,choice):
        if choice == self.stringValue.defaultTemplate.get():
            self._selectedEmailGroup = None
            pass
        else:
            recipientList = self.database.GetRecipientByGroupName(choice)

            if recipientList != None and len(recipientList) > 0:
                self._selectedEmailGroup = recipientList
                for recipient in recipientList:
                    self.tree.insert('','end',values=recipient.toList())
                pass
            else:
                pass


    def __CreateEditEmailTopLevel(self):
        if self.editEmailTopLevel is None or not self.editEmailTopLevel.winfo_exists():
            self.editEmailTopLevel = EditEmailListTopLevel(xPos=self.winfo_rootx(),yPos=self.winfo_rooty())  # create window if its None or destroyed
            operation = self.editEmailTopLevel.show()

            if operation != -1:
                self.recipient.configure(values = self.database.GetAllRecipientGroupName()) 
                self.recipient.set(self.stringValue.defaultEmailGroup.get())
                return
            else:
                pass
        else:
            self.editEmailTopLevel.focus()  # if window exists focus it
    
    def __Clear(self):

        self._selectedEmailTemplate = None
        self._selectedEmailGroup = None

        self.template.set(self.stringValue.defaultTemplate.get())
        self.recipient.set(self.stringValue.defaultEmailGroup.get())

        self.emailPreview.configure(state=NORMAL)
        self.emailPreview.delete("0.0","end")
        self.emailPreview.configure(state=DISABLED)
        
        for i in self.tree.get_children():
            self.tree.delete(i)
        pass

    def __Send(self):
        if not self.emailService.IsLogin():
            messagebox.showerror(self.stringValue.loginFailed.get(), self.stringValue.loginFailed.get())
            return

        if self._selectedEmailTemplate == None:
            messagebox.showerror(self.stringValue.defaultTemplate.get(), self.stringValue.defaultTemplate.get())
            return
        elif self._selectedEmailGroup == None or len(self._selectedEmailGroup) == 0:
            messagebox.showerror(self.stringValue.defaultEmailGroup.get(), self.stringValue.defaultEmailGroup.get())
            return
        
        errorList = self.emailService.SendEmail(self._selectedEmailGroup,self._selectedEmailTemplate)

        if len(errorList) == 0:
            messagebox.showinfo(self.stringValue.sendSuccess.get(), self.stringValue.sendSuccess.get())
            return
        else:
            errorMessage = self.stringValue.sendFailed.get() + "\n"
            for emailAddr in errorList:
                errorMessage += emailAddr + "\n"

            messagebox.showerror(self.stringValue.retry.get(), errorMessage)
            pass

        pass












customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("1000x1000")

# set grid layout 1x2
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

email = MainView(app)
email.grid(row=0, column=1, sticky="nsew")

app.mainloop()

