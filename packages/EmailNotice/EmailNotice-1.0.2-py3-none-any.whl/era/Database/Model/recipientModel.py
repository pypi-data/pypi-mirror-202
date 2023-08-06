class RecipientModel:

    _fullNameEn = None
    _fullNameZh = None
    _displayNameEn = None
    _displayNameZh = None
    _recipientEmail = None

    def __init__(self,fullNameEn,fullNameZh,displayNameEn,displayNameZh,recipientEmail):
        self._fullNameEn = fullNameEn
        self._fullNameZh = fullNameZh
        self._displayNameEn = displayNameEn
        self._displayNameZh = displayNameZh
        self._recipientEmail = recipientEmail

    def GetFullNameEn(self):
        return self._fullNameEn
    
    def GetFullNameZh(self):
        return self._fullNameZh

    def GetDisplayNameEn(self):
        return self._displayNameEn
    
    def GetDisplayNameZh(self):
        return self._displayNameZh
    
    def GetRecipientEMail(self):
        return self._recipientEmail
    
    def SetFullNameEn(self,fullNameEn):
        self._fullNameEn = fullNameEn
    
    def SetFullNameZh(self,fullNameZh):
        self._fullNameZh = fullNameZh

    def SetDisplayNameEn(self,displayNameEn):
        self._displayNameEn = displayNameEn
    
    def SetDisplayNameZh(self,displayNameZh):
        self._displayNameZh = displayNameZh
    
    def SetRecipientEMail(self,recipientEmail):
        self._recipientEmail = recipientEmail

    def toList(self):
        return [self._fullNameEn,self._fullNameZh,self._displayNameEn,self._displayNameZh,self._recipientEmail]
