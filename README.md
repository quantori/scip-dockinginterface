# DockingInterface

## Requirements

Python 3.6 or higher is required

CMake (`cmake`) 2.8.12 or higher is required.

boost 1.53 or higher is required.
<br> For vina/qvina 
<br>(`libboost-program-options-dev`, `libboost-system-dev`, `libboost-thread-dev`, `libboost-filesystem-dev`)
<br> For smina, in addition to the libraries specified for vina / qvina, you need:
<br>(`libboost-regex-dev`, `libboost-serialization-dev`, `libboost-timer-dev`, `libboost-iostreams-dev`)

For smina, Openbabel `libopenbabel-dev` 2.4.1 or higher is required.

If installing system-wide boost and Openbabel is not an option, you can use a local installation (see BOOST_ROOT and OPENBABEL2_ROOT / OPENBABEL3_ROOT options below).


## Building libraries

1. Clone vina, smina, and qvina repositories.
2. In each of them, do:
   ```
    mkdir lib && cd lib
    cmake ..
    make %target_name%
   ```

Where `%target_name%` is `vinaDynamic`, `sminaDynamic`, or `qvinaDynamic` respectively.

If you have a multiprocessor machine, you can use a parallel build:

```make -j4 %target_name%```

You can provide BOOST_ROOT to cmake to use a specific boost installation:

```
cmake .. -DBOOST_ROOT=/path/to/my/boost
```

In smina, similar option is provided for Openbabel 2 or 3:

```
cmake .. -DOPENBABEL2_ROOT=/path/to/my/openbabel2
```

```
cmake .. -DOPENBABEL3_ROOT=/path/to/my/openbabel3
```

You are allowed to combine `BOOST_ROOT` with `OPENBABEL2_ROOT` or `OPENBABEL3_ROOT`,
but not the latter two.


## Installing DockingInterface

```
python3 -m pip install DockingInterface/
```


## Where to put libraries

By default the DockingInterface looking for the dynamic libraries in the *C_Dynamic_Libs* subfolder
of the DockingInterface source code. So you should copy or create symlinks for *qvina/lib/libqvinaDynamic.so*,
*smina/lib/libsminaDynamic.so* and *qvina/lib/libqvinaDynamic.so* into one of the following folders:

 - *DockingInterface/C_Dynamic_Libs/Linux/x86_64*
 - *DockingInterface/C_Dynamic_Libs/Linux/arm64*
 - *DockingInterface/C_Dynamic_Libs/macOS/x86_64*
 - *DockingInterface/C_Dynamic_Libs/macOS/arm64*
 - *DockingInterface/C_Dynamic_Libs/win*

depending on your system architecture. But you can re-configure this behaviour using an environment variable

    ```
    export DOCKING_LIBRARY_PATH=/usr/lib/DockingInterface:/usr/local/lib/DockingInterface
    ```

In the example above the libraries are expected in one of directory: */usr/lib/DockingInterface* and */usr/local/lib/DockingInterface*.


---

## Using Docking Interface (class DockingInterface)

Use `DockingInterface` to run vina/smina/qvina inside Python script without spawning sub-process.

### Initialization
First you call constructor with no arguments:
<br>```docking = DockingInterface()``` 

### Setting the parameters
1. ```set_handler('<handler>')``` - <handler> == vina or smina or qvina
2. ```docking.set_ligand(./path/to/your/ligand.pdbqt)``` - takes a path to pdbqt file
3. ```docking.set_center(x, y, z)``` - takes double values x, y, z
4. ```docking.set_size(x, y, z)``` - takes double values x, y, z
5. ```docking.set_exhaustiveness(exhaustiveness)``` - takes int value. Default == 8;
6. ```docking.set_log_file(./path/to/your/log.txt)``` - use this setter if you need all output in txt file - takes a path to txt file
7. ```docking.set_receptor(./path/to/your/receptor.pdbqt)``` - takes a path to pdbqt file
8. ```docking.set_config(./path/to/your/config.txt)```- takes a path to txt file. In config file must be center and size, may be exhaustiveness. You can use config or setter (center or size)
9. ```docking.set_output(./path/to/your/output.pdbqt)``` takes a path to pdbqt file
10. ```docking.set_autobox_ligand(./path/to/your/crystal_ligand.pdbqt)``` takes a path to pdbqt file
11. ```docking.set_scoring_function(scoring_function)``` takes scoring functions name. You can use:
   <br><t>9.1 ```ad4_scoring```
   <br><t>9.2 ```default```
   <br><t>9.3 ```dkoes_fast```
   <br><t>9.4 ```dkoes_scoring```
   <br><t>9.5 ```dkoes_scoring_old```
   <br><t>9.6 ```vina```
   <br><t>9.7 ```vinardo```
### Runing the docking
After the parameters are set up, call the `docking` method:

```docking.docking()```

### Geting the results
When docking ends, use this function to get results as list of lists of numbers:

<br>```result = docking.get_result()``` 
<br> After getting the result (it is an object of class `DockingResult`),
you can use getters:
<br> `result.get_number_of_models()` - get the number of models
<br> `result.get_values_by_index(i)` - for a given model index, get a list containing: model index, affinity, rms lower bound and upper bound.
<br> `result.get_model_by_index()` - get text (PDBQT) representation of the model by index

## Example
```
from DockingInterface import *

if __name__ == "__main__":
    docking = DockingInterface()
    docking.set_handler('qvina')
    docking.set_log_file('logfile.txt')
    docking.set_ligand('ligand.pdbqt')
    docking.set_receptor('receptor.pdbqt')
    docking.set_center(17.3564, 1.5176, 12.9464)
    docking.set_size(25.0, 25.0, 25.0)
    docking.set_exhaustiveness(8)
    docking.docking()
    result = docking.get_result()
    for i in range(a.get_number_of_models()):
        print(result.get_values_by_index(i))
        print(result.get_model_by_index(i))
```
