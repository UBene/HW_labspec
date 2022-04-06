'''
Created on Apr 5, 2022

@author: Benedikt Ursprung
'''
from ScopeFoundry.measurement import Measurement
import pyqtgraph as pg
from qtpy import QtWidgets

import numpy as np
from ScopeFoundry import h5_io


class LabspecReadout(Measurement):
    
    name = 'labspec_readout'
    
    
    def setup(self):
        self.settings.New('save_h5', bool, initial=True)
    
    def setup_figure(self):
        self.ui = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout(self.ui)
        
        start_pushButton = QtWidgets.QPushButton()
        self.layout.addWidget(start_pushButton)
        
        if hasattr(self, 'graph_layout'):
            self.graph_layout.deleteLater()  # see http://stackoverflow.com/questions/9899409/pyside-removing-a-widget-from-a-layout
            del self.graph_layout
        self.graph_layout = pg.GraphicsLayoutWidget(border=(100, 100, 100))
        self.layout.addWidget(self.graph_layout)

        # # Add plot and plot items
        self.plot = self.graph_layout.addPlot(title="Labspec")
        self.line = self.plot.plot()        
        self.data = {'wavelengths':np.arange(1024),
                     'spectrum':np.cos(np.arange(1024))}
        self.hw = self.app.hardware['labspec']
        
        self.settings.activation.connect_to_pushButton(start_pushButton)
        
    def run(self):
        self.data['wavelengths'] = self.hw.get_wavelengths()
        self.hw.dev.prepare_N_acquisition(1)
        self.hw.dev.timeout = 100
        self.data['spectrum'] = self.hw.get_spectrum()
        
        if self.settings['save_h5']:
            self.save_h5_data()
        
    def update_display(self):
        self.line.setData(self.data['wavelengths'], self.data['spectrum'])
        
    def save_h5_data(self):
        self.h5_file = h5_io.h5_base_file(app=self.app, measurement=self)
        self.h5_meas_group = h5_io.h5_create_measurement_group(self, self.h5_file)
        for k,v in self.data.items():
            self.h5_meas_group[k] = v
        self.h5_file.close()
