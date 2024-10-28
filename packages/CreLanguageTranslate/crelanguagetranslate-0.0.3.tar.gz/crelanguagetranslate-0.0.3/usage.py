from CreLanguageTranslate import LanguageTranslate 

lt = LanguageTranslate()
li = lt.getTranslatorByLanguage('en','de')
tar = li.translate('tree')
print(tar)
tar2 = li.translate('house')
print(tar2)

translateInstance.getTranslatorInfo()


