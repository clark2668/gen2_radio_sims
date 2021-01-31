README

The different folders contain various different levels of the simulation.

## Step 2
The “step2” folder contains the first pass at simulations. 
These are the simulation results produced with a single, noiseless dipole trigger.

## Step 3
The “step3” folder contains the second pass at simulations. 
These are the simulation results produced with a full phased array trigger with noise. 
This step is only run on the results of step2. 
This way, only events which are “plausible” to trigger receive the full phasing simulation.

## Step 4
The “step4” folder contains the merged files of step 3. 
Files are merged together in energy and zenith bands with the NuRadioMC merge utility (https://github.com/nu-radio/NuRadioMC/blob/master/NuRadioMC/utilities/merge_hdf5.py ). 
So, all of the files from step 3 for a single flavor, energy, and zenith band are combined, and saved here. 
The step 4 files are *not* a complete duplicate of the step 3 files. 
In particular, any output field which had multiplicity of “number of showers” was not copied in order save space (about a factor of 5 at the highest energies).

## Step 5
The “step5” folder contains the extracted high level effective volumes in pkl files. 
We wrote to disk the dictionary produced by the NuRadioMC get_Veff_Aeff function (https://github.com/nu-radio/NuRadioMC/blob/master/NuRadioMC/utilities/Veff.py#L411). 
The dictionaries stored in these pkl files can be input directly into the get_Veff_Aeff_array function (https://github.com/nu-radio/NuRadioMC/blob/master/NuRadioMC/utilities/Veff.py#L515 ).
