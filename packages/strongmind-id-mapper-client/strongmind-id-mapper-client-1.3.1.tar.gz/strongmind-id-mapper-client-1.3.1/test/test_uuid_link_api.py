import json

import pytest
import responses
from faker import Faker

from mapper.client import IDMapperClient
from mapper.errors import IdentifierMapperError

fake = Faker()


class TestIDMapperUuidLinkAPI:
    def setup(self):
        self.responses = responses.RequestsMock()
        self.responses.start()
        self.domain = fake.domain_name()
        self.token = fake.sentence()
        secret = {"domain": self.domain, "token": self.token}

        self.target = IDMapperClient(secret)
        self.target.domain = self.domain
        self.target.token = self.token

    def teardown(self):
        self.responses.stop(allow_assert=False)
        self.responses.reset()

    def test_get_uuid_link_by_string_key(self) -> None:
        """A uuid is successfully retrieved from the Identifier Mapper"""
        key = fake.word()
        uuid = fake.uuid4()
        self.responses.add(
            responses.GET,
            f"https://{self.domain}/api/v1/uuid/{key}/",
            body=f'"{uuid}"'
        )

        result = self.target.get_or_create_uuid(key=key)

        assert result == uuid

    def test_get_uuid_link_by_string_key_does_not_redirect_without_trailing_slash(self) -> None:
        """A uuid is successfully retrieved from the Identifier Mapper
        when the URL in the GET has a trailing slash"""
        key = fake.word()
        uuid = fake.uuid4()
        self.responses.add(
            responses.GET,
            f"https://{self.domain}/api/v1/uuid/{key}",
            body=f'"{uuid}"',
            status=301
        )
        self.responses.add(
            responses.GET,
            f"https://{self.domain}/api/v1/uuid/{key}/",
            body=f'"{uuid}"',
            status=200
        )

        self.target.get_or_create_uuid(key=key)

        assert len(self.responses.calls) == 1
        assert self.responses.calls[0].response.status_code == 200

    def test_get_uuid_link_raises_error(self) -> None:
        """An IdentifierMapperError is raised when the request returns a 4XX or 5XX"""
        key = fake.word()
        uuid = fake.uuid4()
        url = f"https://{self.domain}/api/v1/uuid/{key}/"
        self.responses.add(
            responses.GET,
            url,
            status=500,
        )

        with pytest.raises(IdentifierMapperError) as exception:
            self.target.get_or_create_uuid(key=key)

        assert exception.value.response is not None
        assert exception.value.request is not None
        assert exception.value.response.status_code == 500
        assert exception.value.request.url == url