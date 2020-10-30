# Copyright (c) 2020 original authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an \"AS IS\" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import requests

from expertai.nlapi.v1 import constants
from expertai.nlapi.v1.errors import CredentialsError, ExpertAiRequestError


class ExpertAiAuth:
    @property
    def header(self):
        value = constants.AUTH_HEADER_VALUE.format(self.fetch_token_value())
        return {constants.AUTH_HEADER_KEY: value}

    @property
    def username(self):
        value = os.getenv(constants.USERNAME_ENV_VARIABLE)
        if not value:
            raise CredentialsError("Missing username env variable")
        return value

    @property
    def password(self):
        value = os.getenv(constants.PASSWORD_ENV_VARIABLE)
        if not value:
            raise CredentialsError("Missing password env variable")
        return value

    def token_is_valid(self):
        return os.getenv(constants.TOKEN_ENV_VARIABLE)

    def fetch_token_value(self):
        if self.token_is_valid():
            return os.getenv(constants.TOKEN_ENV_VARIABLE)

        response = requests.post(
            url=constants.OAUTH2_TOKEN_URL,
            headers=constants.CONTENT_TYPE_HEADER,
            json={"username": self.username, "password": self.password},
        )

        if not response.ok:
            raise ExpertAiRequestError(
                "Failed to fetch the Bearer Token. Error: {}-{}".format(
                    response.status_code, response.reason
                )
            )

        token = response.text
        os.environ[constants.TOKEN_ENV_VARIABLE] = token
        return token
