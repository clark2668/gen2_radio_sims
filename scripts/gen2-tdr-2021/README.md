# Gen2 Radio Simulations
repository for gen2 radio sims stuff, this specific one deals with TDR

- [Overview](#overview)
- [Simulation Tools and Steps](#simulation-tools-and-steps)
  * [step 1](#step-1)
  * [step 2](#step-2)
  * [step3](#step3)
- [Logistical Details](#logistical-details)
  * [Setting up the software](#setting-up-the-software)
  * [Submitting jobs](#submitting-jobs)
  * [git maintenance](#git-maintenance)

## Overview

For an overview, go to the central radio production scripts [repo](https://github.com/nu-radio/analysis-scripts/tree/gen2-tdr-2021/gen2-tdr-2021/production_scripts).

## Simulation Tools and Steps

The helper script, and the step 0 script has been standardized into the radio analysis scripts directory. Check [there](https://github.com/nu-radio/analysis-scripts/tree/gen2-tdr-2021/gen2-tdr-2021/production_scripts).

### step 1
Step 1 is the process where we actually run the `.py` control files created in step 0 to generate the list of energy depositions. Running `python make_step1_dag.py` will generate the three dagman files (one for each flavor), which can then be submitted by doing `condor_submit_dag dagman_step1_e.dag`.

The main parameters, which sit near the top of the dag maker, is `step0dir` and `step1dir`.

### step 2
Step 2 is the process where we run NuRadioMC on the list of energy depositions created in step 1.

To make the output directory structure for a corresponding geometry, configuration, and simulation specification, run `python make_step2_outdirs.py`

To make the dagman files, do `python make_step2_dag.py`. The major variables to be changed here (as well as in the output directory maker above) is `step1dir`, `step2dir`, `det_file` (the detector json file), `config_file` (the config yaml file), and the `sim_file` (the simulation .py file).

Then you can submit the per flavor simulations by doing `condor_submit_dag dagman_step2_e.dag`.

### step3
After all of step 2 is complete, there is a step which will merge all of the step 2 files in a single zenith bin into a "total" file. The naming convention is `filename.part.XXXXXX.hdf5.tar.gz`.

Do `python make_step3_dag.py` to make dag file which can then be submitted by `condor_submit_dag dagman_step3.py`. Note that this step (and this step only!) is designed to be run on the **submit** machine, not **sub-1** at WIPAC. That is, you want to do this with access to the local filesystem, not on the grid.

## Logistical Details
### Setting up the software
These jobs are designed to run on "the grid." They therefore need software that is installed in cvmfs. This is currently being handled by code distributed in [user cvmfs for IceCube](https://wiki.icecube.wisc.edu/index.php/User_CVMFS).

Brian is using a conda environment to handle python and proposal. GSL, NuRadioMC, NuRadioReco, and radiotools are installed in cvmfs itself.

To install the software on cvmfs, you will first need to get into a singularity container, which you can do with the following command (or equivalent):
`singularity exec -B /tmp:/tmp -B /cvmfs:/cvmfs -B /net/cvmfs_users/brianclark:/cvmfs/icecube.opensciencegrid.org/users/brianclark -B /data/sim/:/data/sim /cvmfs/singularity.opensciencegrid.org/opensciencegrid/osgvo-el7:latest bash`


### Submitting jobs
Before submitting jobs, it is important to make sure your grid proxy certificates are good

```
grid-proxy-init -hours 72
export X509_USER_PROXY=/tmp/x509up_u$UID
```

### git maintenance
if you are keeping the repo on sub-1, which has an oudated version of git, you will also need to do:

`git remote set-url origin https://clark2668@github.com/clark2668/grid_scripts.git`

or else pushing won't work
