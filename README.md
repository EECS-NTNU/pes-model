# PES-model

This repository contains the source code for the PES model, An Energy and Throughput Model for Energy Harvesting IoT Systems. The Periodic Energy Harvesting Systems (PES) model enables developers to explore energy versus throughput trade-offs early in the design process.

The README briefly describes how to use PES across different IoT benchmarks. The repository includes these files :
- PES_Model.py : Models the energy consumed by an IoT application during different states and predicts the number of shutdowns due to insufficient energy.
- config.py : Contains a collection of average harvesting power, wake up and shutdown thresholds, and system specific energy and power consumption constants.
- Benchmarks.py : Includes IoT benchmarks and their specific configuration. 
- runme.py : Run PES model for a specific benchmark.

# Setting up PES model

For the scripts to work, you must first install:
Python version 3.10.6 or newer

Then, clone pes-model using the following command:
```
git clone https://github.com/EECS-NTNU/pes-model
```

Finally, enter the pes-model directory and run the PES model for specific configuration and benchmark:
```
cd pes-model
python3 runme.py
```
#Using PES model
* Select a benchmark from Benchmarks.py file
* Determine sampling frequency (fs), communication incidence (ns for each sampling task), and communication events (nc) 
* Write fs, ns, nc, and the benchmark's name like the following command inside the runme.py file. 

```
HR = Benchmarks(1/8.0, [0, 20], 4, type='HR')
```
For example, in the above command, 1/8.0, [0, 20], and 4 are chosen for sampling frequency, communication incidence (there is one type of sampling task in this example), and communication events, respectively, for HR benchmark.

* Run the PES model:
Write the following command inside the runme.py file
```
HR.run_PES_Model()
```
PES can predict infeasible, intermittent, and feasible systems by running python3 runme.py in the pes-model directory with the chosen configuration. In intermittent systems, PES also can predict the number of shutdowns (n_sd). There are more examples of different benchmarks in the runme.py file. 

In addition to changing sampling frequency, communication incidence, and communication events, PES enables more exploration by changing average harvesting power, wake up and shutdown thresholds, etc.

# Attribution and PES model-related Publications

If used for research, please cite PES model by the following publication: 
