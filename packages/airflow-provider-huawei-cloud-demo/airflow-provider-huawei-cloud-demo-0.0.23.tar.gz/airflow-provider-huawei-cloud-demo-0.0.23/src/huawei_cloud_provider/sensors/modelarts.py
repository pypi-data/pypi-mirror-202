#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence

if TYPE_CHECKING:
    from airflow.utils.context import Context

from airflow.compat.functools import cached_property
from airflow.exceptions import AirflowException
from huawei_cloud_provider.hooks.modelarts import ModelArtsHook
from airflow.sensors.base import BaseSensorOperator


class ModelArtsDatasetSensor(BaseSensorOperator):

    template_fields: Sequence[str] = ("dataset_id",)

    SUCCESS_STATES = (1,)

    def __init__(
        self,
        dataset_id: str,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.dataset_id = dataset_id
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.project_id = project_id
        self.region = region

    def poke(self, context: Context) -> bool:

        datasets = self.get_hook.list_dataset()["datasets"]

        for dataset in datasets:
            if dataset["dataset_id"] == self.dataset_id:

                if dataset["status"] in self.SUCCESS_STATES:
                    return True

                return False

        return False

    @cached_property
    def get_hook(self) -> ModelArtsHook:
        """Create and return a ModelArtsHook"""
        return ModelArtsHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, project_id=self.project_id, region=self.region
        )


class ModelArtsDatasetVersionSensor(BaseSensorOperator):

    template_fields: Sequence[str] = ("dataset_id", "version_id")

    SUCCESS_STATES = (1,)
    FAILURE_STATES = (4,)

    def __init__(
        self,
        dataset_id: str,
        version_id: str,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.dataset_id = dataset_id
        self.version_id = version_id
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.project_id = project_id
        self.region = region

    def poke(self, context: Context) -> bool:

        versions = self.get_hook.list_dataset_version(self.dataset_id)[
            "versions"]

        for version in versions:
            if version["version_id"] == self.version_id:
                if version["status"] in self.FAILURE_STATES:
                    raise AirflowException(
                        f"Dataset version {self.version_id} failed to create.")
                if version["status"] in self.SUCCESS_STATES:
                    return True

                return False

        return False

    @cached_property
    def get_hook(self) -> ModelArtsHook:
        """Create and return a ModelArtsHook"""
        return ModelArtsHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, project_id=self.project_id, region=self.region
        )


class ModelArtsTrainingJobSensor(BaseSensorOperator):

    template_fields: Sequence[str] = ("training_job_id",)
    # Creating Pending Running Failed Completed, Terminating Terminated Abnormal
    SUCCESS_STATES = ("Completed",)
    FAILURE_STATES = ("Abnormal", "Failed")

    def __init__(
        self,
        training_job_id: str,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.training_job_id = training_job_id
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.project_id = project_id
        self.region = region

    def poke(self, context: Context) -> bool:

        job_status = self.get_hook.list_training_job(
            self.training_job_id)["status"]["phase"]

        if job_status in self.FAILURE_STATES:
            raise AirflowException(
                f"Training job {self.training_job_id} failed to create.")
        if job_status in self.SUCCESS_STATES:
            return True

        return False

    @cached_property
    def get_hook(self) -> ModelArtsHook:
        """Create and return a ModelArtsHook"""
        return ModelArtsHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, project_id=self.project_id, region=self.region
        )


class ModelArtsServiceJobSensor(BaseSensorOperator):

    template_fields: Sequence[str] = ("service_id",)
    # Creating Pending Running Failed Completed, Terminating Terminated Abnormal
    # running deploying concerning failed stopped finished
    SUCCESS_STATES = ("finished", "stopped", "running")
    FAILURE_STATES = ("failed", "concerning")

    def __init__(
        self,
        service_id: str,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.service_id = service_id
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.project_id = project_id
        self.region = region

    def poke(self, context: Context) -> bool:

        service_status = self.get_hook.show_service(
            self.service_id)["status"]

        if service_status in self.FAILURE_STATES:
            raise AirflowException(
                f"Service {self.service_id} failed to create.")
        if service_status in self.SUCCESS_STATES:
            return True

        return False

    @cached_property
    def get_hook(self) -> ModelArtsHook:
        """Create and return a ModelArtsHook"""
        return ModelArtsHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, project_id=self.project_id, region=self.region
        )

class ModelArtsModelSensor(BaseSensorOperator):

    template_fields: Sequence[str] = ("model_id",)
    SUCCESS_STATES = ("published",)
    FAILURE_STATES = () #TODO:

    def __init__(
        self,
        model_id: str,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.model_id = model_id
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.project_id = project_id
        self.region = region

    def poke(self, context: Context) -> bool:
        model_status = self.get_hook.show_model(self.model_id)["model_status"]

        if model_status in self.FAILURE_STATES:
            raise AirflowException(
                f"Model {self.model_id} failed to create.")
        if model_status in self.SUCCESS_STATES:
            return True

        return False

    @cached_property
    def get_hook(self) -> ModelArtsHook:
        """Create and return a ModelArtsHook"""
        return ModelArtsHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, project_id=self.project_id, region=self.region
        )
