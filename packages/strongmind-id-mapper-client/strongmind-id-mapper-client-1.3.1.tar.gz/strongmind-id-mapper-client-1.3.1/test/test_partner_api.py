import dataclasses
import random

from mapper.client import IDMapperClient
from mapper.partner import Partner
from mapper.errors import IdentifierMapperError, PartnerNotFoundError
from test.factories.standalone_partner import StandalonePartnerFactory
from test.factories.partner import PartnerFactory
from test.helpers import add_authenticated_payload
import json
import responses
import pytest

from faker import Faker

fake = Faker()


class TestIDMapperPartnerAPI:
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

    def test_get_partners_by_fields(self) -> None:
        """A partner with full data is successfully retrieved from the Identifier Mapper"""
        fake_partner = PartnerFactory()
        field_choice = random.choice([field.name for field in dataclasses.fields(fake_partner)])
        field_value = dataclasses.asdict(fake_partner)[field_choice]
        self.responses.add(
            responses.GET,
            f"https://{self.domain}/api/v1/partners/?{field_choice}={field_value}",
            body=json.dumps([dataclasses.asdict(fake_partner)])
        )

        partners = self.target.get_partners_by_fields(**{field_choice: field_value})
        partner = partners[0]

        assert isinstance(partner, Partner)
        self._assert_identical_partners(fake_partner, partner)

    def test_get_standalone_partner(self) -> None:
        """A standalone partner with data as null is correctly retrieved from the Identifier Mapper"""
        fake_partner = StandalonePartnerFactory()

        field_value = None
        while not field_value:
            field_choice = random.choice([field.name for field in dataclasses.fields(fake_partner)])
            field_value = dataclasses.asdict(fake_partner)[field_choice]

        self.responses.add(
            responses.GET,
            f"https://{self.domain}/api/v1/partners/?{field_choice}={field_value}",
            body=json.dumps([dataclasses.asdict(fake_partner)])
        )

        partners = self.target.get_partners_by_fields(**{field_choice: field_value})
        partner = partners[0]

        assert isinstance(partner, Partner)
        self._assert_identical_partners(fake_partner, partner)

    def test_get_partners_by_fields_returns_extra_fields(self) -> None:
        """Additional fields, not in our model, from the partner API do not matter"""
        fake_partner_response = dataclasses.asdict(PartnerFactory())
        fake_partner_response["new_field_" + fake.word()] = fake.sentence()
        self.responses.add(
            responses.GET,
            f"https://{self.domain}/api/v1/partners/?foo=bar",
            body=json.dumps([fake_partner_response])
        )

        partner = self.target.get_partners_by_fields(foo='bar')[0]

        assert len(fake_partner_response.keys()) > len(dataclasses.fields(partner))
        assert isinstance(partner, Partner)

    def test_error_is_raised_on_get_partners_by_fields(self):
        """An Identifier Mapper API mapper raises an exception when it receives an error from the service"""
        field = fake.word()
        value = fake.word()
        url = f"https://{self.domain}/api/v1/partners/?{field}={value}"

        self.responses.add(
            responses.GET,
            url,
            status=500
        )

        with pytest.raises(IdentifierMapperError) as exception:
            self.target.get_partners_by_fields(**{field: value})

        assert exception.value.response is not None
        assert exception.value.request is not None
        assert exception.value.response.status_code == 500
        assert exception.value.request.url == url

    def test_not_found_error_is_raised_on_get_partners_by_fields(self):
        """An Identifier Mapper mapper raises a different exception when it receives a 404"""
        field = fake.word()
        value = fake.word()
        url = f"https://{self.domain}/api/v1/partners/?{field}={value}"

        self.responses.add(
            responses.GET,
            url,
            status=404
        )

        with pytest.raises(PartnerNotFoundError) as exception:
            self.target.get_partners_by_fields(**{field: value})

        assert exception.value.response is not None
        assert exception.value.request is not None
        assert exception.value.response.status_code == 404
        assert exception.value.request.url == url

    def test_not_found_error_is_raised_when_get_partners_by_fields_gets_an_empty_list(self) -> None:
        """An Identifier Mapper mapper raises a different exception when it receives a 404"""
        field = fake.word()
        value = fake.word()
        url = f"https://{self.domain}/api/v1/partners/?{field}={value}"

        self.responses.add(
            responses.GET,
            url,
            status=200,
            body="[]"
        )

        with pytest.raises(PartnerNotFoundError) as exception:
            self.target.get_partners_by_fields(**{field: value})

        assert exception.value.response is not None
        assert exception.value.request is not None
        assert exception.value.response.status_code == 200
        assert exception.value.request.url == url

    def test_can_get_a_partner_with_multiple_fields(self):
        """The Identifier Mapper mapper properly forms the query string when it looks up with multiple fields"""
        fake_partner = PartnerFactory()

        add_authenticated_payload(
            self.responses,
            responses.GET,
            f"https://{self.domain}/api/v1/partners/?canvas_domain={fake_partner.canvas_domain}&canvas_account={fake_partner.canvas_account}",
            body=json.dumps([dataclasses.asdict(fake_partner)]),
            auth=f"Token {self.token}"
        )

        partner = self.target.get_partners_by_fields(canvas_domain=fake_partner.canvas_domain,
                                                     canvas_account=fake_partner.canvas_account)[0]
        self._assert_identical_partners(fake_partner, partner)

    def _assert_identical_partners(self, partner1, partner2):
        assert partner1.name == partner2.name
        assert partner1.canvas_domain == partner2.canvas_domain
        assert partner1.canvas_account == partner2.canvas_account
        assert partner1.powerschool_domain == partner2.powerschool_domain
        assert partner1.powerschool_dcid == partner2.powerschool_dcid
        assert partner1.fuji_id == partner2.fuji_id
        assert partner1.canvas_account_uuid == partner2.canvas_account_uuid
        assert partner1.clever_district_id == partner2.clever_district_id
        assert partner1.group_label == partner2.group_label

    def test_get_partner_by_name(self) -> None:
        """A partner with full data is successfully retrieved from the Identifier Mapper by name"""
        fake_partner = PartnerFactory()

        add_authenticated_payload(
            self.responses,
            responses.GET,
            f"https://{self.domain}/api/v1/partners/{fake_partner.name}/",
            body=json.dumps(dataclasses.asdict(fake_partner)),
            auth=f"Token {self.token}"
        )

        partner = self.target.get_partner_by_name(fake_partner.name)

        assert isinstance(partner, Partner)
        self._assert_identical_partners(fake_partner, partner)

    def test_get_partner_by_name_does_not_redirect_without_trailing_slash(self) -> None:
        """A client sends 1 GET to the server and receives a 200 response code
        when the URL in the GET has a trailing slash"""
        fake_partner = PartnerFactory()
        self.responses.add(
            responses.GET,
            f"https://{self.domain}/api/v1/partners/{fake_partner.name}",
            body=json.dumps(dataclasses.asdict(fake_partner)),
            status=301
        )

        self.responses.add(
            responses.GET,
            f"https://{self.domain}/api/v1/partners/{fake_partner.name}/",
            body=json.dumps(dataclasses.asdict(fake_partner)),
            status=200
        )
        self.target.get_partner_by_id(fake_partner.name)
        assert len(self.responses.calls) == 1
        assert self.responses.calls[0].response.status_code == 200

    def test_get_partner_by_id(self) -> None:
        """A partner with full data is successfully retrieved from the Identifier Mapper by ID"""
        fake_partner = PartnerFactory()

        add_authenticated_payload(
            self.responses,
            responses.GET,
            f"https://{self.domain}/api/v1/partners/{fake_partner.id}/",
            body=json.dumps(dataclasses.asdict(fake_partner)),
            auth=f"Token {self.token}"
        )

        partner = self.target.get_partner_by_id(fake_partner.id)

        assert isinstance(partner, Partner)
        self._assert_identical_partners(fake_partner, partner)

    def test_get_partner_by_id_does_not_redirect_without_trailing_slash(self) -> None:
        """A client sends 1 GET to the server and receives a 200 response code
        when the URL in the GET has a trailing slash"""
        fake_partner = PartnerFactory()
        self.responses.add(
            responses.GET,
            f"https://{self.domain}/api/v1/partners/{fake_partner.id}",
            body=json.dumps(dataclasses.asdict(fake_partner)),
            status=301
        )
        self.responses.add(
            responses.GET,
            f"https://{self.domain}/api/v1/partners/{fake_partner.id}/",
            body=json.dumps(dataclasses.asdict(fake_partner)),
            status=200
        )
        self.target.get_partner_by_id(fake_partner.id)
        assert len(self.responses.calls) == 1
        assert self.responses.calls[0].response.status_code == 200

    def test_error_is_raised_on_get_partner_by_name(self):
        """An Identifier Mapper API mapper raises an exception when it receives an error from the service"""
        name = fake.word()
        url = f"https://{self.domain}/api/v1/partners/{name}/"

        self.responses.add(
            responses.GET,
            url,
            status=500
        )

        with pytest.raises(IdentifierMapperError) as exception:
            self.target.get_partner_by_name(name)

        assert exception.value.response is not None
        assert exception.value.request is not None
        assert exception.value.response.status_code == 500
        assert exception.value.request.url == url

    def test_not_found_error_is_raised_on_get_partner_by_name(self):
        """An Identifier Mapper mapper raises a different exception when it receives a 404"""
        name = fake.word()
        url = f"https://{self.domain}/api/v1/partners/{name}/"

        self.responses.add(
            responses.GET,
            url,
            status=404
        )

        with pytest.raises(PartnerNotFoundError) as exception:
            self.target.get_partner_by_name(name)

        assert exception.value.response is not None
        assert exception.value.request is not None
        assert exception.value.response.status_code == 404
        assert exception.value.request.url == url

    def test_not_found_error_is_raised_on_get_partner_by_id(self):
        """An Identifier Mapper mapper raises a different exception when it receives a 404"""
        id = fake.uuid4()
        url = f"https://{self.domain}/api/v1/partners/{id}/"

        self.responses.add(
            responses.GET,
            url,
            status=404
        )

        with pytest.raises(PartnerNotFoundError) as exception:
            self.target.get_partner_by_id(id)

        assert exception.value.response is not None
        assert exception.value.request is not None
        assert exception.value.response.status_code == 404
        assert exception.value.request.url == url

