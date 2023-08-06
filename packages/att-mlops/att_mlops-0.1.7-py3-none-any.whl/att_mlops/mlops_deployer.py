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
class importModel:
    prj = mlops.StorageProject

    def __init__(self,mlops_client, 
                  project_name,
                  deployment_scale, 
                  mlops_env_name, 
                  replica,
                  MAX_WAIT_TIME ,
                  REFRESH_STATUS_INTERVAL,
                  registered_model_name,
                  registered_model_versions
                  ):
        self.project_name = project_name
        self.runtime_name = "python-scorer_mlflow_38"
        self.deployment_scale = deployment_scale
        self.mlops_env_name = mlops_env_name
        self.replica = replica
        self.client =mlops_client
        # Defines maximum waiting time for the deployment to become healthy.
        self.max_wait_time = 600  # 600
          # Interval time of the status verification
        self.REFRESH_STATUS_INTERVAL = REFRESH_STATUS_INTERVAL
        self.registered_model_name = registered_model_name
        self.registered_model_versions = registered_model_versions
        prj: mlops.StorageProject
        self.project = self.prj
        self.project_id = self.project.id
#         self.mlops_exp
        self.artifact_type_name = "python/mlflow.zip"
        self.processor_name = "unzip_processor"
        self.runtime_version='python-scorer_mlflow_38'
        self.resource_request = '{"cpu": "200m", "memory": "256Mi"}'
#         self.to_deploy = to_deploy

    def _get_project_id(self):
        """Gets the ID of the selected project."""
        # Get MLOps projects
        projects: mlops.StorageListProjectsResponse = self.client.storage.project.list_projects(
            mlops.StorageListProjectsRequest()
        )
        for p in projects.project:
            if p.display_name == self.project_name:
                return p
        else:
            raise LookupError("Requested project not found")
    def _create_project(self):
        return self.client.storage.project.create_project(
            mlops.StorageCreateProjectRequest(
                mlops.StorageProject(display_name=self.project_name)
            )
        ).project

    def _form_list_model_version_request(self):
        return mlops.ModelregistryListRegisteredModelVersionsForModelRequest(
            source_key=self.registered_model_name
        )

    def _form_import_model_version_request(self):

        external_registered_model_versions = [
            mlops.ModelregistryExternalRegisteredModelVersion(
                source_key=self.registered_model_name, version=self.registered_model_versions
            )
            for version in str(self.registered_model_versions)
        ]
        return mlops.ModelregistryImportRegisteredModelVersionRequest(
            external_registered_model_versions=external_registered_model_versions,
            project_id=self.project.id,
        )


    def _form_add_experiments_request(self, versions: List[mlops.ModelregistryExternalRegisteredModelVersion]):
