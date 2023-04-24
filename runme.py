from Benchmarks import Benchmarks


HR = Benchmarks(1/8.0, [0, 20], 4, type='HR')  #fs, ns, nc
HR.run_PES_Model()

GL = Benchmarks(1/9.0, [0, 6], 6, type='GL')
GL.run_PES_Model()

BP = Benchmarks(1/6.0, [0,10], 5, type='BP')
BP.run_PES_Model()

BO = Benchmarks(1/8.0, [0,12], 2, type='BO')
BO.run_PES_Model()

PN = Benchmarks(1/6.0, [0,6], 4, type='PN')
PN.run_PES_Model()

MP = Benchmarks(1/7.0, [8,8], 3, type='MP')
MP.run_PES_Model()

AES = Benchmarks(1/25.0, [0,3], 4, type='AES')
AES.run_PES_Model()

GM = Benchmarks(1/20.0, [0,2], 3, type='GM')
GM.run_PES_Model()

FFT = Benchmarks(1/25.0, [0,1], 3, type='FFT')
FFT.run_PES_Model()
