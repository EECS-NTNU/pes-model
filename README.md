# PES-model

This repository contains the source code for PES model, An Energy and Throughput Model for Energy Harvesting IoT Systems. Periodic Energy Har-
vesting Systems (PES) model enables developers to explore energy versus throughput trade-offs early in the design process.

The README briefly describes how to use PES across different IoT benchmarks used to validate PES. The repository includes these files :
- PES_Model.py : Models the energy consumed by an IoT application during different states and predicts the number of shutdowns due to insufficient energy.
- config.py : Contains collection of average harvesting power, wake up and shutdown threshols and system specific energy and power consumption constants.
- Benchmarks.py : Includes IoT benchmarks and their specefic configuration. 
- runme.py : Run PES model for specefic benchmark.

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
* Determine Sampling frequency, communication incidence (for each sampling task), and communication events

```
HR = Benchmarks(1/8.0, [0, 20], 4, type='HR')
```
In above line example 1/8.0 , [0, 20] and 4 are chosen sampling frequency, communication incidence (there is one type of sampling task), and communication events respectively for HR benchmark.
* Run the PES model:
```
HR.run_PES_Model()
```

# Attribution and PES model-related Publications

If used for research, please cite PES model by the following publication: 
