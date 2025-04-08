"""
This script is used to deploy a Python function to the Craft.AI MLOps platform. It performs the following steps:
1. Loads environment variables from a .env file (token and environment URL).
2. Initializes the Craft.AI SDK.
3. Deletes any existing pipeline and deployments with the same name to avoid conflicts.
4. Defines the input and output parameters for the pipeline.
5. Creates a new pipeline from the specified local Python function.
6. Deploys this pipeline as an HTTP endpoint with low-latency mode.

Each line is documented for clarity on its purpose.
"""

##############################
### DEPENDENCIES MANAGEMENT ##
##############################
import os  # Provides functions to interact with the operating system
from craft_ai_sdk import CraftAiSdk  # Main class for interacting with the Craft.AI platform
from craft_ai_sdk.exceptions import SdkException  # Exception class for handling SDK-related errors
from craft_ai_sdk.io import Input, Output, InputSource, OutputDestination  # Classes to define I/O for pipelines
from dotenv import load_dotenv  # Allows loading environment variables from a .env file

### ENVIRONMENT VAR LOADING ###
load_dotenv()  # Loads environment variables from the .env file

### INITIALISE SDK ###
sdk = CraftAiSdk()  # Initializes the SDK using environment variables (CRAFT_AI_SDK_TOKEN and CRAFT_AI_ENVIRONMENT_URL from .env file)

################################
### OLD PIPELINE DESTRUCTION ###
################################
pipeline_name = "myfunction-pipeline"  # Name of the pipeline to manage (delete/create)

################################
### OLD PIPELINE DESTRUCTION ###
################################
print("Looking for old pipeline and deploiement.")

try:
    sdk.delete_pipeline(pipeline_name, force_deployments_deletion=True)  # Deletes pipeline and any associated deployments if they exist
    print("Old pipeline and deploiement found and deleted !")
except Exception as e:
    print(f"Ignored deletion: {e}")  # Logs any exception raised during deletion and continues

#########################
### PIPELINE CREATION ###
#########################

print("Pipeline creation begins.")

# Function's input
predict_input = Input(
    name="text",  # Name of the input parameter of the function
    data_type="string",  # Type of the input (must match function expectations)
    description="This is the pipeline input",  # Description for documentation
)

# Function's output
predict_output = Output(
    name="result",  # Name of the key in the dictionary returned by the function
    data_type="string",  # Type of the output (must match returned value type)
    description="This is the pipeline output",  # Description for documentation
)

# Pipeline definition
sdk.create_pipeline(
    pipeline_name=pipeline_name,  # Name of the pipeline
    function_name="my_function",  # Name of the function inside the Python file to execute
    function_path="src/my_function.py",  # Path to the Python file containing the function
    container_config={
        "local_folder": os.getcwd() ,  # Path to the folder to use as context
        "requirements_path": "requirements.txt",  # Path to the file listing Python dependencies
        "included_folders": ["/"],  # Folders/files to include in the deployment package
    },
    inputs=[predict_input],  # List of inputs expected by the function (refers to Input and Output objects defined above create_pipeline)
    outputs=[predict_output],  # List of outputs returned by the function
)

print("Pipeline successfully created !")

###################################
######## PIPELINE TEST RUN ########
###################################
print("Pipeline test begins !")

test_result = sdk.run_pipeline(pipeline_name, inputs = {"text":"This is a test run."}) # This is how you trigger a pipeline with the sdk
function_result = test_result["outputs"]["result"] # Function result is stored in a JSON in a field called "outputs", which contains a dict with all function results
print(function_result)

#####################################
######## DEPLOYMENT CREATION ########
#####################################
print("Deployment creation begins.")

sdk.create_deployment(
    pipeline_name=pipeline_name,  # Name of the pipeline to deploy
    deployment_name=pipeline_name+"-api",  # Name of the deployment (based on pipeline name)
    execution_rule="endpoint",  # The deployment will be accessible via HTTP endpoint (POST). The other way to deploy is a periodic deployment.
    mode="low_latency",  # Uses a low-latency mode for fast execution (pod is persistent). The other deployement mode is "elastic" (pod is created for the execution then destroyed)
)

print("Deployment successfully created !")
