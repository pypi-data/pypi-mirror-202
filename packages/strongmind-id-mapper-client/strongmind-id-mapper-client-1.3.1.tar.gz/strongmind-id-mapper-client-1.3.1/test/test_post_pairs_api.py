from mapper.client import IDMapperClient
from mapper.errors import IdentifierMapperError, PairNotFoundError, PartnerNotFoundError
import json
import responses
import pytest

from faker import Faker

fake = Faker()


class TestIDMapperPostPairsAPI:
    def setup(self):
        self.responses = responses.RequestsMock()
        self.responses.start()

        self.domain = fake.domain_name()
        self.token = fake.sentence()
        self.target = IDMapperClient({"token": self.token, "domain": self.domain})

    def teardown(self):
        self.responses.stop(allow_assert=False)
        self.responses.reset()

    def test_client_can_submit_pairs(self) -> None:
        """An Identifier Mapper mapper can submit a dictionary payload to be treated as pairs"""
        payload = {
            "com.powerschool.user.numbers": {
                "venture": 12345
            },
            "com.instructure.canvas.user.ids": {
                "venture": 58
            }
        }

        self.responses.add(
            responses.POST,
            f"https://{self.target.domain}/api/v1/pairs/",
            status=201
        )

        partners = self.target.submit_pairs(payload)

        assert len(self.responses.calls) == 1
        assert json.loads(self.responses.calls[0].request.body) == payload

    def test_client_cannot_submit_pairs_does_not_redirect_without_trailing_slash(self) -> None:
        """An Identifier Mapper mapper can submit a dictionary payload to be
        treated as pairs when the URL in the POST has a trailing slash"""
        payload = {
            "com.powerschool.user.numbers": {
                "venture": 12345
            },
            "com.instructure.canvas.user.ids": {
                "venture": 58
            }
        }

        self.responses.add(
            responses.POST,
            f"https://{self.target.domain}/api/v1/pairs",
            status=301
        )

        self.responses.add(
            responses.POST,
            f"https://{self.target.domain}/api/v1/pairs/",
            status=201
        )

        partners = self.target.submit_pairs(payload)

        assert len(self.responses.calls) == 1
        assert json.loads(self.responses.calls[0].request.body) == payload

    def test_client_post_failure_raises_exception(self) -> None:
        """An Identifier Mapper mapper will raise an error when the POST fails"""
        url = f"https://{self.target.domain}/api/v1/pairs/"
        self.responses.add(
            responses.POST,
            url,
            status=500
        )

        with pytest.raises(IdentifierMapperError) as exception:
            self.target.submit_pairs({})

        assert exception.value.response is not None
        assert exception.value.request is not None
        assert exception.value.response.status_code == 500
        assert exception.value.request.url == url
