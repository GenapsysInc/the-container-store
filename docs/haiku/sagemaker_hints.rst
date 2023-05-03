==========================================
AWS Sagemaker Guildelines / Hints (Future)
==========================================
The steps outlined below are intended to help bootstrap Jupyter Notebooks onto 
`AWS Sagemaker <https://aws.amazon.com/pm/sagemaker/>`_ (AWSs ML platform)
and is specifically for Haiku.  The steps are general enough to translate to 
running the notebook in other environments as well, e.g., running a Jupyter notebook 
in VS Code may require the VS Code Python Kernel to be updated, etc.  Many of the steps are simliar 
for other notebooks that may require porting to Sagemaker as well.

The advantages of AWS Sagemaker Jupyter Notebooks (vs onsite VMs) are that the underlying instances 
may be scaled to any of the native AWS ML instance types to help accomodate the workload required 
by the notebook.  The true power / advantages of Sagemaker may come into play when/if 
the other Sagemaker platform features are utilized in conjunction with the Notebook.


TBDs:
-----
- How to allow a user access to just the instance and not the entire Sagemaker console or other parts of AWS via IAM
- Automating the steps below, perhaps using the Sagemaker Lifecycle capability
- Automatic Shutdown of instances to save cost
- Integration with other Sagemaker platform capabilities / pipelines


Step 0:  Prerequisites
----------------------
AWS Cloud Administrators of the Notebooks should ensure the following are in place/discussed before embarking on notebook creation:

-  AWS Console permission to SageMaker to create Notebooks
-  Discuss the data analysis size/set in order to provision the underlying local storage appropriately (below)
-  Discuss the data analysis workload size in order to pick an appropriate ML instance
-  Ensure Notebook user(s) have permission to access the S3 buckets where data is stored


Step 1:  Create a new Sagemaker Instance (Cloud Administrator)
--------------------------------------------------------------
This step uses Sagemaker to provision a new compute (EC2) instance 
in AWS that is specifically tailored for Machine Learning and running 
Jupyter notebooks.


- Open the AWS Console
- Navigate to SageMaker
- Select ``Notebooks`` from the left hand menu
- ``Create Notebook Instance``
- Provide a name and instance type.  Start small and change the instance type later if required
- The default disk is only 5GB.  If data is larger and to be kept local, increase this appropriately
- Select Platform Identifier for ``Amazon Linux 2, Jupyter Lab 3``
- Let users have Root access to the notebook to help overcome memory issues (see below)
- Leave VPC at defaults (@FUTURE:  use existing VPC and subnets close to user)
- Enable direct internet access
- Do not add a git repo - this will be done below
- Tag the instance appropriately
- ``Create Instance``
- After ``Create Instance`` is complete and provisioned you can then select ``Open Jupyter Lab`` to access the notebook.



Step 2: GIT Clone the Haiku repository
--------------------------------------
You can ``git clone`` the Haiku repository using Jupyter itself. 


For this step, you will need your github username/password (GIT personal access token).  
If using Jupyter to do the cloning (*recommended*) it will automatically place the code 
in the ``/home/ec2-user/SageMaker/Haiku`` directory.


Step 3: Update the environment/python version (if necessary)
------------------------------------------------------------
Some notebooks may require an updated version of Python within Jupyter. 

For example, the McNaught notebook required version of Python is v3.9 
(due to requirement of ``numpy==1.22``).  However at this time, AWS Sagemaker comes 
at most with v3.8 for the Jupyter Kernel.  

Therefore, you have to upgrade the python version and make it 
available as a kernel to the Jupyter notebook 
(`Upgrading Jupyter Notebook Python Version in Sagemaker <https://awstip.com/how-to-use-a-newer-python-version-in-aws-sagemaker-notebook-1682a89625ef>`_)

    .. code-block:: console

        $ conda create -n  my_custom_python_39 python=3.9
        $ source activate my_custom_python_39
        $ pip install virtualenv
        $ virtualenv my_custom_python_39_venv
        $ conda deactivate
        $ source my_custom_python_39_venv/bin/activate
        $ pip install ipykernel
        $ python -m ipykernel install --user --name=my_custom_python_39


Now, pick the kernel from the notebook which should be visible.

Note that if the Sagemaker instance is restarted some steps will have to be repeated.  
See the referenced article above.
	

Step 4:  Install the required packages
--------------------------------------
``docker/requirements/python_requirements.txt`` lists the packages that are required for the Dockerfile.  
For the Jupyter notebook, access the Terminal and do ``pip install`` or run the 
requirement file manually.

