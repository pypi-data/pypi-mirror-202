
import customtkinter
from tkinter import DISABLED, NORMAL ,ttk
from src.Database.Repository.databaseRepository import GetDBRepositorySingletion

from src.Service.emailService import EmailService
from src.Logger.logger import Logger
from src.Utility.ConfigUtility import GetConfigSingletion
from src.Utility.StringUtilityCTK import GetStringSingletionCTK
from src.View.edit_template_top_level import EditTemplateTopLevel

class MainView(customtkinter.CTkFrame):

    editTemplateTopLevel = None

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
        self.emailAcLabel = customtkinter.CTkLabel(self, text=self.stringValue.emailAC.get()+self.emailService.GetEmailAccount())
        self.emailAcLabel.grid(row=0, column=0, pady = 10, padx = 10,sticky="w")

        self.emailLoginStatus = customtkinter.CTkLabel(self, text=self.stringValue.status.get()+self.stringValue.offline.get())
        self.emailLoginStatus.grid(row=0, column=3, pady = 10, padx = 10,sticky="e")

        # self.loginEmail = customtkinter.CTkButton(self,text = "Connect")
        # self.loginEmail.grid(row=0, column=2, pady = 10, padx = 10,sticky="nsew")

        # self.editEmail = customtkinter.CTkButton(self,text = "Edit")
        # self.editEmail.grid(row=0, column=3, pady = 10, padx = 10,sticky="nsew")


        #ROW1
        self.template = customtkinter.CTkOptionMenu(self,values=self.database.GetAllEmailTemplateName(),command=self._OnSelectEmailTemplate,dynamic_resizing=False)
        self.template.grid(row=1, column=0, pady = 10, padx = 10, sticky="nsew")

        self.attachData = customtkinter.CTkButton(self,text = self.stringValue.attachData.get())
        self.attachData.grid(row=1, column=1, pady = 10, padx = 10,sticky="nsew")

        self.editEmail = customtkinter.CTkButton(self,text = self.stringValue.editTemplate.get(),command=self._CreateEditTemplateTopLevel)
        self.editEmail.grid(row=1, column=3, pady = 10, padx = 10,sticky="nsew")


        #ROW2
        self.recipient = customtkinter.CTkOptionMenu(self,values=self.database.GetAllRecipientGroupName(),dynamic_resizing=False)
        self.recipient.grid(row=2, column=0, pady = 10, padx = 10, sticky="nsew")

        self.editRecipient = customtkinter.CTkButton(self,text = self.stringValue.editEmailList.get())
        self.editRecipient.grid(row=2, column=3, pady = 10, padx = 10,sticky="nsew")


        #ROW3
        self.leftFrame = customtkinter.CTkFrame(self)
        self.leftFrame.grid(row=3, column=0, columnspan=2, padx=(10,5), pady=(10,0), sticky="nsew")

        self.tree = ttk.Treeview(self.leftFrame,show='headings')
        self.tree["column"]=('Recipient','Email')
        self.tree.grid(row=0,column=0,rowspan=2,sticky='nsew')
        col_width = self.tree.winfo_width()
        self.tree.column("Recipient",width=col_width)
        self.tree.column("Email",width=col_width)
        self.tree.heading("Recipient",text="Recipient")
        self.tree.heading("Email",text="Email")
        self.tree.pack(fill='both',expand=1)

        
        self.tree.insert('','end',values=['Stanley','mat230821@hotmail.com'])
        self.tree.insert('','end',values=['Michelle','palamlam@hotmail.com'])

        
        self.rightFrame = customtkinter.CTkFrame(self)
        self.rightFrame.grid(row=3, column=2, columnspan=2, padx=(5,10), pady=(10,0), sticky="nsew")
        self.rightFrame.grid_columnconfigure(0, weight=1)
        self.rightFrame.grid_rowconfigure(0, weight=1)

        self.emailPreview = customtkinter.CTkTextbox(self.rightFrame)
        self.emailPreview.configure(state=DISABLED)
        self.emailPreview.grid(row=0, column=0,sticky="nsew")


        #ROW4
        self.attachmentStatus = customtkinter.CTkLabel(self, text=self.stringValue.attachment.get(),padx = 10)
        self.attachmentStatus.grid(row=4, column=3, columnspan=2,sticky="e")

        #ROW5
        self.sendEmail = customtkinter.CTkButton(self,text = self.stringValue.sendEmail.get())
        self.sendEmail.grid(row=5, column=2, pady = 10, padx = 10,sticky="nsew")

        self.clearEmail = customtkinter.CTkButton(master=self, text = self.stringValue.resetEmail.get(),fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.clearEmail.grid(row=5, column=3, pady = 10, padx = 10,sticky="nsew")

        self.InitView()

    pass


    def InitView(self):
        if self.emailService.ConnectEmailAccount():
            self.emailLoginStatus.after(100,self.emailLoginStatus.configure(text=self.stringValue.status.get()+self.stringValue.online.get()))
            pass
        else:
            self.emailLoginStatus.after(100,self.emailLoginStatus.configure(text=self.stringValue.status.get()+self.stringValue.offline.get()))
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
            pass
        else:
            emailTemplate = self.database.GetEmailTemplateByName(choice)

            if emailTemplate != None:
                file = open(emailTemplate.GetPath(),encoding="utf-8")#append mode 

                self.emailPreview.configure(state=NORMAL)
                self.emailPreview.delete("0.0","end")
                self.emailPreview.insert("0.0",file.read())
                self.emailPreview.configure(state=DISABLED)


                file.close()
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

