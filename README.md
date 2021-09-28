# tep2py

This repository provides a Python interface to a modified Fortran program of the Tennessee Eastman Process (TEP) Control Test Problem provided by [gmxavier](https://github.com/gmxavier/TEP-meets-LSTM).
Users of this modified version should cite it as:

> G. M. Xavier and J. M. de Seixas, "Fault Detection and Diagnosis in a Chemical Process using Long Short-Term Memory Recurrent Neural Network", 2018 International Joint Conference on Neural Networks (IJCNN), 2018, pp. 1-8, doi: 10.1109/IJCNN.2018.8489385.

In order to use it properly, you should build the fortran program from source using *f2py*.
You may refer to the instructions below to build it yourself or, if you are on a linux system, you may try the file provided in this repository, which was compiled on a linux machine according to:
```
$ uname -srvmpio
Linux 4.15.0-51-generic #55-Ubuntu SMP Wed May 15 14:27:21 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
```

## How to use

```python
# modules
import numpy as np 
from tep2py import tep2py

# matrix of disturbances
idata = np.zeros((5,20))  

# instantiate tep2py object for given `idata`
tep = tep2py(idata)

# run simulation
tep.simulate()

# retrieve simulated data as DataFrame
print(tep.process_data)

# retrieve table of disturbances
print(tep.info_disturbance)

# retrieve table of variables
print(tep.info_variable)
```

## Wrap Fortran code in Python using f2py (following the smart way)

See [this](https://docs.scipy.org/doc/numpy/f2py/getting-started.html#the-smart-way) for more details.

1. Create a signature file from fortran source code by running:

    ```
    $ python -m numpy.f2py src/tep/temain_mod.f src/tep/teprob.f -m temain_mod -h temain_mod-auto.pyf
    ```

2. Explicit what are the intent of the arguments of the target functions (use `intent(in)` and `intent(out)` attribute) . You should do this by editing the signature file `temain_mod-auto.pyf`.

    The final version is:
    
    ```
    subroutine temain(npts,nx,idata,xdata,verbose) ! in :temain_mod:temain.f
            integer, intent(in) :: npts
            integer, intent(in) :: nx
            integer dimension(nx,20), intent(in), depend(nx) :: idata
            double precision dimension(nx,52),depend(nx), intent(out) :: xdata
            integer, intent(in) :: verbose
    ```

3. Build the extension module by running:

    ```
    python -m numpy.f2py -c temain_mod-smart.pyf src/tep/temain_mod.f src/tep/teprob.f
    ```

4. Import the module in python:

    ```
    import temain_mod
    ```
