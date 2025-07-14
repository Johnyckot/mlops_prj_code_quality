# Software Code Defects Prediction

## Table of Contents
1. [Problem Description](#1-problem-description)
2. [Data Analysis](#2-data-analysis)
3. [Exploratory Data Analysis Results](#3-exploratory-data-analysis-results)
4. [Models Training and Evaluation](#4-models-training-and-evaluation)
5. [Source Code](#5-source-code)
6. [Dependency Management](#6-dependency-management)
7. [Containerization](#7-containerization)
8. [Test Run](#8-test-run)

## 1. Problem Description
Project is aiming to predict a probabilty of a software code to have a defect. For ML model training it uses one of the NASA Metrics Data Program defect data sets. Data from software for storage management for receiving and processing ground data. Data comes from McCabe and Halstead features extractors of source code. These features were defined in the 70s in an attempt to objectively characterize code features that are associated with software quality.

**Project Goal**: 
Project goal is to create a MLOPS pipeline which:
 - Ingest dataset from publicly availalbe URLs;
 - Trains the ML model which predicts software defects;
 - Validates model;
 - Deploys model; 
 
**Additional requirements**: 
 - Model should be accessible as a Web-Service for downstream consumers.
 - Model should be accessible as a Spark-UDF for downstream batch-loads;


The dataset used in this project is publicly available at [OpenML Dataset](https://www.openml.org/search?type=data&sort=runs&status=active&id=1067).

### Dataset Fields

Dataset contains of following features:

- `loc`: numeric - McCabe's line count of code
- `v(g)`: numeric - McCabe "cyclomatic complexity"
- `ev(g)`: numeric - McCabe "essential complexity"
- `iv(g)`: numeric - McCabe "design complexity"
- `n`: numeric - Halstead total operators + operands
- `v`: numeric - Halstead "volume"
- `l`: numeric - Halstead "program length"
- `d`: numeric - Halstead "difficulty"
- `i`: numeric - Halstead "intelligence"
- `e`: numeric - Halstead "effort"
- `b`: numeric - Halstead
- `t`: numeric - Halstead's time estimator
- `lOCode`: numeric - Halstead's line count
- `lOComment`: numeric - Halstead's count of lines of comments
- `lOBlank`: numeric - Halstead's count of blank lines
- `lOCodeAndComment`: numeric
- `uniq_Op`: numeric - unique operators
- `uniq_Opnd`: numeric - unique operands
- `total_Op`: numeric - total operators
- `total_Opnd`: numeric - total operands
- `branchCount`: numeric - count of the flow graph
- `problems`: {false, true} - module has/has not one or more reported defects

### Project technical description

 Project is implemented on Dataricks. Which is a cloud-based platform, containing:
  - Data processing (via Spark);
  - Pipeline orchestration (Databricks workflows);
  - ML Experiment tracking (Via managed version of MLFolw);
  - Model registry (via Databricks Unity Catalog)
  - Model Deployment (via Databricks Model Serving Endpoints)
  - IaC (via Databrciks Asset Bundles)

## 2. Project structure and reproducibility

**Prerequisites**
 - Access to a Databricks workspace with enabled Unity Catalog (free version could be used https://www.databricks.com/learn/free-edition)
 - VSCode with installed Databricks extension. (Hence project deployment is done via Databricks-CLI, VsCode extension is recommendet for simplicity)

**Project structure and implementation logic**
 - databricks.yml - contains project metadata, including connection details to Databricks workspaces;
 - resources\mlops_project.job.yml - contains description of all resources within a bundle. Including worklow, jobs and dependencies. 
 - src\ - contains logic for each step of the workflow;
   - src\0_setup.ipynb - deploys objects into the Unity Catalog(catalog, schema, volumes). Idempotent.
   - src\1_ingest_data.ipynb - loads data from https://www.openml.org/ into a DeltaLake table within a unity catalog. 
   - src\2_train_model.ipynb - creates a MLFlow experiment and trains the model with different tunning parameters. 
   - src\3_model_registration.ipynb - select the model with the best metrics from previous step and registers it as a candidate;
   - src\4_model_validation.ipynb - validates candidate model and register it as Production version
   - src\5_model_usage.ipynb - example of using a Production model as a Spark UDF for predictions on a Spark Dataframe (simulates a batch load)
- tests\test_web_model.py - test script for Model Web Service.

## 3. Databricks Cloud deployment and reproducability

In order to deploy the project to the Databricks cloud platform you need an access to a Databricks worspace (see prerequisites). 
Deployment steps:
 - Clone the repo;
 - Initialize Databricks Bundle project using VScode extenson. (Alternatively use Databricks-CLI)
 - Deploy the Bundle project to the Databricks worksace using extension or CLI.  
   ![deployment](images\deployment_extension.png)

## 4. Workflow orchestration
   The workflow orchestration job is described in resources\mlops_project.job.yml. Once it is deployed on a worskace as a part of a bundle, it is available in Databricks UI. In scope of this project, the pipeline is configured to run daily. It also could be triggered  manually via UI or via databricks-cli.
   ![orchestation UI](images\orchestration.png)

## 5. Experiment tracking and model registry
  During the 2_train_model step of the workflow the model is trained within a MLFlow experiment. The RandomForestClassifier is selected as the base model. 
  Each iteration of experiment training a model with a specific thet of tuning parameters( defined with hyperopt scope).
  Results of experiments could be tracked in a Databricks UI ('experiments' tab)
   ![Experiment tracking](images\experiment_tracking.png)

  The 3_model_registration step of the workflow selects the best model from previous step (model with the best Accuracy metric) and then registers it in the Unity Catalog model registry as a 'candidate'. 
  Then  the 4_model_validation step performs some validations of the candidate model (if it is correctly tagget, if the accurac is better then current Production model) and registers it as a 'Production' model. Results could be viewed in Databricks UI ('Models' tab)

  ![Model registration](images\model_registration.png)

## 6. Deployment

  According to the requirements the Production model shold be deployed in 2 ways: 
   - as a Spark-UDF for downstream batch-loads;
   - as a Web-Service for downstream consumers.

   The 5_model_usage.ipynb contains the code which deploys the model as a Spark-UDF on a Databricks Spark cluster. Then the model is used in a spark job to make predictions on a Spark DataFrame. 
   ![Spark UDF deployment](images\spark_udf_deployment.png)
   
   For deployment of the Production model as a web-service, Dtabricks model-serving endpoint was used:  
   ![Web deployment](images\web_deployment.png)  
   The funtionality could be tested by a test-script tests\test_web_model.py (running locally)  
   ![Web deployment test](images\web_deployment_test.png)   

   
  