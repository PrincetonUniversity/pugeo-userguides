#!/bin/bash

#SBATCH --nodes 1
#SBATCH --ntasks 24
#SBATCH --time 00:30:00

# load modules
module load intel/18.0
module load openmpi/intel-18.0

# change directory to build
cd /scratch/gpfs/<your_puid>/specfem3d_globe

srun ./bin/xmeshfem3D
