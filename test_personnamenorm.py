##################################
## testing module personnamenorn
##################################

import personnamenorm 


## input for pnn.unify
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
'first !§$%&/\=?*+#-_.:;<>| last',
'! § $ % & / \ = ? * + # - _ . : ; < > | last',
'first ! § $ % & / \ = ? * + # - _ . : ; < > |',
"FirstLast",
"FirstSecond Last",
"FirstSecondLast",
"first d'Last",
"d'Last, first",
"first 123 last",
"1234 567",
"Dr. Last",
"PhD Last,",
"MBA ,First",
'first von   und zu last',
'FIRST VON LAST',
'FIRST von LAST',
'first Von last',
'last,First',
'Van Last',
'DR first last',
'first last-last1',
'first second last-last1',
'Last1-Last, First',
'Last1-Last First',
'Last-last1',
'first second last last1',
'last last1, first second',
'last last1 first second',
'last last1, first-second',
'last last1 first-second',
'first last-second',
'last-second first',
'First DiLast',
'van den Last, First',
'First van den Last',
'van den Last First',
'First Last van den',
"O'Last, First",
"First O'Last",
"O'Last First",
"Last, First S.T.",
"Last, First SxT.",
"Last, First c/o company",
"Last, Firstc/o company",

]

## expected output from pnn.unify(<input>);pnn.name
target = [
{'raw':'first last','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':[], 'fullname': 'Last, First', 'fullname_abbrev': 'Last, F'},
{'raw':'  first   last ','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':[], 'fullname': 'Last, First', 'fullname_abbrev': 'Last, F'},
{'raw':'first second last','firstname':['First','Second'], 'lastname':['Last'],'title':[],'prefix':[], 'fullname': 'Last, First Second', 'fullname_abbrev': 'Last, F S'},
{'raw':'first second third last','firstname':['First','Second','Third'], 'lastname':['Last'],'title':[],'prefix':[], 'fullname': 'Last, First Second Third', 'fullname_abbrev': 'Last, F S T'},
{'raw':'Last, First','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':[], 'fullname': 'Last, First', 'fullname_abbrev': 'Last, F'},
{'raw':'Last, First Second','firstname':['First','Second'], 'lastname':['Last'],'title':[],'prefix':[], 'fullname': 'Last, First Second', 'fullname_abbrev': 'Last, F S'},
{'raw':'Last, First Second Third','firstname':['First','Second','Third'], 'lastname':['Last'],'title':[],'prefix':[], 'fullname': 'Last, First Second Third', 'fullname_abbrev': 'Last, F S T'},
{'raw':'first last \n company','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':[], 'fullname': 'Last, First', 'fullname_abbrev': 'Last, F'},
{'raw':'first last¶ company','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':[], 'fullname': 'Last, First', 'fullname_abbrev': 'Last, F'},
{'raw':'first last \n street\n company','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':[], 'fullname': 'Last, First', 'fullname_abbrev': 'Last, F'},
{'raw':'first \t last','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':[], 'fullname': 'Last, First', 'fullname_abbrev': 'Last, F'},
{'raw':'fÃ¶rst last','firstname':['Foerst'], 'lastname':['Last'],'title':[],'prefix':[], 'fullname': 'Last, Foerst', 'fullname_abbrev': 'Last, F'},
{'raw':'first (123) last','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':[], 'fullname': 'Last, First', 'fullname_abbrev': 'Last, F'},
{'raw':'first [123] last','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':[], 'fullname': 'Last, First', 'fullname_abbrev': 'Last, F'},
{'raw':'first {123} last','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':[], 'fullname': 'Last, First', 'fullname_abbrev': 'Last, F'},
{'raw':'first (123) last (MBA)','firstname':['First'], 'lastname':['Last'],'title':['MBA'],'prefix':[], 'fullname': 'Last, First', 'fullname_abbrev': 'Last, F'},
{'raw':'Dr. first last','firstname':['First'], 'lastname':['Last'],'title':['Dr.'],'prefix':[], 'fullname': 'Last, First', 'fullname_abbrev': 'Last, F'},
{'raw':'Dr. first second last','firstname':['First','Second'], 'lastname':['Last'],'title':['Dr.'],'prefix':[], 'fullname': 'Last, First Second', 'fullname_abbrev': 'Last, F S'},
{'raw':'Dr. Last, First','firstname':['First'], 'lastname':['Last'],'title':['Dr.'],'prefix':[], 'fullname': 'Last, First', 'fullname_abbrev': 'Last, F'},
{'raw':'Dr. Last, First Second','firstname':['First','Second'], 'lastname':['Last'],'title':['Dr.'],'prefix':[], 'fullname': 'Last, First Second', 'fullname_abbrev': 'Last, F S'},
{'raw':'PhD first last','firstname':['First'], 'lastname':['Last'],'title':['PhD'],'prefix':[], 'fullname': 'Last, First', 'fullname_abbrev': 'Last, F'},
{'raw':'PhD first second last','firstname':['First','Second'], 'lastname':['Last'],'title':['PhD'],'prefix':[], 'fullname': 'Last, First Second', 'fullname_abbrev': 'Last, F S'},
{'raw':'PhD Last, First','firstname':['First'], 'lastname':['Last'],'title':['PhD'],'prefix':[], 'fullname': 'Last, First', 'fullname_abbrev': 'Last, F'},
{'raw':'PhD Last, First Second','firstname':['First','Second'], 'lastname':['Last'],'title':['PhD'],'prefix':[], 'fullname': 'Last, First Second', 'fullname_abbrev': 'Last, F S'},
{'raw':'Ph.D. first last','firstname':['First'], 'lastname':['Last'],'title':['Ph.D.'],'prefix':[], 'fullname': 'Last, First', 'fullname_abbrev': 'Last, F'},
{'raw':'Ph.D. first second last','firstname':['First','Second'], 'lastname':['Last'],'title':['Ph.D.'],'prefix':[], 'fullname': 'Last, First Second', 'fullname_abbrev': 'Last, F S'},
{'raw':'Ph.D. Last, First','firstname':['First'], 'lastname':['Last'],'title':['Ph.D.'],'prefix':[], 'fullname': 'Last, First', 'fullname_abbrev': 'Last, F'},
{'raw':'Ph.D. Last, First Second','firstname':['First','Second'], 'lastname':['Last'],'title':['Ph.D.'],'prefix':[], 'fullname': 'Last, First Second', 'fullname_abbrev': 'Last, F S'},
{'raw':'first di last','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':['di'],'fullname': 'di Last, First', 'fullname_abbrev': 'di Last, F'},
{'raw':'first von und zu last','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':['von und zu'], 'fullname': 'von und zu Last, First', 'fullname_abbrev': 'von und zu Last, F'},
{'raw':'first ! § $ % & / \ = ? * + # - _ . : ; < > | last','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':[], 'fullname': 'Last, First', 'fullname_abbrev': 'Last, F'},
{'raw':'first !§$%&/\=?*+#-_.:;<>| last','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':[], 'fullname': 'Last, First', 'fullname_abbrev': 'Last, F'},
{'raw':'! § $ % & / \ = ? * + # - _ . : ; < > | last','firstname':[], 'lastname':['Last'],'title':[],'prefix':[], 'fullname': 'Last,', 'fullname_abbrev': 'Last,'},
{'raw':'first ! § $ % & / \ = ? * + # - _ . : ; < > |','firstname':[], 'lastname':['First'],'title':[],'prefix':[], 'fullname': 'First,', 'fullname_abbrev': 'First,'},
{'raw':"FirstLast",'firstname':['First'], 'lastname':['Last'],'title':[], 'prefix':[], 'fullname': "Last, First",'fullname_abbrev': "Last, F"},
{'raw':"FirstSecond Last",'firstname':['First','Second'], 'lastname':['Last'],'title':[],'prefix':[], 'fullname': 'Last, First Second', 'fullname_abbrev': 'Last, F S'},
{'raw':"FirstSecondLast",'firstname':['First','Second'], 'lastname':['Last'],'title':[],'prefix':[], 'fullname': 'Last, First Second', 'fullname_abbrev': 'Last, F S'},
{'raw':"first d'Last",'firstname':['First'], 'lastname':['Last'],'title':[],'prefix':["d"], 'fullname': "d Last, First", 'fullname_abbrev': "d Last, F"},
{'raw':"d'Last, first",'firstname':['First'], 'lastname':['Last'],'title':[], 'prefix':["d"], 'fullname': "d Last, First",'fullname_abbrev': "d Last, F"},
{'raw':"first 123 last",'firstname':['First'], 'lastname':['Last'],'title':[], 'prefix':[], 'fullname': "Last, First",'fullname_abbrev': "Last, F"},
{'raw':"1234 567",'firstname':[], 'lastname':[],'title':[], 'prefix':[], 'fullname': "",'fullname_abbrev': ""},
{'raw':"Dr. Last",'firstname':[], 'lastname':['Last'],'title':['Dr.'], 'prefix':[], 'fullname': "Last,",'fullname_abbrev': "Last,"},
{'raw':"PhD Last,",'firstname':[], 'lastname':['Last'],'title':['PhD'], 'prefix':[], 'fullname': "Last,",'fullname_abbrev': "Last,"},
{'raw':"MBA ,First",'firstname':[], 'lastname':['First'],'title':['MBA'], 'prefix':[], 'fullname': "First,",'fullname_abbrev': "First,"},
{'raw':'first von   und zu last','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':['von und zu'], 'fullname': 'von und zu Last, First', 'fullname_abbrev': 'von und zu Last, F'},
{'raw':'FIRST VON LAST','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':['von'], 'fullname': 'von Last, First', 'fullname_abbrev': 'von Last, F'},
{'raw':'FIRST von LAST','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':['von'], 'fullname': 'von Last, First', 'fullname_abbrev': 'von Last, F'},
{'raw':'first Von last','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':['von'], 'fullname': 'von Last, First', 'fullname_abbrev': 'von Last, F'},
{'raw':'last,First','firstname':['First'], 'lastname':['Last'],'title':[],'prefix':[], 'fullname': 'Last, First', 'fullname_abbrev': 'Last, F'},
{'raw':'Van Last','firstname':[], 'lastname':['Last'],'title':[],'prefix':['van'], 'fullname': 'van Last,', 'fullname_abbrev': 'van Last,'},
{'raw':'DR first last','firstname':['First'], 'lastname':['Last'],'title':['DR'],'prefix':[], 'fullname': 'Last, First', 'fullname_abbrev': 'Last, F'},
{'raw':'first last-last1','firstname':['First'], 'lastname':['Last','Last1'],'title':[], 'prefix':[], 'fullname': 'Last-Last1, First','fullname_abbrev': 'Last-Last1, F'},
{'raw':'first second last-last1','firstname':['First','Second'], 'lastname':['Last','Last1'],'title':[], 'prefix':[], 'fullname': 'Last-Last1, First Second','fullname_abbrev': 'Last-Last1, F S'},
{'raw':'Last1-Last, First','firstname':['First'], 'lastname':['Last1','Last'],'title':[], 'prefix':[], 'fullname': 'Last1-Last, First','fullname_abbrev': 'Last1-Last, F'},
{'raw':'Last1-Last First','firstname':['First'], 'lastname':['Last1','Last'],'title':[], 'prefix':[], 'fullname': 'Last1-Last, First','fullname_abbrev': 'Last1-Last, F'},
{'raw':'Last-last1','firstname':[], 'lastname':['Last','Last1'],'title':[], 'prefix':[], 'fullname': "Last-Last1,",'fullname_abbrev': "Last-Last1,"},
{'raw':'first second last last1','firstname':['First','Second'], 'lastname':['Last','Last1'],'title':[], 'prefix':[], 'fullname': "Last Last1, First Second",'fullname_abbrev': "Last Last1, F S"},
{'raw':'last last1, first second','firstname':['First','Second'], 'lastname':['Last','Last1'],'title':[], 'prefix':[], 'fullname':"Last Last1, First Second",'fullname_abbrev': "Last Last1, F S"},
{'raw':'last last1 first second','firstname':['First','Second'], 'lastname':['Last','Last1'],'title':[], 'prefix':[], 'fullname':"Last Last1, First Second",'fullname_abbrev': "Last Last1, F S"},
{'raw':'last last1, first-second','firstname':['First','Second'], 'lastname':['Last','Last1'],'title':[], 'prefix':[], 'fullname':"Last Last1, First-Second",'fullname_abbrev': "Last Last1, F"},
{'raw':'last last1 first-second','firstname':['First','Second'], 'lastname':['Last','Last1'],'title':[], 'prefix':[], 'fullname':"Last Last1, First-Second",'fullname_abbrev': "Last Last1, F"},
{'raw':'first last-second','firstname':['First'], 'lastname':['Last','Second'],'title':[], 'prefix':[], 'fullname': 'Last-Second, First','fullname_abbrev': "Last-Second, F"},
{'raw':'last-second first','firstname':['First'], 'lastname':['Last','Second'],'title':[], 'prefix':[], 'fullname': 'Last-Second, First','fullname_abbrev': "Last-Second, F"},
{'raw':'First DiLast','firstname':['First'], 'lastname':['Last'],'title':[], 'prefix':['di'], 'fullname': "di Last, First",'fullname_abbrev': "di Last, F"},
{'raw':'van den Last, First','firstname':['First'], 'lastname':['Last'],'title':[], 'prefix':['van den'], 'fullname': "van den Last, First",'fullname_abbrev': "van den Last, F"},
{'raw':'First van den Last','firstname':['First'], 'lastname':['Last'],'title':[], 'prefix':['van den'], 'fullname': "van den Last, First",'fullname_abbrev': "van den Last, F"},
{'raw':'van den Last First','firstname':['First'], 'lastname':['Last'],'title':[], 'prefix':['van den'], 'fullname': "van den Last, First",'fullname_abbrev': "van den Last, F"},
{'raw':'First Last van den','firstname':['First'], 'lastname':['Last'],'title':[], 'prefix':['van den'], 'fullname': "van den Last, First",'fullname_abbrev': "van den Last, F"},
{'raw':"O'Last, First",'firstname':['First'], 'lastname':["O Last"],'title':[], 'prefix':[], 'fullname': "O Last, First",'fullname_abbrev': "O Last, F"},
{'raw':"First O'Last",'firstname':['First'], 'lastname':["O Last"],'title':[], 'prefix':[], 'fullname': "O Last, First",'fullname_abbrev': "O Last, F"},
{'raw':"O'Last First",'firstname':['First'], 'lastname':["O Last"],'title':[], 'prefix':[], 'fullname': "O Last, First",'fullname_abbrev': "O Last, F"},
{'raw':"Last, First S.T.",'firstname':['First S T'], 'lastname':["Last"],'title':[], 'prefix':[], 'fullname': "Last, First S T",'fullname_abbrev': "Last, F S T"},
{'raw':"Last, First SxT.",'firstname':['First Sx T'], 'lastname':["Last"],'title':[], 'prefix':[], 'fullname': "Last, First Sx T",'fullname_abbrev': "Last, F S T"},
{'raw':"Last, First c/o company",'firstname':['First'], 'lastname':["Last"],'title':[], 'prefix':[], 'fullname': "Last, First",'fullname_abbrev': "Last, F"},
{'raw':"Last, Firstc/o company",'firstname':['First'], 'lastname':["Last"],'title':[], 'prefix':[], 'fullname': "Last, First",'fullname_abbrev': "Last, F"},

]


