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

# Databricks notebook source
class mlopsConnect:
  # initializer / instance attributes
  def __init__(self, REFRESH_TOKEN, 
              API_CLIENT_ID="hac-platform-public",
              TOKEN_ENDPOINT_URL=(
                                  "https://auth.h2o.web.att.com/auth/realms/h2oaic/protocol/openid-connect/token"
                                ),
              H2O_CLOUD_URL= "h2o.web.att.com"):
      self.REFRESH_TOKEN = REFRESH_TOKEN
      self.API_CLIENT_ID = API_CLIENT_ID
      self.TOKEN_ENDPOINT_URL=TOKEN_ENDPOINT_URL
      self.H2O_CLOUD_URL=H2O_CLOUD_URL
  def showAttribute(self):
    print(

      f'REFRESH_TOKEN :{self.REFRESH_TOKEN }',
      f'API_CLIENT_ID :{self.API_CLIENT_ID}',
      f'TOKEN_ENDPOINT_URL : {self.TOKEN_ENDPOINT_URL}',
      f'H2O_CLOUD_URL : {self.H2O_CLOUD_URL}'

    )
  def token_provider(self):
        return mlops.TokenProvider(
          refresh_token=self.REFRESH_TOKEN,
          client_id=self.API_CLIENT_ID,
          token_endpoint_url=self.TOKEN_ENDPOINT_URL,
      )
  def connect(self):
      """
      Connect to MLOps
      """
      try:
        MLOPS_API = "https://mlops-api." + self.H2O_CLOUD_URL
        client = h2o_mlops_client.Client(
            gateway_url=MLOPS_API, token_provider=self.token_provider()
        )
        print("Successfully connected MLOPS client.")
        return client
      except Exception as e: print(e)
  def discription():
    print(
      '''
      '''
    )

