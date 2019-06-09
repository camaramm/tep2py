# Wrap Fortran code in Python using f2py (following the smart way)

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
