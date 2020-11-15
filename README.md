# Particles

## Thesis

This particle simulator was created to assist with my masters thesis project on decentralised algorithms for area coverage. To follow the code, it may be easiest to read parts of the thesis first, which I have also uploaded to git (see `Masters_Thesis.pdf` at the top level).

## Building the project on linux or OSX
The project is written in Python 3
To ensure that the correct dependencies are installed, start by creating a new virtual environment.
If you do not have `pip` and `virtualenv` installed, run:

```
sudo python3 -m ensurepip --default-pip
sudo python3 -m pip install --upgrade pip
sudo python3 -m pip install virtualenv
```

Now create a new virtual environment and install the required packages:
```
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
``` 

## Running the project

It should now be possible to run a simulation from the forecast config, for example:
```
python3 coverage.py LOW_NOISE_COMPARISON 1
```
For testing purposes, it might help to set the `ITERATIONS=100` and `N=100` in `coverageconfig.py` so that the simulations run faster.
Results will be saved in the `results` folder, and data from the runs should be saved in the `data` folder.
You can see an animation of one of the simulations by executing the particle simulator, e.g.
```
python particlesim.py "data/low noise electrostatic repulsion" 5
```
