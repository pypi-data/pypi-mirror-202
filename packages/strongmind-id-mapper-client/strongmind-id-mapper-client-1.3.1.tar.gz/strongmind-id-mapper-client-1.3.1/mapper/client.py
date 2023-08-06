from dataclasses import fields
from typing import List, Dict, Any

import requests
from requests import HTTPError

from mapper.errors import IdentifierMapperError, PairNotFoundError, PartnerNotFoundError
from mapper.partner import Partner


class IDMapperClient:
    def __init__(self, secret: Dict):
        self.token = secret['token']
        self.domain = secret['domain']

    def _headers(self):
        headers = {'Authorization': f'Token {self.token}'}
        return headers

    def _get(self, url, params=None, partner_api: bool = False):
        response = requests.get(url, headers=self._headers(), params=params)
        try:
            response.raise_for_status()
        except requests.HTTPError as http_error:
            handle_http_error(http_error, partner_api=partner_api)
        return response

    def _put(self, url, payload):
        response = requests.put(url, headers=self._headers(), json=payload)
        try:
            response.raise_for_status()
        except requests.HTTPError as http_error:
            raise IdentifierMapperError(http_error)
        return response

    def get_pairs(self, service, value):
        url = f"https://{self.domain}/api/v1/pairs/"
        params = {service: value}
        return self._get(url, params).json()

    def get_pair_by_guid(self, guid):
        url = f"https://{self.domain}/api/v1/pairs/{guid}"
        if not guid.startswith('strongmind.guid://'):
            url += '/'

        return self._get(url).json()

    def get_partner_by_name(self, partner_name) -> Partner:
        url = f"https://{self.domain}/api/v1/partners/{partner_name}/"
        responded_partner = self._get(url, partner_api=True).json()
        return self._json_to_partner(responded_partner)

    def get_partner_by_id(self, partner_id: str) -> Partner:
        url = f"https://{self.domain}/api/v1/partners/{partner_id}/"
        responded_partner = self._get(url, partner_api=True).json()
        return self._json_to_partner(responded_partner)

    def get_partners_by_fields(self, **kwargs) -> List[Partner]:
        url = f"https://{self.domain}/api/v1/partners/"
        response = self._get(url, params=kwargs, partner_api=True)
        responded_partners = response.json()
        if not responded_partners:
            raise PartnerNotFoundError(HTTPError(response=response, request=response.request))
        all_partners = []

        for responded_partner in responded_partners:
            all_partners.append(self._json_to_partner(responded_partner))

        return all_partners

    # CAUTION: This should only be used if you know what you're doing
    def put_partner(self, **kwargs):
        partner_name = kwargs.get('name')
        if not partner_name:
            raise PartnerNotFoundError()

        url = f"https://{self.domain}/api/v1/partners/{partner_name}/"
        return self._put(url, kwargs)

    def _json_to_partner(self, partner_json: Dict[str, Any]) -> Partner:
        partner_model_keys = [field.name for field in fields(Partner)]
        shared_keys = set(partner_json) & set(partner_model_keys)

        partner_dict = {}
        for key in shared_keys:
            partner_dict[key] = partner_json[key]
        return Partner(**partner_dict)

    def submit_pairs(self, payload):
        """Send the payload as a bunch of pairs to the Identifier Mapper by
        sending a POST to the Pairs API"""
        url = f"https://{self.domain}/api/v1/pairs/"
        response = requests.post(url, headers=self._headers(), json=payload)

        try:
            response.raise_for_status()
        except requests.HTTPError as http_error:
            raise IdentifierMapperError(http_error)

    def get_or_create_uuid(self, key: str) -> str:
        """Send a GET request to the id mapper uuid route and receive a UUID string"""
        url = f"https://{self.domain}/api/v1/uuid/{key}/"
        return self._get(url).json()


def handle_http_error(http_error, partner_api: bool = False):
    if http_error.response.status_code == 404:
        if partner_api:
            raise PartnerNotFoundError(http_error)
        else:
            raise PairNotFoundError(http_error)
    raise IdentifierMapperError(http_error)
