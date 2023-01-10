
**Installation Instructions:**

If you participated in The Data Labs for differential and Integral Calculus, you are already familiar with Jupyter Lab and Thonny. We will be using Jupyter Lab, Thonny and Python throughout this course. Jupyter Lab is a development environment for using Jupyter Notebooks. Thonny is a development environment meant for smaller projects, with good tools for interacting with the Raspberry Pi Pico microcontroller.

**Installing Miniconda**

We will be using miniconda for installing python and managing all the libraries.

Download the miniconda installer from this [link](https://repo.anaconda.com/miniconda/Miniconda3-py310_22.11.1-1-Linux-x86_64.sh).

The installer will be downloaded to your machine usually to the Downloads folder.  
Open Terminal and move to the Downloads directory once the download is finished.

```bash
cd ~/Downloads
```

and run the installer by running this command.

```bash
sh Miniconda3-py310_22.11.1-1-Linux-x86_64.sh
```

Follow the instructions on the terminal to complete the installation.

**Testing the python installation.**

Open a new terminal window and type

```bash
python -–version
```

You will get an output like,

_Python 3.9.12_

if not there may be an issue with the installation. Please contact a TA for help.

**Creating a virtual environment.**

A virtual environment is used to isolate your project from other python projects. This is done so that the dependencies of the current project will not create conflicts with older projects.

You can easily create a virtual environment with the name "dslab" using conda by

```bash
conda create --name dslab
```

This will create a new environment dslab.

To activate the env, we use the command activate

```bash
conda activate dslab
```

if this is successful, bash will show "(dslab)" before your username at the next prompt.

and to deactivate dslab environment, we use the deactivate command in conda

```bash
conda deactivate
```

To list all the environments currently in the machine,

```bash
conda env list
```

**Installing Libraries and Dependencies**

For installing libraries and dependencies using conda, we can use conda install command.

example: to install numpy

```bash
conda install numpy
```

**Installing Jupyter lab**

If you already have jupyter lab installed, you can skip this step.

```bash
conda install jupyter
```

**Starting jupyter lab**

Go to terminal and type

```bash
jupyter lab
```

**Installing Thonny**

In order to install Thonny,  **copy and paste the following command into a terminal**, then press enter:

```bash
wget -O - https://github.com/thonny/thonny/releases/download/v3.3.13/thonny-3.3.13.bash
```

This will automatically create an icon on your desktop, which you can use to launch Thonny.
