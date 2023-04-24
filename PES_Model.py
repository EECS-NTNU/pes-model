import sys
import numpy as np
import math
from config import*

class PES_Model:

	def __init__(self,Bench ):
			self.pS = Bench.pS
			self.tS = Bench.tS			
			self.cS = Bench.cS
			self.ds = Bench.ds
			self.sample_size = Bench.sample_size
			self.Ph = Bench.Ph
			self.wakeupThreshold = Bench.wakeupThreshold
			self.shutdownThreshold = Bench.shutdownThreshold
	def E_Sampling(self,ns):
		if (self.tS[0] ==0):
			ESL = 0
		else:
			ESL = self.pS[0] * self.cS[0] * ns[0];  
		ESH = self.pS[1] * self.cS[1] * ns[1]; 
		ES =  ESL + ESH;
		tSL = self.tS[0]  * ns[0]
		tSH = self.tS[1]  * ns[1];
		tS = tSL + tSH
		return ES,tS ;
	def E_C(self,fs,ns):
		nc = np.ceil(self.sample_size /(ns[1] *self.ds))
		e_con   = Eadv + Einit;
		e_trans = (np.ceil((ns[1] *self.ds)/dp)  )*(et +Epre_process /9)
		Eempty = Nempty * (e_keep_alive +Epre_process);

		Ec = e_con + e_trans + e_discon + Eempty ; 
		Ek =  0 ;
		Et = e_trans  ;
		return Ec,e_con,Et,Ek;
	def E_I(self,fs,ns):
		Ec,e_con,Et,Ek = self.E_C(fs,ns);
		Ei = 0;
		return Ei;
	def backup(self,E,t_ROI,ns):
		if nr ==0 :
			return 0 ,0;
		er = self.E_restore(ns);
		nb = (np.floor (ns[1] *self.ds))+16 #8 for header
		eb = AlphaB *nb + BetaB
		tB = 0.017e-3 * nb + 1.2757e-3
		tR = 0.0002e-3 * nb+ 0.7611e-3
			
		t_lostT = Tadv + Tinit + 1/f_keep_alive * Nempty
		t_lost = HistogramScale * t_lostT
		E_lostT = Eadv + Einit + (Tadv + Tinit + 1/f_keep_alive * Nempty) * Pidle_sleep + power_100ms * t_lostT + e_keep_alive * Nempty+ energy_background			
		E_lost = E_lostT*HistogramScale
		eCheckpointing = (er + eb+ startUpEnergy)		
		n_sd = np.ceil((E  - t_ROI * self.Ph - self.wakeupThreshold)  / (self.wakeupThreshold-self.shutdownThreshold))
		if n_sd <=0 :
			n_sd =0 
		else:
			if (self.wakeupThreshold-self.shutdownThreshold-E_lost-eCheckpointing + (t_lost + tB+tR) *self.Ph) > 0:
				n_sd = np.ceil((E  - t_ROI * self.Ph - self.wakeupThreshold)  / (self.wakeupThreshold-self.shutdownThreshold-E_lost-eCheckpointing + (t_lost + tB+tR) *self.Ph))			 
			else:
				print( f' low wakeupThreshold({self.wakeupThreshold}) , min is {self.shutdownThreshold+E_lost+eCheckpointing - (t_lost+tB+tR) *self.Ph}')
				exit()			 
		if n_sd <=0 :
			n_sd =0
			T_back_store = 0
		else:
			###3.6e-3 is avg of time for startup 	
			T_back_store = 	tB + tR + n_sd * 3.6e-3
		E_lost_total = n_sd * E_lost
		eCheckpointingT = n_sd * (er + eb+ startUpEnergy)				

		return E_lost_total,n_sd,t_lost,eCheckpointingT,T_back_store;
	def E_restore(self,ns):
		nb = (np.floor (ns[1] *self.ds)) +16
		er = AlphaR * nb+ BetaR
		return er;
	def E_idleSleep(self,fs,ns):
		t_off = 4 /f_keep_alive;
		ES,tS = self.E_Sampling(ns);
		T_communication = Tadv + Tinit + t_off+ T_after_init ; 
		tc_transfer = (np.ceil((ns[1] *self.ds)/dp) ) * (tTransfer1peak +Tpre_process/9)+ Nempty * (t_alive +Tpre_process);
		T_transfer = (np.ceil((ns[1] *self.ds)/dp/9)+ Nempty ) / f_keep_alive;
		tc_keepAlive = (np.floor ((f_keep_alive /fs)*(ns[0]+ns[1])))* (t_alive + Tpre_process);
		nc = np.ceil(self.sample_size /(ns[1] *self.ds))
		self.tc = tc_Adv + tc_init + tc_transfer + tc_off + Nempty *(t_alive +Tpre_process);
		tIs_check = T_transfer + T_communication;
		t_ROI = (1 / fs) * (ns[0]+ns[1]) * nc + tIs_check

		n_peak = nAdv + nInit +nBond + 4+(np.ceil(((ns[0]+ns[1]) *self.ds)/dp/9)+ Nempty )
		tIdleSleep = t_ROI - (nc *(ns[0] *self.tS[0]+ ns[1] *self.tS[1] + self.tc))
		Eis = Pidle_sleep * tIdleSleep
		return Eis,t_ROI,nc,tIs_check,n_peak*T_cpu_in_ble_peak,tIdleSleep ;
	def E_consuming(self,fs,ns):
		ES,tS = self.E_Sampling(ns);
		Ec,e_con,Et,Ek = self.E_C(fs,ns);
		Ei = self.E_I(fs,ns);
		Eis,t_ROI,nc,tIs_check,tST,tIdleSleep = self.E_idleSleep(fs,ns)
		E100ms = self.energy_t100ms(t_ROI)
		Ebackground = self.energy_Background(t_ROI)		
		self.E0 = 0 
		E00 =0
		E01 =0
		E_RoI = nc * (ES + Ec )+ Eis + Ei - self.E0 + E100ms + startUpEnergy0 + Ebackground; #without backup
		E_lost_total,n_sd,t_lost,eCheckpointingT,T_back_store = self.backup( E_RoI,  t_ROI ,ns) ;
		self.E0 = E00*(1+n_sd) + E01 
		E = nc * (ES + Ec )+ Eis + Ei - self.E0 + E100ms + E_lost_total + startUpEnergy0 + Ebackground + eCheckpointingT; #with backup				
		return E_RoI,E; 
	def Energy_supply(self,fs,ns):
		Eis,t_ROI,nc,tIs_check,tST,tIdleSleep = self.E_idleSleep(fs,ns)
		tDead,f_effective,EffectiveRatio,eDead,deepSleepTime0 = self.Dead(fs,ns)
		Eh = self.Ph * (t_ROI +tDead );
		return Eh;
	def Dead(self,fs,ns):
		E_RoI,E = self.E_consuming(fs,ns);
		Eis,t_ROI,nc,tIs_check,tST,tIdleSleep = self.E_idleSleep(fs,ns)
		E_lost_total,n_sd,t_lost,eCheckpointingT,T_back_store = self.backup( E_RoI,  t_ROI ,ns) ;
		if (self.Ph > Pdeep_sleep):
			tDead = n_sd*((self.wakeupThreshold-self.shutdownThreshold)/(self.Ph -Pdeep_sleep))+self.wakeupThreshold/(self.Ph-Pdeep_sleep)
		else:
			print('Harvesting Energy is less than Deep sleep energy. This system is infeasible')	
		eDead = tDead *Pdeep_sleep
		f_effective = fs * t_ROI / ( t_ROI + tDead);
		EffectiveRatio = t_ROI / ( t_ROI + tDead);
		deepSleepTime0 = self.wakeupThreshold /(self.Ph-Pdeep_sleep)
		return tDead,f_effective, EffectiveRatio,eDead,deepSleepTime0;
	def energy_t100ms(self,tRoi):
		return power_100ms * self.tc
	def energy_Background(self,tRoi):
		return energy_background * tRoi		
	def energyDistrubution(self,fs,ns) :
		ES,tS = self.E_Sampling(ns);
		E_RoI,E = self.E_consuming(fs,ns);
		Eh = self.Energy_supply(fs,ns);
		Eis,t_ROI,nc,tIs_check,tST,tIdleSleep = self.E_idleSleep(fs,ns)
		tDead,f_effective,EffectiveRatio,eDead,deepSleepTime0 = self.Dead(fs,ns)
		Ec,e_con,Et,Ek = self.E_C(fs,ns);
		E100ms = self.energy_t100ms(t_ROI)
		Ebackground = self.energy_Background(t_ROI)		
		E_lost_total,n_sd,t_lost,eCheckpointingT,T_back_store = self.backup( E_RoI,  t_ROI ,ns) ;
		Ei = self.E_I(fs,ns);
		print( 'self.Ph ,n_sd, tDead , t_ROI,E,resume',self.Ph ,n_sd, tDead ,t_ROI,E +eDead,self.wakeupThreshold)

		if (((tIs_check) > ((ns[0]+ns[1])/fs) or ( ns[1] * self.ds )  > 35000 )or (((ns[0]+ns[1])/fs)< (ns[0]*self.tS[0]+ns[1]*self.tS[1]+tST) )):
			Distrubution = {
				"E":0,
				"Eh":0,
				"E_lost_total":0,
				"eCheckpointingT":0,
				"ES":0,
				"tSampling":0 ,
				"Ec":0,
				"Ek":0,
				"Et":0,
				"Ei":0,
				"Eis":0,
				"EffectiveRatio":0,
				"f_effective":0,
				"Throughput":0,	
				"tIdleSleep":0,	
				"tComm":0,
				"tIs_check":0,
				"tDead":0,
				"tRunTime":0,								
				"tBR":0,
				"tLost":0,																																																																														
						}
			return Distrubution;
		else:
			Distrubution = {
				"E":E +eDead,
				"Eh":Eh,
				"E_lost_total":E_lost_total,
				"eCheckpointingT":eCheckpointingT,
				"ES":ES * nc ,
				"tSampling":tS * nc ,
				"Ec":Ec * nc - self.E0 + startUpEnergy0 + E100ms + Ebackground,				
				"Ek":Ek * nc - self.E0,
				"Et":Et * nc ,
				"Ei":Ei ,
				"EIs":Eis,
				"EDs":eDead,	
				"EDead": E_lost_total,																											
				"EffectiveRatio":EffectiveRatio,
				"f_effective":f_effective,
				"Throughput":ns[1] *self.ds * nc /(tDead +t_ROI-deepSleepTime0),	
				#"Throughput":ns[1] *self.ds * nc /(tDead +t_ROI),					
				"tIdleSleep":tIdleSleep,	
				"tComm":self.tc,
				"tIs_check":tIs_check,				
				"tDeepSleep":tDead,
				"tRunTime":tDead +t_ROI,								
				"tBR":T_back_store,
				"tLost":t_lost,																																																
				}
		return Distrubution;

