import os

from win32com import client as wc

mypath = r'D:\repos\docpath'
all_FileNum = 0


def Translate(path):
    global all_FileNum
    '''
    将一个目录下所有 word文件 转成 txt文件
    '''
    files = os.listdir(path)
    for f in files:
        name, extname = os.path.splitext(f)
        if extname not in ['.doc', '.docx']:
            continue

        word = wc.Dispatch('Word.Application')
        doc = word.Documents.Open(os.path.join(path, f))
        doc.SaveAs(os.path.join(path, name) + '.txt', 4)
        doc.Close()
        all_FileNum = all_FileNum + 1


if __name__ == '__main__':
    Translate(mypath)
    print('文件总数 = ', all_FileNum)
