# Databricks notebook source
# Databricks notebook source
import os
import mimetypes
import time
import json
import mlflow
from mlflow.types.schema import Schema
from mlflow.models import infer_signature
from mlflow.tracking import MlflowClient
from typing import List
import sys
import subprocess

# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'https://s3.amazonaws.com/artifacts.h2o.ai/releases/ai/h2o/mlops/rel-0.60.1/3/h2o_mlops_client-0.60.1-py2.py3-none-any.whl'])
import h2o_mlops_client
import h2o_mlops_client as mlops
