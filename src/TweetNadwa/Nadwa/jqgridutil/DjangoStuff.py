'''
Created on Apr 3, 2011

@author: aali
'''
from datetime import datetime, date
from datetime import time as dtTime
import time
import logging
from django.utils import simplejson as json

class DjangoStuff:
    def readRequest_handler(self, request):
        logging.debug("***** Django readRequest -> Handler")
        page = int(request.GET['page'])
        limit = int(request.GET['rows'])
        sidx = request.GET['sidx']
        sord = request.GET['sord']
        search = request.GET['_search']
        filter = ''
        if search == 'true':
            filter = request.GET['filters']
            filter = json.loads(filter)
        custom_search = request.GET['custom_search']
        custom_filter = ''
        if custom_search == 'true':
            custom_filter = request.GET['custom_filter']
            custom_filter = json.loads(custom_filter)
        return (page, limit, sidx, sord, search, filter, custom_search, custom_filter)
    
    def readRequest_javaScript(self, request):        
        htmlTableGrid = request.GET['htmlTableGrid']
        htmlDivPager = request.GET['htmlDivPager']
        handlerURL = request.GET['handlerURL']
        editURL = request.GET['editURL']
        gridCaption = request.GET['gridCaption']
        logging.debug("***** Django readRequest -> JS(%s, %s, %s, %s, %s)" %(htmlTableGrid, htmlDivPager, handlerURL, editURL, gridCaption))
        return (htmlTableGrid, htmlDivPager, handlerURL, editURL, gridCaption)
    
    def readRequest_editHandler(self, request, AllMembers):
        operation =  request.POST['oper']
        attrMap = {}
        validate = True
        if operation != 'del':
            for member in AllMembers:
                try:
                    val = request.POST[member]
                    attrMap[member] = val
                except:
                    pass
            (validate, attrMap) = self.validation(AllMembers, attrMap)
        logging.critical("***** Django editHandler -> (%s)" %attrMap)
        if validate:
            id = request.POST['id']
            attrMap['id'] = id
            return (operation, attrMap)
        else:
            return ('err', '')
    
    def validation(self, entityProperties, propertiesValues):
        validate = True
        attrObjMap = {}
        try:
            for prop in entityProperties:
                obj = entityProperties[prop]
                val = propertiesValues[prop]
                attrObjMap[prop] = val
        except:
            validate = False
        return (validate, attrObjMap)

