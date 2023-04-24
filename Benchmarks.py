import sys
import numpy as np
import math
from config import*
from PES_Model import PES_Model

class Benchmarks:
	
	def __init__(self,fs,ns,nc,**kw):
		self.fs = fs
		self.ns = ns
		self.nc = nc
		if 'type' in kw:
			match kw['type']:
				case 'HR':
					self.name = kw['type'];
					self.pS = [0,13.036103697e-6]
					self.tS = [0,0.956197797e-3]
					self.ds = 4.0
					self.Ph = PhLow
					self.wakeupThreshold = wakeupThresholdLow
					self.shutdownThreshold = shutdownThresholdLow
		
		
				case 'GL':
					self.name = kw['type'];
					self.pS = [0,9.150782864e-6]
					self.tS = [0,0.798543294e-3]
					self.ds = 44.0
					self.Ph = PhLow
					self.wakeupThreshold = wakeupThresholdLow
					self.shutdownThreshold = shutdownThresholdLow

				case 'BP':
					self.name = kw['type'];
					self.pS = [0,24.055761199e-6]
					self.tS = [0,1.480102539e-3]
					self.ds = 36.0
					self.Ph = PhLow
					self.wakeupThreshold = wakeupThresholdLow
					self.shutdownThreshold = shutdownThresholdLow
					
				case 'BO':
					self.name = kw['type'];
					self.pS = [0,326.388224008e-6]
					self.tS = [0,15.526072184e-3]
					self.ds = 4.0
					self.Ph = PhLow
					self.wakeupThreshold = wakeupThresholdLow
					self.shutdownThreshold = shutdownThresholdLow	
										
				case 'PN':
					self.name = kw['type'];
					self.pS = [0,54.443262723e-6]
					self.tS = [0,2.896457248e-3]
					self.ds = 4.0
					self.Ph = PhLow
					self.wakeupThreshold = wakeupThresholdLow
					self.shutdownThreshold = shutdownThresholdLow

				case 'MP':
					self.name = kw['type'];
					self.pS = [52.055992955e-06,114.957911823e-06]
					self.tS = [2.883911133e-03,5.651108762e-03]
					self.ds = 4.0
					self.Ph = PhLow
					self.wakeupThreshold = wakeupThresholdLow
					self.shutdownThreshold = shutdownThresholdLow

				case 'AES':
					self.name = kw['type'];
					self.pS = [0,515.3440566e-6]
					self.tS = [0,23.288302951e-3]
					self.ds = 2704.0
					self.Ph = PhHigh 
					self.wakeupThreshold = wakeupThresholdHigh
					self.shutdownThreshold = shutdownThresholdHigh
					
				case 'GM':
					self.name = kw['type'];
					self.pS = [0,861.902953512e-6]
					self.tS = [0,37.970648872e-3]
					self.ds = 4096.0
					self.Ph = PhHigh 
					self.wakeupThreshold = wakeupThresholdHigh
					self.shutdownThreshold = shutdownThresholdHigh
					
				case 'FFT':
					self.name = kw['type'];
					self.pS = [0,23.796619446e-6]
					self.tS = [0,1.627604167e-3]
					self.ds = 8192.0
					self.Ph = PhHigh 
					self.wakeupThreshold = wakeupThresholdHigh
					self.shutdownThreshold = shutdownThresholdHigh
					
					
		self.sample_size = ns[1] * nc * self.ds	
		self.cS = np.array(self.tS) * 64 * 1000000;
		if(self.cS[0] != 0 ):
			self.pS[0] =self.pS[0]/self.cS[0]
		if(self.cS[1] != 0 ):
			self.pS[1] =self.pS[1]/self.cS[1]
		
	def run_PES_Model(self):
		analyzer_PES_Model = PES_Model(self)
		analyzer_PES_Model .energyDistrubution(self.fs, self.ns);
			



