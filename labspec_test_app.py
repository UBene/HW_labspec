'''
Created on Apr 5, 2022

@author: RAMAN
'''
from ScopeFoundry import BaseMicroscopeApp

import logging
logging.basicConfig(level=logging.DEBUG)

class SpecTestApp(BaseMicroscopeApp):

    name = 'labspec_test_app'
    
    def setup(self):
        from ScopeFoundryHW.labspec.labspec_hw import LabspecHW
        self.add_hardware(LabspecHW(self))
        
        from ScopeFoundryHW.labspec.labspec_readout import LabspecReadout
        self.add_measurement(LabspecReadout(self))
        

if __name__ == '__main__':
    import sys
    app = SpecTestApp(sys.argv)
    sys.exit(app.exec_())