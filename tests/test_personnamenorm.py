##################################
## testing module personnamenorn
##################################

import personnamenorm as pnn

## input for pnn.namenorm
inputdata=[
'first last',
'  first   last ',
'first second last',
'first second third last',
'Last, First',
'Last, First Second',
'Last, First Second Third',
'first last \n company',
'first last¶ company',
'first last \n street\n company',
'first \t last',
'fÃ¶rst last',
'first (123) last',
'first [123] last',
'first {123} last',
'first (123) last (MBA)',
'Dr. first last',
'Dr. first second last',
'Dr. Last, First',
'Dr. Last, First Second',
'PhD first last',
'PhD first second last',
'PhD Last, First',
'PhD Last, First Second',
'Ph.D. first last',
'Ph.D. first second last',
'Ph.D. Last, First',
'Ph.D. Last, First Second',
'first di last',
'first von und zu last',
'first ! § $ % & / \ = ? * + # - _ . : ; < > | last',
"first d'Last",
"d'Last, first",
]

## expected output from pnn.namenorm(<input>).name
target = [
{'raw':'first last','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':[]},
{'raw':'  first   last ','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':[]},
{'raw':'first second last','firstname':['First','Second'], 'lastname':['Last'],'title':[],'prefix':[]},
{'raw':'first second third last','firstname':['First','Second','Third'], 'lastname':['Last'],'title':[],'prefix':[]},
{'raw':'Last, First','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':[]},
{'raw':'Last, First Second','firstname':['First','Second'], 'lastname':['Last'],'title':[],'prefix':[]},
{'raw':'Last, First Second Third','firstname':['First','Second','Third'], 'lastname':['Last'],'title':[],'prefix':[]},
{'raw':'first last \n company','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':[]},
{'raw':'first last¶ company','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':[]},
{'raw':'first last \n street\n company','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':[]},
{'raw':'first \t last','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':[]},
{'raw':'fÃ¶rst last','firstname':['Först'], 'lastname':['Last'],'title':[],'prefix':[]},
{'raw':'first (123) last','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':[]},
{'raw':'first [123] last','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':[]},
{'raw':'first {123} last','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':[]},
{'raw':'first (123) last (MBA)','firstname':['First'], 'lastname':['Last'],'title':['MBA'],'prefix':[]},
{'raw':'Dr. first last','firstname':['First'], 'lastname':['Last'],'title':['Dr.'],'prefix':[]},
{'raw':'Dr. first second last','firstname':['First','Second'], 'lastname':['Last'],'title':['Dr.'],'prefix':[]},
{'raw':'Dr. Last, First','firstname':['First'], 'lastname':['Last'],'title':['Dr.'],'prefix':[]},
{'raw':'Dr. Last, First Second','firstname':['First','Second'], 'lastname':['Last'],'title':['Dr.'],'prefix':[]},
{'raw':'PhD first last','firstname':['First'], 'lastname':['Last'],'title':['PhD'],'prefix':[]},
{'raw':'PhD first second last','firstname':['First','Second'], 'lastname':['Last'],'title':['PhD'],'prefix':[]},
{'raw':'PhD Last, First','firstname':['First'], 'lastname':['Last'],'title':['PhD'],'prefix':[]},
{'raw':'PhD Last, First Second','firstname':['First','Second'], 'lastname':['Last'],'title':['PhD'],'prefix':[]},
{'raw':'Ph.D. first last','firstname':['First'], 'lastname':['Last'],'title':['Ph.D.'],'prefix':[]},
{'raw':'Ph.D. first second last','firstname':['First','Second'], 'lastname':['Last'],'title':['Ph.D.'],'prefix':[]},
{'raw':'Ph.D. Last, First','firstname':['First'], 'lastname':['Last'],'title':['Ph.D.'],'prefix':[]},
{'raw':'Ph.D. Last, First Second','firstname':['First','Second'], 'lastname':['Last'],'title':['Ph.D.'],'prefix':[]},
{'raw':'first di last','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':['di']},
{'raw':'first von und zu last','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':['von und zu']},
{'raw':'first ! § $ % & / \ = ? * + # - _ . : ; < > | last','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':[]},
{'raw':"first d'Last",'firstname':['First'], 'lastname':['Last'],'title':[],'prefix':["d'"]},
{'raw':"d'Last, first",'firstname':['First'], 'lastname':['Last'],'title':[],'prefix':["d'"]},
]


## start testing
test_pass = 0
test_fail  = 0

for i, (thisinput,thistarget) in enumerate(zip(inputdata,target)):
    actual = pnn.namenorm(thisinput,False).name
    if thistarget == actual:
        print(str(i+1).zfill(3),'OK   ',thisinput)
        test_pass += 1
    else:
        print(str(i+1).zfill(3),'ERROR target:',thistarget,'\n'\
              '          actual:',actual)
        test_fail += 1

print('#'*50)
print('checked only the resulting dictionary pnn.namenorm(<str>).name')
print(f'{len(target)} tests done. {test_pass} successful. {test_fail} failed.')




