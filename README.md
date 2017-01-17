# python_postgrad_2017
Postgrad Python tutorial 2017

# Instructions

Open a terminal.

First, assuming you already have python, IPython, numpy and matplotlib installed on your machine, we also need to install jupyter. If you don't have the command `jupyter-notebook`, then run these two commands:
```
pip install jupyter --user
setenv PATH $HOME/.local/bin:$PATH
```

(if your shell is `bash`, the second line will be ```export PATH=$HOME/.local/bin:$PATH```).
The `pip` command might take a couple of minutes to complete.

Now get the tutorial notebook. Try:
```
git clone https://github.com/apcooper/python_postgrad_2017.git
```

If that doesn't work, [click here to download](https://github.com/apcooper/python_postgrad_2017/archive/master.zip), save and unzip the file.

Launch the tutorial:
```
cd python_postgrad_2017
jupyter-notebook 01-Introduction.pynb
```

(the directory will be called python_postgrad_2017-master if you downloaded the tutorial as a zip file).

 [![Binder](http://mybinder.org/badge.svg)](http://mybinder.org:/repo/apcooper/python_postgrad_2017) 
