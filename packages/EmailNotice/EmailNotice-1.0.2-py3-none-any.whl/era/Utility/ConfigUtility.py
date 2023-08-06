import configparser
import os

class _ConfigSingleton:
    _configInstance = None
    _defaultINIPath = "C:\IPRA\config.ini"
    _defaultDirectory = "C:\IPRA"
    _defaultResouce = 'C:/IPRA/RESOURCE/'


    def __init__(self) -> None:
        self.config_obj = configparser.ConfigParser()
        configParam = self.config_obj.read(self._defaultINIPath)

        if len(configParam) == 0:
            #no config found,write default
            self.WriteAllDefault()
        else:
            #config found, check the related setting is existed
            self.CheckAndWriteDefault()
            pass
        pass


    def IsConfigExist(self,section,key):
        if not self.config_obj.has_section(section):
            return False
        else:
            if self.config_obj.has_option(section,key):
                return True
            else:
                return False
    
    def ReadConfig(self,section,key):
        #call IsConfigExist before
        try:
            return self.config_obj[section][key]
        except:
            return None
    
    def WriteConfig(self,section,key,value):
        if not self.config_obj.has_section(section):
            self.config_obj.add_section(section)


        self.config_obj.set(section=section,option=key,value=value)

        if not os.path.exists(self._defaultINIPath):
            os.makedirs(self._defaultDirectory,0o777)

        if not os.path.exists(self._defaultResouce):
            os.makedirs(self._defaultResouce,0o777)

        with open(self._defaultINIPath, 'w') as configfile:
            self.config_obj.write(configfile)

    def WriteAllDefault(self):
        self.WriteConfig('resource_path','resourcepath','C:/IPRA/RESOURCE/')
        self.WriteConfig('logger_path','loggerpath','C:/IPRA/LOG/')
        self.WriteConfig('language','display','zh')
        self.WriteConfig('database','type','SQLITE')
        self.WriteConfig('database','repository','C:/IPRA/RESOURCE/era.db')
        self.WriteConfig('email','smtpServer','smtp.xxxxx.com')
        self.WriteConfig('email','port','smtp.xxxxx.com')
        self.WriteConfig('email','emailac','xxxxxx@email.com')
        self.WriteConfig('email','emailpw','Abc12345')

        if not os.path.exists(self._defaultResouce):
            os.makedirs(self._defaultResouce,0o777)
    
    def CheckAndWriteDefault(self):
        if not self.IsConfigExist('resource_path','resourcepath'):
            self.WriteConfig('resource_path','resourcepath','C:/IPRA/RESOURCE/')

        if not self.IsConfigExist('logger_path','loggerpath'):
            self.WriteConfig('loggerpath','loggerpath','C:/IPRA/LOG/')

        if not self.IsConfigExist('language','display'):
            self.WriteConfig('language','display','zh')

        if not self.IsConfigExist('database','type'):
            self.WriteConfig('database','type','SQLITE')

        if not self.IsConfigExist('database','repository'):
            self.WriteConfig('database','repository','C:/IPRA/RESOURCE/era.db')

        if not self.IsConfigExist('email','smtpServer'):
            self.WriteConfig('email','smtpServer','smtp.xxxxx.com')

        if not self.IsConfigExist('email','port'):
            self.WriteConfig('email','port','587')
            
        if not self.IsConfigExist('email','emailac'):
            self.WriteConfig('email','emailac','xxxxxx@email.com')

        if not self.IsConfigExist('email','emailpw'):
            self.WriteConfig('email','emailpw','Abc12345')

        if not os.path.exists(self._defaultResouce):
            os.makedirs(self._defaultResouce,0o777)            

    def ReloadConfig(self):
        self.config_obj.read(self._defaultINIPath)

def GetConfigSingletion():
    if _ConfigSingleton._configInstance is None:
        _ConfigSingleton._configInstance = _ConfigSingleton()
    return _ConfigSingleton._configInstance