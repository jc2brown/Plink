

class Test:
    __shared_state = {}
    def __init__( self ):
        self.__dict__ = self.__shared_state
        if not 'bank' in self.__dict__:
            self.__dict__['bank'] = []
            
    def testbank(self):
        return self.__dict__['bank']
        
    def test(self, quiet=False):
        for mod, tst in self.testbank():
            try:
                tst()
            except AssertionError as message:
                print mod, ": ", message
                return False
        return True
    
    def register(self, mod, tst):
        if not tst in [ t for m, t in self.testbank() ]:
            self.testbank().append( (mod, tst) )

        

