# Person Name Normalisation
## Description
#### unifying person names in different notations
different sources write person names in different notations:

-  Firstname Secondname Lastname
-  Lastname, Firstname Secondname


## Usage
```python
import personnamenorm as pnn
nameobj = pnn.namenorm('Dr. Firstname Secondname von und zu Lastname')
```

#### results in

``
```python
nameobj.name <dict>
{
    'raw': 'Dr. Dipl. Firstname von und zu Lastname',
    'Firstname': ['Firstname','Secondname'],
    'Lastname': ['Lastname'],
    'title': ['Dr.','Dipl.'],
    'prefix': ['von und zu']
}

nameobj.fullname <str>
'von und zu Lastname, Firstname Secondname'

nameobj.fullname_abbrev <str>
'von und zu Lastname, F S'

```
more examples can be found in the github test-folder


#### debug-mode
by default debug mode is off.
```python
nameobj = pnn.namenorm(<str>, True)
```
returns additional information as logging message:

- used annotation dictionary
- annotated input string as list of tuples

## Logging
logging is implemented

- and writes to std-out if logging is NOT enabled before 
- and to the existing logging handler if other logging is enabled before



## Test


