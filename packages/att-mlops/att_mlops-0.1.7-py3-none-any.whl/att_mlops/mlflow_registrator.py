import os
import mimetypes
import time
import json
import mlflow
from mlflow.types.schema import Schema
from mlflow.models import infer_signature
from mlflow.tracking import MlflowClient
# AI DOC

class AI_Document:
    def __init__(self, name=None, description=None, creator_user=None, type_of_model_fit=None, business_unit_owner=None, location=None, key_model_parameters=None, set_experiment_path=None):
        self.name = name
        self.description = description
        self.creator_user = creator_user
        self.type_of_model_fit = type_of_model_fit
        self.business_unit_owner = business_unit_owner
        self.location = location
        self.key_model_parameters = key_model_parameters
        self.set_experiment_path = set_experiment_path
        self.DocAIJSONS ="""
            {
                "usecase": {
                    "name": "",
                    "description": "NA",
                    "creator_user": "NA",
                    "business_unit_owner": "NA",
                    "creation_date": "NA"
                },
                "training_data": {
                    "location": "NA"
                },
                "model": {
                    "owner": "NA",
                    "type_of_model_fit": "NA",
                    "model_library_used": "NA",
                    "artifacts_location": "not applicable",
                    "deployment_date": "not applicable",
                    "last_modified": "NA",
                    "key_model_parameters": "Depth=3, Num Trees = 1000"
                },
                "is_sift_compliance": "N",
                "bias_evaluation_doc_location": "N",
                "privacy_review_doc_number": "N"
            }
            """
    def json_doc(self):
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

        if self.type_of_model_fit is not None:
            DocAIJSON["model"]["type_of_model_fit"] = self.type_of_model_fit
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

        return DocAIJSON

# registrator

class ModelRegistrator:
    """
    A class to register model in mlflow Registry. experiment_name, set_experiment_path, model, model_name, framework, X_train, y_train, target, model_metrics are the mandatory parameters.

    Attributes:
    - experiment_name (str) : Name of experiment.
    - set_experiment_path (str) : Databricks Workspace path where experiment create. ex. /Users/<userid>@att.com/mlflow_exp/
    - model (str) : the object of model
    - model_name (str) : Name of model user want to keep
    - framework (str) : model build framework. ex. sklearn, pytorch, H2o_dai
    - X_train (dataframe): X train dataset used for buid the model
    - y_train (dataframe): y train dataset used for buid the model
    - target (str) : Provide target column name
    - model_metrics list(Key, value) : metrics user want to log [('score', 0.25)]
    - name (str, optional): usecase of model
    - description (str, optional): model use case discription 
    - creator_user (str, optional): id of user who created model 
    - business_unit_owner (str, optional): name of business unit under this model is build 
    - location (str, optional): location of dataset which used to build the model  
    - key_model_parameters (str, optional): main key perameters of model ex. perameters used in model 
    """
    def __init__(self, experiment_name=None, set_experiment_path=None, model=None, model_name=None, framework=None, X_train=None, y_train=None, target=None, model_metrics=[], name=None, description=None, creator_user=None, business_unit_owner=None, location=None, key_model_parameters=None):
      # mlflow registarator mendatory fields
      self.experiment_name = experiment_name      
      self.set_experiment_path = set_experiment_path
      self.model = model
      self.model_name = model_name
      self.framework = framework
      self.X_train = X_train
      self.y_train = y_train
      self.target = target
      self.model_metrics = model_metrics
      # Document Ai file optional fields for user
      self.name = name
      self.description = description
      self.creator_user = creator_user
      self.type_of_model_fit = framework
      self.business_unit_owner = business_unit_owner
      self.location = location
      self.key_model_parameters = key_model_parameters
      
      if self.experiment_name != None:
        self.experiment_name = experiment_name
      else:
        raise ValueError("provide experiment name")
      
      if self.set_experiment_path != None:
        self.set_experiment_path = set_experiment_path
      else:
        raise ValueError("provide workspace path for setting up experiment")
        
      if self.model != None:
        self.model = model
      else:
        raise ValueError("provide your model")
    
      if self.model_name != None:
        self.model_name = model_name
      else:
        raise ValueError("provide model name")
        
      if self.framework != None:
        self.framework = framework
      else:
        raise ValueError("provide your model framework (Ex. sklearn or pytorch)")
        
      if type(self.X_train) == type(None):
        raise ValueError("provide X_train data used in model")
      
      if type(self.y_train) == type(None):
        raise ValueError("provide y_train data used in model")

      if self.target != None:
        self.target = target
      else:
        raise ValueError("provide target column name")
      
      if(self.name == None):
        self.name = self.model_name
        
      mlflow.set_experiment(self.set_experiment_path+"/"+experiment_name+"/")

    def get_metrics(model_metrics):
      if len(model_metrics) > 0:
        for key, value in model_metrics:
            metric_nm, metric_val = key, value
            mlflow.log_metric(metric_nm, metric_val)
      else:
        pass
    
    def register_model(self):
      ai_document_json = AI_Document(name=self.name, description=self.description, creator_user=self.creator_user, type_of_model_fit=self.type_of_model_fit, business_unit_owner=self.business_unit_owner, location=self.location, key_model_parameters=self.key_model_parameters, set_experiment_path=self.set_experiment_path).json_doc()
      
      ModelRegistrator.get_metrics(self.model_metrics)      
      mlflow.log_dict(ai_document_json, "ai_model_document.json")
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
