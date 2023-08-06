import json

import pytest
import responses
from faker import Faker

from mapper.client import IDMapperClient
from mapper.errors import IdentifierMapperError, PairNotFoundError, PartnerNotFoundError
from test.factories.partner import PartnerFactory
from test.helpers import add_authenticated_payload
from test.response_factory import response_factory as id_mapper_factory

fake = Faker()


class TestIDMapperClient:
    def setup(self):
        self.responses = responses.RequestsMock()
        self.responses.start()
        self.domain = fake.domain_name()
        self.token = fake.sentence()
        secret = {"domain": self.domain, "token": self.token}

        self.target = IDMapperClient(secret)
        self.target.domain = self.domain
        self.target.token = self.token
        self.partner = PartnerFactory()

    def teardown(self):
        self.responses.stop(allow_assert=False)
        self.responses.reset()

    def test_get_credentials(self):
        """An Identifier Mapper API mapper holds its credentials"""

        assert self.target.token == self.token
        assert self.target.domain == self.domain

    def test_error_is_raised_on_get(self):
        """An Identifier Mapper API mapper raises an error when it receives an error from the service"""
        service = fake.word()
        value = fake.word()
        url = f"https://{self.domain}/api/v1/pairs/?{service}={value}"

        self.responses.add(
            responses.GET,
            url,
            status=500
        )

        with pytest.raises(IdentifierMapperError) as exception:
            self.target.get_pairs(service, value)

        assert exception.value.response is not None
        assert exception.value.request is not None
        assert exception.value.response.status_code == 500
        assert exception.value.request.url == url

    def test_missing_error_on_404(self):
        """An Identifier Mapper API mapper raises an PairNotFound error when it fails to find a pair from the service"""
        service = fake.word()
        value = fake.word()
        url = f"https://{self.domain}/api/v1/pairs/?{service}={value}"

        self.responses.add(
            responses.GET,
            url,
            status=404
        )

        with pytest.raises(PairNotFoundError) as exception:
            self.target.get_pairs(service, value)

        assert exception.value.response is not None
        assert exception.value.request is not None
        assert exception.value.response.status_code == 404
        assert exception.value.request.url == url

    def test_get_returns_api_body(self):
        """An Identifier Mapper API mapper returns the API Body when we try to get a service/value pair from an
        authenticated service """
        service = fake.word()
        value = fake.word()
        subdomain, response_body_callable = id_mapper_factory()
        response_body = response_body_callable()

        add_authenticated_payload(
            self.responses,
            responses.GET,
            f"https://{self.domain}/api/v1/pairs/?{service}={value}",
            body=json.dumps(response_body),
            auth=f"Token {self.token}"
        )

        return_value = self.target.get_pairs(service, value)

        assert return_value == response_body

    def test_get_pairs_with_query_params_does_not_redirect_without_trailing_slash(self):
        """An Identifier Mapper API mapper returns the API Body when we try to get a service/value pair from an
        authenticated service, only when trailing slash is present"""
        service = fake.word()
        value = fake.word()
        subdomain, response_body_callable = id_mapper_factory()
        response_body = response_body_callable()

        add_authenticated_payload(
            self.responses,
            responses.GET,
            f"https://{self.domain}/api/v1/pairs?{service}={value}",
            body=json.dumps(response_body),
            auth=f"Token {self.token}",
            status=301
        )

        add_authenticated_payload(
            self.responses,
            responses.GET,
            f"https://{self.domain}/api/v1/pairs/?{service}={value}",
            body=json.dumps(response_body),
            auth=f"Token {self.token}"
        )

        self.target.get_pairs(service, value)
        assert len(self.responses.calls) == 1
        assert self.responses.calls[0].response.status_code == 200

    def test_client_can_get_pair_by_guid(self):
        """An Identifier Mapper mapper can look up a set of related pairs by a GUID string, nee sourcedId"""
        guid = fake.uuid4()
        subdomain, response_body_callable = id_mapper_factory()
        response_body = response_body_callable()

        add_authenticated_payload(
            self.responses,
            responses.GET,
            f"https://{self.domain}/api/v1/pairs/{guid}/",
            body=json.dumps(response_body),
            auth=f"Token {self.token}"
        )

        return_value = self.target.get_pair_by_guid(guid)

        assert return_value == response_body

    def test_client_can_get_pair_by_strongmind_guid(self):
        """An Identifier Mapper mapper can look up a set of related pairs by a GUID string, nee sourcedId"""
        service = fake.word()
        value = fake.word()
        subdomain, response_body_callable = id_mapper_factory()
        psuedo_guid = f"strongmind.guid://{service}/{subdomain}/{value}"
        response_body = response_body_callable()

        add_authenticated_payload(
            self.responses,
            responses.GET,
            f"https://{self.domain}/api/v1/pairs/{psuedo_guid}",
            body=json.dumps(response_body),
            auth=f"Token {self.token}"
        )

        return_value = self.target.get_pair_by_guid(psuedo_guid)

        assert return_value == response_body

    def test_client_can_put_partner(self):
        """An Identifier Mapper can edit a partner"""
        kwargs = {
            "name": self.partner.name,
            "canvas_authentication_provider_type": fake.random_element(elements=["cas", "openid_connect", ""])
        }

        add_authenticated_payload(
            self.responses,
            responses.PUT,
            f"https://{self.domain}/api/v1/partners/{self.partner.name}/",
            body=json.dumps(kwargs),
            auth=f"Token {self.token}"
        )
        response = self.target.put_partner(**kwargs)
        assert response.status_code == 200

    def test_put_partner_raises_partner_not_found_error(self):
        """An Identifier Mapper raises a PartnerNotFoundError when name is not passed in as a kwarg"""
        kwargs = {
            "canvas_authentication_provider_type": fake.random_element(elements=["cas", "openid_connect", ""])
        }
        with pytest.raises(PartnerNotFoundError):
            self.target.put_partner(**kwargs)

    def test_client_can_get_pair_by_guid_does_not_redirect_without_trailing_slash(self):
        """An Identifier Mapper mapper can look up a set of related pairs by a GUID
        string, only when trailing slash is present"""
        guid = fake.uuid4()
        subdomain, response_body_callable = id_mapper_factory()
        response_body = response_body_callable()

        add_authenticated_payload(
            self.responses,
            responses.GET,
            f"https://{self.domain}/api/v1/pairs/{guid}",
            body=json.dumps(response_body),
            auth=f"Token {self.token}",
            status=301
        )

        add_authenticated_payload(
            self.responses,
            responses.GET,
            f"https://{self.domain}/api/v1/pairs/{guid}/",
            body=json.dumps(response_body),
            auth=f"Token {self.token}",
            status=200
        )

        self.target.get_pair_by_guid(guid)
        assert len(self.responses.calls) == 1
        assert self.responses.calls[0].response.status_code == 200

    def test_client_does_not_add_trailing_slash_for_gets_with_strongmind_guid(self):
        """
        Given we have a StrongMind guid look up
        When the request is handled
        Then the client will be sent the request without a trailing slash
        """
        service = fake.word()
        value = fake.word()
        subdomain, response_body_callable = id_mapper_factory()
        strongmind_guid = f"strongmind.guid://{service}/{subdomain}/{value}"
        response_body = response_body_callable()

        add_authenticated_payload(
            self.responses,
            responses.GET,
            f"https://{self.domain}/api/v1/pairs/{strongmind_guid}",
            body=json.dumps(response_body),
            auth=f"Token {self.token}",
            status=301
        )

        add_authenticated_payload(
            self.responses,
            responses.GET,
            f"https://{self.domain}/api/v1/pairs/{strongmind_guid}/",
            body=json.dumps(response_body),
            auth=f"Token {self.token}",
            status=200
        )

        self.target.get_pair_by_guid(strongmind_guid)
        assert len(self.responses.calls) == 1
        assert self.responses.calls[0].response.status_code == 301

    def test_client_can_submit_pairs(self):
        """An Identifier Mapper mapper can submit pairs"""
        service = fake.word()
        value = fake.word()
        subdomain, response_body_callable = id_mapper_factory()
        request_body = response_body_callable()

        add_authenticated_payload(
            self.responses,
            responses.POST,
            f"https://{self.domain}/api/v1/pairs/",
            body=json.dumps(request_body),
            auth=f"Token {self.token}"
        )

        self.target.submit_pairs(request_body)
