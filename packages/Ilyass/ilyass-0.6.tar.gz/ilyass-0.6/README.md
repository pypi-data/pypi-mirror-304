```bash
pip install Ilyass
```
```bash
#Check the email if is available in Hotmail or not 
```
from Ilyass import HotmailChecker

python = HotmailChecker.HotmailEm('example@hotmail.com')

if python == True:
  print('Email Valide')
else:
  print('Email Invalide')
