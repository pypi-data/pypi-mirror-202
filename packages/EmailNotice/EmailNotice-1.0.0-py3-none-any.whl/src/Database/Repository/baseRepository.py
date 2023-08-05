from src.Utility.ConfigUtility import GetConfigSingletion
from src.Database.Repository.sqliteRepository import SqliteRepository


class _DatabaseRepository:

    _SQLITE = 'SQLITE'


    _dbInstance = None
    _databaseRepository = None


    def __init__(self) -> None:
        #Get config and check what db is using
        self.config_obj = GetConfigSingletion()
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



def GetDBRepositorySingletion():
    if _DatabaseRepository._dbInstance is None:
        _DatabaseRepository._dbInstance = _DatabaseRepository()
    return _DatabaseRepository._dbInstance