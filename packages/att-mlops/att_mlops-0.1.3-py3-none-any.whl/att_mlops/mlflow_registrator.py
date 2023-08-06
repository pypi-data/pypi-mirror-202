import os
import mimetypes
import time
import json
import mlflow
from mlflow.types.schema import Schema
from mlflow.models import infer_signature
from mlflow.tracking import MlflowClient
from typing import List
import h2o_mlops_client
import h2o_mlops_client as mlops

class ModelRegistrator:
    
    def __init__(self, experiment_name, model, model_name, framework, X_train, y_train, target, model_metrics=[], name=None, description=None, creator_user=None,
    business_unit_owner=None, location=None, key_model_parameters=None, set_experiment_path=None):
      self.experiment_name = experiment_name
      self.model = model
      self.model_name = model_name
      self.framework = framework
      self.X_train = X_train
      self.y_train = y_train
      self.target = target
      self.model_metrics = model_metrics
      self.name = name
      self.description = description
      self.creator_user = creator_user
      self.business_unit_owner = business_unit_owner
      self.location = location
      self.key_model_parameters = key_model_parameters
      self.set_experiment_path = set_experiment_path
        
      mlflow.set_experiment(self.set_experiment_path+experiment_name+"/")

      # DOC AI
      self.DocAIJSONS = """
      {
          "usecase": {
              "name": "Wine Quality Predication",
              "description": "The Quality of red wine can be predict with using this model.",
              "creator_user": "dt1634@att.com",
              "business_unit_owner": "CDO-AIaaS",
              "creation_date": "02/17/2022"
          },
          "training_data": {
              "location": "https://www.kaggle.com/datasets/yasserh/wine-quality-dataset"
          },
          "model": {
              "owner": "DT1634@att.com",
              "type_of_model_fit": "sklearn",
              "model_library_used": "Sklearn",
              "artifacts_location": "not applicable",
              "deployment_date": "not applicable",
              "last_modified": "02/17/2023",
              "key_model_parameters": "Depth=3, Num Trees = 1000"
          },
          "is_sift_compliance": "N",
          "bias_evaluation_doc_location": "not applicable",
          "privacy_review_doc_number": "N"
      }
      """
    
    def get_metrics(model_metrics):
      if len(model_metrics) > 0:
        for key, value in model_metrics:
            metric_nm, metric_val = key, value
            mlflow.log_metric(metric_nm, metric_val)
      else:
        pass
    
    def register_model(self):
      import json
      from datetime import date
      DocAIJSON = json.loads(self.DocAIJSONS)
      
      if self.name is not None:
          DocAIJSON["usecase"]["name"] = self.name
      else:
          pass

      if self.description is not None:
          DocAIJSON["usecase"]["description"] = self.description
      else:
          pass

      if self.creator_user is not None:
          DocAIJSON["usecase"]["creator_user"] = self.creator_user
          DocAIJSON["model"]["owner"] = self.creator_user
      else:
          pass

      if self.business_unit_owner is not None:
          DocAIJSON["usecase"]["business_unit_owner"] = self.business_unit_owner
      else:
          pass

      if self.location is not None:
          DocAIJSON["training_data"]["location"] = self.location
      else:
          pass

      if self.key_model_parameters is not None:
          DocAIJSON["model"]["key_model_parameters"] = self.key_model_parameters
      else:
          pass

      DocAIJSON["usecase"]["creation_date"] = str(date.today())
      DocAIJSON["model"]["last_modified"] = str(date.today())

      ModelRegistrator.get_metrics(self.model_metrics)      
      mlflow.log_dict(DocAIJSON, "ai_model_document.json")
      mlflow.set_tag("category","DocAI")
      
      if self.framework == 'sklearn':
        model_signature = infer_signature(self.X_train, self.y_train)
        model_signature.outputs = mlflow.types.Schema([mlflow.types.ColSpec(name=self.target, type=mlflow.types.DataType.float)])
        model_log_model = mlflow.sklearn.log_model(self.model, self.model_name, signature=model_signature)
      elif self.framework == 'pytorch':
        model_signature = infer_signature(self.X_train, self.y_train)
        model_signature.outputs = mlflow.types.Schema([mlflow.types.ColSpec(name=self.target, type=mlflow.types.DataType.float)])
        model_log_model = mlflow.pytorch.log_model(self.model, self.model_name, signature=model_signature)
      else:
        raise ValueError(f"Framework '{self.framework}' not supported.")
      model_version = mlflow.register_model(model_log_model.model_uri, self.model_name)
      return model_version

