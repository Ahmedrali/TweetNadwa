'''
Created on Aug 6, 2011

@author: Ahmed H.Ali
'''
class ThreadController():
    _map = {}
    
    @staticmethod
    def getNadwa(name):
        if ThreadController.isExist(name):
            return ThreadController._map[name]
        return None
    
    @staticmethod
    def addNadwa(name, threadObj):
        if not ThreadController.isExist(name):
            ThreadController._map[name] = threadObj
            return True
        return False
    
    @staticmethod
    def deleteNadwa(name):
        if ThreadController.isExist(name):
            del(ThreadController._map[name])
            return True
        return False
    
    @staticmethod
    def pauseNadwa(name):
        if ThreadController.isExist(name):
            threadObj = ThreadController.getNadwa(name)
            if not threadObj.isPaused() and threadObj.isRunning():
                threadObj.pauseTracking()
                return True
            return False
        return False
    
    @staticmethod
    def resumeNadwa(name):
        if ThreadController.isExist(name):
            threadObj = ThreadController.getNadwa(name)
            if threadObj.isPaused() and threadObj.isRunning():
                threadObj.resumeTraking()
                return True
            return False
        return False
    
    @staticmethod
    def startNadwa(name):
        if ThreadController.isExist(name):
            threadObj = ThreadController.getNadwa(name)
            if not threadObj.isRunning():
                threadObj.start()
                return True
            return False
        return False
    
    @staticmethod
    def stopNadwa(name):
        if ThreadController.isExist(name):
            threadObj = ThreadController.getNadwa(name)
            if threadObj.isRunning():
                threadObj.stop()
                return True
            return False
        return False
    
    @staticmethod
    def isRunning(name):
        threadObj = ThreadController.getNadwa(name)
        return threadObj.isRunning()
    
    @staticmethod
    def isPaused(name):
        threadObj = ThreadController.getNadwa(name)
        return threadObj.isPaused()
    @staticmethod
    def isExist(name):
        if name in ThreadController._map:
            return True
        return False
    
    @staticmethod
    def printMetaData():
        print "size of nadwa =  %s" %len(ThreadController._map)
        print "Nadwa = %s" %ThreadController._map
        