# Interpolation of specfem models in ADIOS format

Hi! You know that your `SPECFEM3D_GLOBE` ADIOS model `model_gll.bp`
is not at the right resolution, and it has the wrong
number of MPI slices? Then this set of instructions is 
for you!

In the following, I will talk about two parameter sets, each of 
which is a combination of 

* NEX_XI/ETA (e.g. 128)
* NPROC_XI_ETA (e.g. 2), and
* CHUNKS (e.g. 6)

1. Parameter set A, the set of parameters of your 
   original ADIOS model is in.
2. Parameter set B, the parameters of you goal ADIOS model

While you don't necesarily need two different compiled versions of 
`SPECFEM`, it is very convenient. In the following however, I will
assume that you only have one version.

## 1. Compile and mesh model using parameter set A 

The first step is to compile and mesh the model using the original
parameter set A.

After meshing is done, save the `solver_data.bp` that was saved in 
`DATABASES_MPI`, in a "safe" directory outside of the `SPECFEM` directory. 
To be on the safe side, you can also save the `model_gll.bp` into a new
directory, but it is not necessary.

**NOTE:**

    If you have the resources to do so, it makes sense to run 
    the solver with one station to create a reference trace set.

## 2. Compile and mesh model using parameter set B

Now that we have are old model and `solver_data.bp`, we can focus on
the new model. Compile specfem and run the mesher using the same model
as in step one, but with parameter set B.

Again, when the job is done, save the `solver_data.bp` that was saved
saved in `DATABASES_MPI` in a "safe" directory outside of the 
`SPECFEM` directory. Make sure, that this is a different directory than
the previous `solver_data.bp` file.

## 3. Interpolate

Now, we have the old model, the old mesh, and the new mesh.
The only thing that is left is interpolating the points from the old mesh
and model using the new mesh, onto a new model (yes, this step is crucial!).

For this purpose, a convenience function exists deep in the specfem 
directory: 
```bash
... specfem3d_globe/src/tomography/postprocess_sensitivity_kernels/interpolate_model.F90
```

The compiled version of this function is located here:
```bash
... specfem3d_globe/bin/xinterpolate_model_adios
```

It is called in the following manner from within the specfem directory
of (to be clear the specfem that is compiled with the new parameter set B):
```bash
./bin/xinterpolate_model_adios OLD_TOPO_DIR OLD_MODEL_DIR NEW_TOPO_DIR NEW_MODEL_DIR (midpoint_search)
```

There are a total of 5 arguments, let's clarify:

* OLD_TOPO_DIR: The directory containing the mesh `solver_data.bp` meshed with 
                parameter set A
* OLD_MODEL_DIR: The directory containing the old model with the wrong MPI
                 slices and resolution.
* NEW_TOPO_DIR: The directory containing the new mesh `solver_data.bp`
* NEW_MODEL_DIR: An empty directory to save the new interpolated model in.
* midpoint_search: an integer defining which points to use for the interpolation:
  * mid-point-search == 1: looking for mid-points only is a good approach when 
                           changing number of processes (NPROC) only,
                           while keeping the mesh resolution (NEX) the same
                           (by default set to .true.)
  * mid-point-search == 0: searching for each single GLL point is a good
                           approach when changing resolution (NEX) of meshes;
                           in general, interpolation suffers and might lead
                           to differences at internal interfaces (e.g. 410)

The interpolation has to be run using the same parameters and MPI slices
as wished for (meaning, parameter set B).

After running the interpolation. Replace the old `model_gll.bp` in the 
`DATA/GLL` directory with the new interpolated model, naming it the same 
as the old model. Then run the mesher and the solver to test the results.

That's it!


#### Some notes

Sometimes, especially when using 6 chunks and 6 MPI slices, the mesher
can take a while. For some reference values from Traverse:

* Meshing using [NPROC=8, CHUNKS=6, NEX=256] took ~5 minutes
* Meshing using [NPROC=1, CHUNKS=6, NEX=128] took ~55 minutes

Significantly different numbers!
