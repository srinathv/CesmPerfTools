#! /bin/bash

/chos/global/u1/v/vadlaman/cesm1_3_xeon_phi_branch/scripts/create_newcase -case $1 -compiler intel15 -mpi impi5.0.up1 -compset FC5 -res ne16_ne16 -mach babbage