#         versions: List[mlops.ModelregistryExternalRegisteredModelVersion]
#         versions = dict(ChainMap(*versions))
        print("****", type(versions))
        return [
            mlops.ModelregistryAddExperimentRequest(
                model_version_id=version.adapter_model_version_id,
                experiment_name=self.registered_model_name,
            )
            for version in versions
        ]

    def _list_all_versions_for_model(self):
        return self.client.external_registry.external_registered_model_version_service.list_registered_model_versions_for_model(
            _form_list_model_version_request(self.registered_model_name)
        )


    def _import_external_model_into_mlops(self):
        try:
            response = self.client.external_registry.external_registered_model_version_service.import_registered_model(
                self._form_import_model_version_request())
            return response
        except Exception:
            raise


    def _add_experiments_to_mlops(self, versions: mlops.ModelregistryImportRegisteredModelVersionResponse):
        try:
            response = self.client.external_registry.external_registered_model_version_service.batch_add_experiments(
                mlops.ModelregistryAddExperimentsRequest(
                    self._form_add_experiments_request(versions)
                )
            )
            return response
        except Exception:
            raise


    def find_model_to_mlops(self):
        """Import the registered model versions from the external registry"""
        try:
            experiments: mlops.StorageListExperimentsResponse = (
                self.client.storage.experiment.list_experiments(
                    mlops.StorageListExperimentsRequest(
                        project_id=self.project.id,
                        filter=self._get_filter_by(),
                    )
                )
            )
            exp = None
            if experiments.experiment:
                for e in experiments.experiment:
                    e_data: mlops.StorageExperiment = (
                        self.client.storage.experiment.get_experiment(
                            mlops.StorageGetExperimentRequest(
                                id=e.id,
                                response_metadata=mlops.StorageKeySelection(pattern=["%"]),
                            )
                        ).experiment
                    )
                    e_metadata: mlops.StorageMetadata = e_data.metadata
                    name = e_data.display_name
                    version = e_metadata.values["source_model_version"].string_value
                    if name == self.registered_model_name and version == self.registered_model_versions[0]:
                        exp = e
                if exp is None:
                    raise Exception(
                        "MLOps cloud not find experiment {} with the version {}".format(
                            self.registered_model_name, self.registered_model_versions[0]
                        )
                    )
                return exp
        except Exception:
            raise


    def import_model_to_mlops(self):
        """Import the registered model versions from the external registry"""
        try:
            import_response = self._import_external_model_into_mlops()
            imported_versions = import_response.external_registered_model_versions.copy()
            for version in import_response.external_registered_model_versions:
                if version.status == "IMPORTED":
                    print(
                        version.source_key
                        + " "
                        + "Version:"
                        + version.version
                        + "--"
                        + version.status_description
                    )
                    imported_versions.remove(version)
                elif version.status_description:
                    print(
                        version.source_key
                        + " "
                        + "Version:"
                        + version.version
                        + "--"
                        + version.status_description
                    )
                    imported_versions.remove(version)

            if len(imported_versions) > 0:
                add_experiment_response = self._add_experiments_to_mlops(imported_versions)
                print(
                    "Model is successfully imported into MLOps Project name: "
                    + self.project.display_name
                )
            else:
                print("No experiments available to add")

            return self.find_model_to_mlops()
        except Exception:
            raise


    # filter
    def _get_filter_by(self):
        return mlops.StorageFilterRequest(
            query=mlops.StorageQuery(
                clause=[
                    mlops.StorageClause(
                        property_constraint=[
                            mlops.StoragePropertyConstraint(
                                _property=mlops.StorageProperty(field="display_name"),
                                operator=mlops.StorageOperator.EQUAL_TO,
                                value=mlops.StorageValue(string_value=self.registered_model_name),
                            )
                        ]
                    )
                ]
            )
        )


    def _get_sort_by(field, order=mlops.ModelregistryOrder.DESCENDING):
        return mlops.StorageSortingRequest(
            _property=[
                mlops.StorageSortProperty(
                    _property=mlops.StorageProperty(field=field),
                    order=order,
                )
            ]
        )

    # deployment functions
    
    def deployment_should_become_healthy(self, deployment_id: str):
        """Waits for the deployment to become healthy helper function."""
        svc = self.client.deployer.deployment_status
        status: mlops.DeployDeploymentStatus
        deadline = time.monotonic() + self.max_wait_time

        while True:
            status = svc.get_deployment_status(
                mlops.DeployGetDeploymentStatusRequest(deployment_id=deployment_id)
            ).deployment_status
            print("..{}..".format(status.state), end="")
            if (
                status.state == mlops.DeployDeploymentState.HEALTHY
                or time.monotonic() > deadline
            ):
                break
            time.sleep(REFRESH_STATUS_INTERVAL)

        return status
    
    def _find_mlops_environment(self):
      # Fetching available deployment environments.
      deployment_envs: mlops.StorageListDeploymentEnvironmentsResponse = (
          self.client.storage.deployment_environment.list_deployment_environments(
              mlops.StorageListDeploymentEnvironmentsRequest(self.project.id)
          )
      )
      # Looking for the ID of the selected deployment environment.
      for de in deployment_envs.deployment_environment:
          if de.display_name == self.mlops_env_name:
              deployment_env = de
              break
      if deployment_env is None:
          raise LookupError("Requested deployment environment not found")
      else:
          return deployment_env.id
    
    def _dai_mlflow_flavor_mojo_composite(self):
      # Customize the composition of the deployment
      print(self.artifact_type_name, self.processor_name)
      artifact_type_name = self.artifact_type_name
      processor_name = self.processor_name
      composition = mlops.DeployDeploymentComposition(
          experiment_id = mlops_exp.id,
          deployable_artifact_type_name = self.artifact_type_name,
          artifact_processor_name = self.processor_name,
          runtime_name = self.runtime_name,
      )
      return composition
    
    def _mlops_deploy(self):
      try:
          # Create the deployment (deploy the model).
#           print("---->>>>>", to_deploy)
          deployed_deployment = self.client.deployer.deployment.create_deployment(
              mlops.DeployCreateDeploymentRequest(deployment=to_deploy)
          ).deployment
          print("Deployment {} has started.".format(deployed_deployment.id))
          # Waiting for the deployment to become healthy.
          deployment_status = self.deployment_should_become_healthy(deployed_deployment.id)
          if deployment_status.state == mlops.DeployDeploymentState.HEALTHY:
              print("Deployment has become healthy")
          else:
              print(
                  f"Deployment still not healthy after max wait time with state: {deployment_status.state}"
              )
      except Exception:
          raise

      return deployed_deployment
    
    def mlops_default_deploy(self):
        # Define deployment
        global to_deploy
        to_deploy = mlops.DeployDeployment(
            project_id = self.project.id,
            display_name = self.registered_model_name,
            deployment_environment_id = self._find_mlops_environment(),
            single_deployment = mlops.DeploySingleDeployment(
                deployment_composition = self._dai_mlflow_flavor_mojo_composite(),
                kubernetes_resource_spec = mlops.DeployKubernetesResourceSpec(
                    kubernetes_resource_requirement = mlops.DeployKubernetesResourceRequirement(
                        requests = json.loads(
                            self.resource_request
                        ),  # {"cpu": "200m", "memory": "256Mi"},
                    ),
                    replicas = self.replica,
                ),
            ),
        )
        # Create the deployment (deploy the model).
        deployment = self._mlops_deploy()
        return deployment

    def mlops_depoly(self):
        # Creating a project in MLOps if a project by the given name doesn not exist.
        # prj: mlops.StorageProject
        global mlops_exp
        try:
            self.project = self._get_project_id()
            print("Existing project found.")
        except LookupError:
            self.project = self._create_project()
            print("New project created.")
        mlops_exp = self.import_model_to_mlops()
        model_dep_details = self.mlops_default_deploy()
        return model_dep_details

