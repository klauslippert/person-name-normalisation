import personnamenorm 
import string


pnn=personnamenorm.namenorm(debug=True)


## add initials   ## still needed ?
#for x in string.ascii_lowercase:
#    pnn.p_firstname[x]=1
#pnn.p_firstname[x+'.']=1
    
#pnn.p_firstname['jr'] = 1
#pnn.p_firstname['jr.'] = 1




## adding p values to the dict for this tests
pnn.p_firstname['first']=1
pnn.p_firstname['second']=1
pnn.p_firstname['third']=1
pnn.p_firstname['last']=1e-4
pnn.p_firstname['last2']=1e-4

#pnn.unify('Martin Roland '.lower())
#pnn.unify('MartinBettina '.lower())
#pnn.unify('Dr. von  und zu Förstner-Schmidt Konrad Ulrich  h. (MBA)')
#pnn.unify('Dr. Last')
#pnn.unify('Dr. Last-Last2')
#pnn.unify('Dr. Konrad U. Förstner (MBA)'.lower())
#print(pnn._get_p_word('konrad'))
#pnn.unify('Herrmann-Krotz Gabrielle')
#pnn.unify('Mueller Anna-Maria Markus')
#pnn.unify('FirstLast')
#pnn.unify('first von und zu last')
#pnn.unify('first ! § $ % & / \\ = ? * + # - _ . : ; < > | last')

#pnn.unify('Johannes Cornelis PAS VAN DE')
#pnn.unify('Friso Bernard Jan ASSEMA von')
#pnn.unify('Friso Bernard Jan von ASSEMA')
#pnn.unify('JUSTA MACNEIL Stacey Ann')
#pnn.unify('Stacey Ann JUSTA MACNEIL')
#pnn.unify('Celine SAVARIAR HAUCK')	                                 
#pnn.unify('VAN KOPPENHAGEN Juanita E')
#pnn.unify('Juanita E. VAN KOPPENHAGEN')
#pnn.unify('Ronald B. Fisher')
#pnn.unify('Valentino K. Stella')	                            #Stella, Valentino K
#pnn.unify('Robert P. Kimberly')
#pnn.unify('Nelson S. Yew')
#pnn.unify('Jonn Stefan')
#pnn.unify('Charles E. Jr. Davis')
#pnn.unify('G. Rodney Jr. Nelson')
#pnn.unify('M. Victor Wickerhauser')
#pnn.unify('J. Richard Gyory')
#pnn.unify('Sauerwein Till')
#pnn.unify('Leyla Jael Garcia Castro')
#pnn.unify(' Garcia   Castro Leyla Jael ')
#pnn.unify(' Norbert Walter Borjans ')
#pnn.unify('Maria del Pilar del Toro')
#pnn.unify('del Toro Maria del Pilar')
#pnn.unify("Navsaria, P.H.")
#pnn.unify("Clevert, J. D.A. Max")
#pnn.unify("Shu, Xiao-Ou")
#pnn.unify('Ph.D. Last, First')
#pnn.unify('PhD Last, ')
#pnn.unify('Last, First, second, third')
#pnn.unify('First, Second, Last')    
#pnn.unify('Thomas J. VAN DAN ELZEN')    
#pnn.unify('Thomas J. von ELZEN (MBA)')    
#pnn.unify('DE BEI, Claudio')
#pnn.unify('Claudio DE BEI')
#pnn.unify('Last, First SxT.')
#pnn.unify('Marco Robin VAN HESSEM	')
#pnn.unify('Hemminga, M.A.')
#pnn.unify('Waard, M.A., de')
#pnn.unify('Van Khoa,  Le')
#pnn.unify("Mannetje, L., 't")
#pnn.unify("Cham ' Mead ', Jennifer A")
#pnn.unify("Fariña, Silvia")
pnn.unify("Netherlands)), (The")

from pprint import pprint
pprint(pnn.name)
print('version:',personnamenorm.__version__)



#python setup.py sdist bdist_wheel
#pip install --force-reinstall dist/personnamenorm-XXX.whl

