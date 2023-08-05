import pandas as pd

class _FileUtilitySingletion():
    _fileInstance = None

    def __init__(self) -> None:
        pass


    def ReadEmailList(self,path):
        try:
            recipient_no_col = pd.read_excel(path,usecols='A:E',header=0,dtype=str)
            policy_no_list = recipient_no_col.values.tolist()
            return policy_no_list
        except:
            return None


def GetFileUtilitySingletion():
    if _FileUtilitySingletion._fileInstance is None:
        _FileUtilitySingletion._fileInstance = _FileUtilitySingletion()
    return _FileUtilitySingletion._fileInstance