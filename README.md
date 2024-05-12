# Person Name Normalisation

[![DOI](https://zenodo.org/badge/304649488.svg)](https://zenodo.org/doi/10.5281/zenodo.11182093)

### Unifying person names in different notations

different sources write person names in different notations:

-  Firstname Secondname Lastname
-  Lastname, Firstname Secondname

also extracted are:

- academic degrees (e.g. 'Dr.', 'Ph.D.')
- name prefixes (e.g. 'van ter', 'von', 'De')

included: german, french, italian, dutch

missing: spanish, portuguese



missing: double Lastnames in Spanish

## Installation
```bash
pip install personnamenorm
```

## Usage
```python
import personnamenorm as pnn
nameobj = pnn.namenorm('Dr. Dipl. Firstname Secondname von und zu Lastname')
```

##### results in

```python
nameobj.name <dict>
{
    'raw': 'Dr. Dipl. Firstname von und zu Lastname',
    'firstname': ['Firstname','Secondname'],
    'lastname': ['Lastname'],
    'title': ['Dr.','Dipl.'],
    'prefix': ['von und zu']
}

nameobj.fullname <str>
'von und zu Lastname, Firstname Secondname'

nameobj.fullname_abbrev <str>
'von und zu Lastname, F S'
```
more examples can be found in this [file](https://github.com/klauslippert/person-name-normalisation/blob/main/tests/test_personnamenorm.py)  on github. 

#### Debug-mode
by default debug mode is off.

activating the debug mode 
```python
nameobj = pnn.namenorm(<str>, True)
```
returns additional information as logging message.
- used annotation dictionary
- annotated input string as list of tuples

## Logging
logging is implemented

- writes to std-out if logging IS NOT enabled before 
- writes to the existing logging handler if other logging IS enabled before

## Test
see folder 'tests' on [github](https://github.com/klauslippert/person-name-normalisation).
```python
python test_personnamenorm.py
```

