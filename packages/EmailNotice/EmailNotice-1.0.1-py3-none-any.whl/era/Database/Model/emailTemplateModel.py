class EmailTemplateModel:

    _idx = 0
    _path = None
    _name = None
    _containData = None
    _containAttachment = None
    _subject = None

    def __init__(self,path,name,containData,containAttachment,subject) -> None:
        self._path = path
        self._name = name
        self._containData = containData
        self._containAttachment = containAttachment
        self._subject = subject
        pass

    def __init__(self,path,name,containData,containAttachment,subject,idx) -> None:
        self._path = path
        self._name = name
        self._containData = containData
        self._containAttachment = containAttachment
        self._subject = subject
        self._idx = idx
        pass


    def GetPath(self):
        return self._path
    
    def GetName(self):
        return self._name

    def GetContainData(self):
        return self._containData
    
    def GetContainAttachment(self):
        return self._containAttachment
    
    def GetSubject(self):
        return self._subject
    
    def GetIdx(self):
        return self._idx
    
    def SetPath(self, path):
        self._path = path

    def SetName(self, name):
        self._name = name

    def SetContainData(self,containData):
        self._containData = containData
    
    def SetContainAttachment(self,containAttachment):
        self._containAttachment = containAttachment
    
    def SetSubject(self,subject):
        self._subject = subject