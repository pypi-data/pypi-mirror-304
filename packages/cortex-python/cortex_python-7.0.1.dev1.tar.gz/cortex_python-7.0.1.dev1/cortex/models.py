"""
Copyright 2024 Tecnotree, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

----
Module to interact with the Sensa model registry
"""

import os
from typing import Optional, Dict, Any, Union
from cortex.serviceconnector import _Client
from cortex.utils import generate_token

try:
    import mlflow
except ImportError:
    mlflow = None


def check_installed():
    """
    Checks if the model SDK extra is installed
    :return:
    """
    if mlflow is None:
        raise NotImplementedError(
            'Models SDK extra not installed, please run `pip install cortex-python[models_dev]` to install')


class ModelClient(_Client):
    """
    Client for model registry, this class requires the `models_sdk` extras to be installed
    """

    def _setup_model_client(self, verify_ssl_cert=None, ttl="2h"):
        # Generate a JWT, this call stores the JWT in `_serviceconnector.jwt` ( meh )

        if verify_ssl_cert is None:
            verify_ssl_cert = self._serviceconnector.verify_ssl_cert

        if self._serviceconnector.token is not None:
            token = self._serviceconnector.token
        else:
            token = generate_token(self._serviceconnector._config, verify_ssl_cert=verify_ssl_cert, validity=ttl)  # pylint: disable=protected-access
        mlflow.set_tracking_uri(self._serviceconnector.url)
        os.environ['MLFLOW_TRACKING_URI'] = self._serviceconnector.url
        os.environ['MLFLOW_TRACKING_TOKEN'] = token
        # Following behavior from python requests https://requests.readthedocs.io/en/latest/user/advanced/#ssl-cert-verification
        if verify_ssl_cert is False:
            os.environ['MLFLOW_TRACKING_INSECURE_TLS'] = "true"
        elif isinstance(verify_ssl_cert, str):
            os.environ['CURL_CA_BUNDLE'] = verify_ssl_cert

        #  detect cortex client setting to avoid invalid SSL cert errors
        # os.environ['MLFLOW_TRACKING_CLIENT_CERT_PATH']=
        # Need api to fetch serverside userid..
        # os.environ['MLFLOW_TRACKING_USERNAME']=_Client.???

    def login(self, ttl: Optional[Union[str, int]] = '2h', verify_ssl_cert: Optional[Union[bool, str]]=None):
        """
        Configure connection settings for model registry.
        :param ttl: Time to live, DEFAULT: 2h
        :param verify_ssl_cert: Boolean enable/disable SSL certificate or String with certificate filepath, DEFAULT: True
        """
        check_installed()
        self._setup_model_client(ttl=ttl, verify_ssl_cert=verify_ssl_cert)
        print("Configuring connection for model registry")

    def create_experiment(self,
                          name: str,
                          tags: Optional[Dict[str, Any]] = None,
                          ) -> str:
        """
        Create an MLFlow experiment with default tags
        :param name: experiment name, must be unique
        :param tags: optional experiment tags
        """
        check_installed()
        if tags is None:
            tags = {}
        # default to client project if project tag isn't specified
        if tags.get('project') is None:
            tags['project'] = self._project()
        return mlflow.create_experiment(name, tags=tags)
