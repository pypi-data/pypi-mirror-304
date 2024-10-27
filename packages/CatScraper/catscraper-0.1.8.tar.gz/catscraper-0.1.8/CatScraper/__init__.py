import Epate
import pandas as pd
class UListError(Exception):

    def __init__(self, message):
        self.message = message


class CSRunningError(Exception):

    def __init__(self, message):
        self.message = message

ul = None

def setUList(ulist):
    global ul
    if ul is None:
        ul = ulist
    else:
        raise UListError(
            'UList is seted,use setUList() to set it.')


def delUList():
    global ul
    if ul is not None:
        ul = None
    else:
        raise UListError(
            'UList is not seted,use setUList() to set it.'
        )


def like(workid: str, times: int):
    global ul
    if ul is not None:
        for i in range(times):
            Epate.login(ul[i]['un'], ul[i]['pw'])
            doing = Epate.like(workid)
            if doing != '200':
                raise CSRunningError(
                    f'failure of the {i+1} operation,HTTPCode is {doing}.')
            Epate.logout()
    else:
        raise UListError(
            'UList is not seted,use setUList() to set it.'
        )


def coll(workid:str, times:int):
    global ul
    if ul is not None:
        for i in range(times):
            Epate.login(ul[i]['un'], ul[i]['pw'])
            doing = Epate.coll(workid)
            if doing != '200':
                raise CSRunningError(
                    f'failure of the {i+1} operation,HTTPCode is {doing}.')
            Epate.logout()
    else:
        raise UListError(
            'UList is not seted,use setUList() to set it.'
        )


def fork(workid:str, times:int):
    global ul
    if ul is not None:
        for i in range(times):
            Epate.login(ul[i]['un'], ul[i]['pw'])
            doing = Epate.fork(workid)
            if doing != '200':
                raise CSRunningError(
                    f'failure of the {i+1} operation,HTTPCode is {doing}.')
            Epate.logout()
    else:
        raise UListError(
            'UList is not seted,use setUList() to set it.'
        )

def comment_workshop(wsid:str, times:int,data:str):
    global ul
    if ul is not None:
        for i in range(times):
            Epate.login(ul[i]['un'], ul[i]['pw'])
            doing = Epate.comment.work_shop(wsid,data)
            if str(doing) != '201':
                raise CSRunningError(
                    f'failure of the {i+1} operation,HTTPCode is {doing}.')
            Epate.logout()
    else:
        raise UListError(
            'UList is not seted,use setUList() to set it.'
        )

def toUList(dir: str):
    xls_files = [f for f in dir if f.endswith('.xls')]

    UList = []

    for file in xls_files:
        df = pd.read_excel(file, engine='openpyxl')
        row_count = df.shape[0]

        username_data = df.iloc[4:int(row_count), 1].tolist()
        password_data = df.iloc[4:int(row_count), 2].tolist()
        for i in range(len(username_data)):
            UList.append({'un': username_data[i], 'pw': password_data[i]})
    return(UList)