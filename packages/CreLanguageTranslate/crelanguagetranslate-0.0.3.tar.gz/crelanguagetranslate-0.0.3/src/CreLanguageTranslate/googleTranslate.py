from CreLanguageTranslate import TranslateBase

import deep_translator
from deep_translator import GoogleTranslator



##        translatorList.append(GoogleTranslator(source=language, target=newLanguage))
##        translatorList.append(MyMemoryTranslator(source=language, target=newLanguage)) 
##         if((not language in ['ar','he','no','se','ud','ur']) and (not newLanguage in ['ar','he','no','se','ud','ur'])):
##            translatorList.append(LingueeTranslator(source=language, target=newLanguage))
## 

##
## dupl: ['long', 'chinese (simplified)', 'short', 'zh-CN']
##       ['long', 'chinese (traditional)', 'short', 'zh-TW']
## https://de.wikipedia.org/wiki/Liste_der_ISO-639-Sprachcodes
## wrong: ['long', 'cebuano', 'short', 'ceb', 'iso', 'ce']
##        ['long', 'hawaiian', 'short', 'haw', 'iso', 'ha']
##        ['long', 'hmong', 'short', 'hmn', 'iso', 'hm']

class googleTranslate(TranslateBase):

    ## https://stackoverflow.com/questions/9056957/correct-way-to-define-class-variables-in-python
    ## class variable vs instance variable

    sourceLanguages = []
    targetLanguages = []
    callCounter = 0
    totalTextLength = 0 
    isoDictionary = {}

    maxTextLength = 5000

    def __init__(self):
        allLanguages = GoogleTranslator().get_supported_languages(as_dict=True)
        for langLong in allLanguages:
            langShort = allLanguages[langLong] 
            langIso = langShort[0:2]                              #better split on "-"
            print(['long',langLong,'short',langShort,'iso',langIso])
            ## ['long', 'chinese (simplified)', 'short', 'zh-CN']
            ## ['long', 'chinese (traditional)', 'short', 'zh-TW']
            googleTranslate.isoDictionary[langIso] = langShort    #overwrites! better collect, then select random
            if(not langShort in googleTranslate.sourceLanguages):
              googleTranslate.sourceLanguages.append(langIso)
            if(not langShort in googleTranslate.targetLanguages):
              googleTranslate.targetLanguages.append(langIso)

    def getServiceName(self):
        return 'google'

    def translate(self, sourceText, sourceLanguage, targetLanguage):
        googleTranslate.callCounter += 1
        googleTranslate.totalTextLength += len(sourceText)
        gt = GoogleTranslator(source=googleTranslate.isoDictionary[sourceLanguage], target=googleTranslate.isoDictionary[targetLanguage]) 
        targetText = gt.translate(sourceText)
        return targetText