Example for Haiku (assuming Haiku was git cloned into the SageMaker directory):

    .. code-block:: console

	    $ pip install -r /home/ec2-user/SageMaker/Haiku/docker/requirements/python_requirements.txt



Step 5:  Ensure the Haiku util package is imported
--------------------------------------------------
The ``merge_hp`` code needs to be available to use. From the Terminal:

    .. code-block:: console

        $ cd /home/ec2-user/SageMaker/Haiku
        $ python -m pip install -e .


Restart the kernel from Jupyter.


Step 6:  Reading Data files
---------------------------
There are two options for reading the data required for the Notebook:

1. Copying the files to the underlying EC2 Instance that is running the notebook 

2. Adapting the code to access S3 files directly.



Option 1:  Download Datafiles via the terminal 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Assuming the data is already in an accessible S3 Bucket.  
This option offers the **BEST PERFORMANCE WITH THE LEAST CODE CHANGES**
at the cost of having duplicated data.

- Open a Terminal from the Jupyter notebook
- Copy Data to the EC2 Instance:

    .. code-block:: console

        $ cd ~/Sagemaker
        $ mkdir data
        $ aws configure
        $ aws s3 cp --recursive "s3://jk-notebook-data/B000149_RUN_2022_09_29_13_48_10" ./B000149_RUN_2022_09_29_13_48_10


- Change DATA_PATH in the notepbook to ``/home/ec2-user/SageMaker/data/B000149_RUN_2022_09_29_13_48_10``
			
- When running the notebook you might get a MEMORY error, in which case, in the Terminal do:

    .. code-block:: console

        $ sudo su -
        $ echo 1 > /proc/sys/vm/overcommit_memory
        $ exit # sudo shell


Option 2:  Adapting Code to use S3
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This option leaves the data in the S3 bucket and attempts to have the 
Notebook code read it directly.  This has the advantage of not duplicating data 
and not having to rely on more expensive EBS storage in the Sagemaker instance
that might be required for multiple/large datasets.


**WARNING:  DID NOT GET THIS TO WORK - h5py does not appear to be natively 
built with ros3 driver and had trouble building it from source**

After copying the data to an accessible (permissioned) S3 bucket the code needs to be adapated to read / stream it directly

NOTE:  An alternative S3 driver not demonstrated is ``s3fs``.  
This was tried but presented its own set of problems...

- Install boto3 directly using pip (or adjust python_requirements.txt):

    .. code-block:: console

        $ pip install boto3
        $ # OR ... If adjusting python_requirements.txt to include boto3
        $ pip install -r /home/ec2-user/SageMaker/Haiku/docker/requirements/python_requirements.txt


- Adapt the code/folder headers:
  
    .. code-block:: python

        subfolder = 'B000149_RUN_2022_09_29_13_48_10/hp/'
        DATA_PATH = '/path/to/data/'+subfolder
        bucket    = 'correctly-permissioned-bucket'
        useS3     = True
	

- Add new method to get H5Files:
  
    .. code-block:: python

        # Added to import S3 data
        def get_file_list_s3(bucket, subfolder):
            file_list = []
            client    = boto3.client('s3')
            paginator = client.get_paginator('list_objects')
            operation_parameters = {'Bucket': bucket,
                                    'Prefix': subfolder}    
            page_iterator = paginator.paginate(**operation_parameters)
            for page in page_iterator:
                for obj in page['Contents']:
                    file_list.append("s3://"+bucket+"/"+obj["Key"])
                
            # @TODO:  Extract to common method for reuse in here and get_file_list
            file_list_h5 = []
            rex = re.compile('.+output_file_.+\.h5')
            for i in range(len(file_list)):
                if len(rex.findall(file_list[i])) != 0:
                    file_list_h5.append(''.join(rex.findall(file_list[i])))
            sort_nicely(file_list_h5)
            print(file_list_h5)
            return file_list_h5
	

- Use the new method defined above where appropriate:

    .. code-block:: python

        # Adapt to use S3 as data source
        # TBD:  Use more pythonic way to do this verses using a boolean switch
        if (useS3 == True):
            file_list = get_file_list_s3(bucket, subfolder)
        else:
            file_list = get_file_list(directory)
		  

- Adapt h5py to use S3 ros3 (ReadOnly S3) driver:


    .. code-block:: python
    
        f = h5py.File(file_path, 'r', driver=('ros3' if (useS3==True) else None))
	



Step 7:  Writing Outputs
------------------------
Outputs can be written to the local EC2 instances disk and copied to S3 or perhaps streamed directly to S3.

    **TBD - not tried/tested**



Step 8:  Check in modified files to GIT
---------------------------------------
Use ``git push`` from the Jupyter Notebook 

    **TBD - not tried/tested**
