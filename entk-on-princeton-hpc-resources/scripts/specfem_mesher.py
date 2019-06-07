from radical.entk import Pipeline, Stage, Task, AppManager
import traceback, sys, os

# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_REPORT'] = 'True'

# Description of how the RabbitMQ process is accessible
# No need to change/set any variables if you installed RabbitMQ has a system
# process. If you are running RabbitMQ under a docker container or another
# VM, set "RMQ_HOSTNAME" and "RMQ_PORT" in the session where you are running
# this script.
hostname = os.environ.get('RMQ_HOSTNAME', 'localhost')
port = os.environ.get('RMQ_PORT', 5672)


if __name__ == '__main__':

    p = Pipeline()

    # First stage to perform one meshfem task
    meshfem_stage = Stage()

    t1 = Task()

    t1.pre_exec = [     # Modules to be loaded
                        'module purge',
                        'module load intel/18.0',
                        'module load intel-mpi/intel/2018.3',

                        # Create file structure
                        'mkdir -p DATABASES_MPI',
                        'mkdir -p OUTPUT_FILES',

                        # Copy data
                        'cp -r /projects/TROMP/entk/specfem3d_globe/DATA .',

                        # Copy input files to output directory
                        'cp DATA/Par_file OUTPUT_FILES/',
                        'cp DATA/CMTSOLUTION OUTPUT_FILES/',
                        'cp DATA/STATIONS OUTPUT_FILES',

                        # Link binaries
                        'ln -s /projects/TROMP/entk/specfem3d_globe/bin .',

                ]
    t1.executable = ['./bin/xmeshfem3D']
    t1.cpu_reqs = {'processes': 4, 'process_type': 'MPI', 'threads_per_process': 1, 'thread_type': 'OpenMP'}

    t1.post_exec = [    # Tar output files
                        'tar -zcf specfem_data.tar.gz bin DATA DATABASES_MPI OUTPUT_FILES',

                        # Copy to scratch folder
                        'cp specfem_data.tar.gz /projects/TROMP/entk/scratch/',

                ]
    t1.download_output_data = ['STDOUT', 'STDERR', 'specfem_data.tar.gz']

    meshfem_stage.add_tasks(t1)

    p.add_stages(meshfem_stage)

    res_dict = {
                'resource': 'princeton.tiger_cpu',
                'project' : 'geo',
                'queue'   : 'cpu',
                'schema'   : 'local',
                'walltime': 10,
                'cpus': 4,
    }
    

    try:

        # Create an Application Manager for our application
        appman = AppManager(hostname=hostname, port=port, resubmit_failed=False)

        # Assign resource request description to the Application Manager
        appman.resource_desc = res_dict

        # Assign the workflow to be executed by the Application Manager
        appman.workflow = set([p])

        # Run the application manager -- blocking call
        appman.run()        

    except Exception, ex:

        print 'Execution failed, error: %s'%ex
        print traceback.format_exc()

    
