from ScopeFoundryHW.labspec.labspec_client import Labspec6Client

from ScopeFoundry.hardware import HardwareComponent

class LabspecHW(HardwareComponent):
    
    name = 'labspec'
    
    def setup(self):
        
        self.settings.New('IP', str, initial='localhost')
        self.settings.New('port', int, initial=1234)
        self.settings.New('exposure_time', initial=1.0, ro=True)
        
        
    def connect(self):
        self.dev = Labspec6Client()

        S=self.settings
        self.dev.connect(S['IP'], S['port'])

        self.dev.get_x_axis() # need to call this first before anything else?     
        
    def disconnect(self):
        if hasattr(self, 'dev'):
            self.dev.close()
            del self.dev
                
    def get_spectrum(self):
        return self.dev.grab_spectrum()
    
    def get_wavelengths(self):
        return self.dev.get_x_axis()
        