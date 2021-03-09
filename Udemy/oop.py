
### Working on my understanding of OOP

class MaxSizeList:
    def __init__(self,max):
        self.maxSize = max
        self.list = []
    def push(self,item):
        if len(self.list) == self.maxSize:
            self.list.pop(0)
            self.list.append(item)
        else:
            self.list.append(item)
    def get_list(self,):
        return self.list


a = MaxSizeList(3)
b = MaxSizeList(1)
a.push('1')
a.push('2')
a.push('3')
a.push('4')

b.push('1')
b.push('2')
b.push('3')
b.push('4')

print(a.get_list())
print(b.get_list())

import csv
class WritetoFile:
    def __init__(self,fileName):
        self.fileName = fileName
    def write(self,msg):
        print('Define Write!')
class LogFile(WritetoFile):
    def __init__(self, fileName):
        WritetoFile.__init__(self,fileName)
        self.file = open(f'{self.fileName}','a')
    def write(self,msg):
        self.file.write(msg+'\n')
class DelimFile(WritetoFile):
    def __init__(self,fileName,delim):
        WritetoFile.__init__(self,fileName)
        self.delim = delim
        with open(self.fileName,'w',newline='') as file:
            self.writer = csv.writer(file,delimiter=self.delim)
    def write(self,list):
        with open(self.fileName,'a',newline='') as file:
            self.writer = csv.writer(file,delimiter=self.delim)
            self.writer.writerow(list)

log = LogFile('log.txt')
c = DelimFile('text.csv',',')

log.write('This is a log message')
log.write('This is another log message')

c.write(['a','b','c'])
c.write(['1','2','3'])