#{'raw':'','firstname':['First'], 'lastname':['Last'],'title':[], 'prefix':['van den'], 'fullname': "van den Last, First",'fullname_abbrev': "van den Last, F"},

pnn=personnamenorm.namenorm(debug=False)

## adding p values to the dict for this tests
pnn.p_firstname['first']=0.6
pnn.p_firstname['foerst']=0.6
pnn.p_firstname['second']=0.6
pnn.p_firstname['third']=0.6
pnn.p_firstname['last']=0.1
pnn.p_firstname['last2']=0.4
pnn.p_firstname['last1']=0.3





## start testing
test_pass = 0
test_fail  = 0

for i, (thisinput,thistarget) in enumerate(zip(inputdata,target)):
    try:
        _=pnn.unify(thisinput)
        actual = pnn.name
        if thistarget['fullname'].lower() == actual['fullname'].lower():
            print(str(i).zfill(3),'OK   ',thisinput,'-> ',actual['fullname'])
            test_pass += 1
        else:
            print(str(i).zfill(3),'ERROR target:',thistarget,'\n'\
              '          actual:',actual)
            test_fail += 1
    except:
        print(str(i).zfill(3),' FATAL ERROR',thistarget)

print('#'*50)
print(f'{len(target)} tests done. {test_pass} successful. {test_fail} failed.')







