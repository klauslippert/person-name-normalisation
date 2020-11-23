import sys
import re
import ftfy

try:
    F=open(sys.argv[1])
    text=F.read()
    text=ftfy.fix_text(text)
    def findall(pattern,text):
        return [m.start() for m in re.finditer(pattern,text)]
    startsur=findall('<name><surname>',text)
    stopsur=findall('</given-names></name>',text)

    for x1,x2 in zip(startsur,stopsur):
        tt=text[x1:x2]
        tt=tt.replace('<name><surname>','')
        tt=tt.replace('</surname><given-names>',', ')
        tt=tt[:tt.find('<')]
        print(tt)
except:
    pass


