# Craft.AI Deployment Example

This repository provides an example of how to deploy a Python function to the [Craft.AI MLOps platform](https://mlops-platform.craft.ai/).

## 📁 Project Structure

- `src/`: Contains the Python function to deploy.
- `push_and_deploy_my_function.py`: Script used to deploy the function as a pipeline and endpoint.
- `.env_template`: Template for the environment configuration file.
- `.requirements.txt`: Contains Python libraries to be included to run Python function.

## 🔧 Setup Instructions
0. **Preparation**:
   - Install CraftAI sdk with for exemple : 
     ```bash
     pip install craft-ai-sdk
     ```


1. **Prepare environment variables**:
   - Rename `.env_template` to `.env`.
   - Edit `.env` and fill in the following variables:
     ```env
     CRAFT_AI_SDK_TOKEN="your_sdk_token_here"
     CRAFT_AI_ENVIRONMENT_URL="your_environment_url_here"
     ```

2. **Deploy your function**:
   - Run the deployment script:
     ```bash
     python3 push_and_deploy_my_function.py
     ```

## 🚀 What Happens Next?

The script will:
- Delete any previous version of the pipeline (if it exists).
- Create a new pipeline with your function.
- Run a test execution of the pipeline.
- Deploy the pipeline as a low-latency endpoint.
