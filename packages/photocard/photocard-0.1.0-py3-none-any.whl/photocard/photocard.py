import dataclasses
import datetime
import enum
import json
import random
import re
import time
from typing import List, Dict, Any

import urllib3


@dataclasses.dataclass()
class Address:
    area: Any  # TODO: unknown
    country: str
    house_or_flat_number: str
    postcode: str
    street: str
    town: str

    @staticmethod
    def from_json(source: Dict[str, str]):
        return Address(
            source["area"],
            source["country"],
            source["houseOrFlatNumber"],
            source["postcode"],
            source["street"],
            source["town"]
        )


class ResidencyStatus(enum.Enum):
    LONDON_RESIDENT = "LONDON_RESIDENT"


@dataclasses.dataclass()
class Person:
    address: Address
    affiliation_id: Any | None  # unknown
    alt_phone: str  # unknown
    applicant_id: Any  # TODO: unknown, will find out when ordering 16+
    barred: Any  # unknown
    can_rename: bool
    date_of_birth: datetime.date
    email: str  # this is always null
    forenames: str
    joint_forenames: str  # unknown
    joint_surname: str  # unknown
    joint_title: str  # unknown
    middle_name: str  # unknown
    parent_person_id: int
    person_id: int
    phone: str
    removable: bool
    residency_status: ResidencyStatus  # enum, known values: LONDON_RESIDENT
    surname: str
    title: str

    @staticmethod
    def from_json(source: Dict[str, Any]):
        return Person(
            source["address"],
            source.get("affiliationId"),
            source.get("altPhone"),
            source.get("applicantId"),
            source.get("barred"),
            source["canRename"],
            datetime.datetime.strptime(source["dateOfBirth"], "%Y-%m-%d").date(),
            source.get("email"),
            source["forenames"],
            source.get("jointForenames"),
            source.get("jointSurname"),
            source.get("jointTitle"),
            source.get("middleName"),
            source.get("parentPersonId"),
            source.get("personId"),
            source["phone"],
            source["removable"],
            ResidencyStatus(source["residencyStatus"]),
            source["surname"],
            source["title"]
        )


def _person_from_json(source: Dict[str, Any]):
    if 'houseOrFlatNumber' in source.keys():
        return Address.from_json(source)
    elif 'email' in source.keys():
        return Person.from_json(source)


class CardApplicationType(enum.Enum):
    NEW = "new",
    REPLACE = "replace",


class CardStatus(enum.Enum):
    # TODO: this can't be the only card status
    ACTIVE = "Active"


class CardType(enum.Enum):
    ELEVEN_TO_FIFTEEN = "11-15"


class CardScheme(enum.Enum):
    ELEVEN_TO_FIFTEEN_ZIP_LONDON = "11_to_15_zip_london"


@dataclasses.dataclass()
class ManageLink:
    id: int
    name: str
    description: str
    display_order: int

    @staticmethod
    def from_json(source: Dict[str, Any]):
        return ManageLink(
            source['id'],
            source['name'],
            source['description'],
            source['displayOrder']
        )


@dataclasses.dataclass()
class CardTicket:
    start_date: datetime.date
    expiry_date: datetime.date
    product: str
    zone: str

    @staticmethod
    def from_json(source: Dict[str, Any]):
        return CardTicket(
            datetime.datetime.strptime(source["startDate"], "%Y-%m-%d").date(),
            datetime.datetime.strptime(source["expiryDate"], "%Y-%m-%d").date(),
            source['product'],
            source['zone']
        )


@dataclasses.dataclass()
class Card:
    application_id: int
    application_type: CardApplicationType
    barred_person: Any  # unknown
    can_reapply: Any  # unknown
    card_id: int  # unknown
    card_image_url: str
    card_number: Any  # unknown, appears deprecated
    card_status: CardStatus
    card_type: CardType
    concession_type: Any  # unknown
    created_date: datetime.datetime
    direct_debit_payment_failed: Any  # unknown
    errors: Any  # unknown
    expiry_date: datetime.datetime
    hot_list: bool  # unknown
    info_message: str  # unknown
    manage_links: List[ManageLink]
    oyster_card_id: Any  # unknown, appears deprecated
    oyster_card_number: str
    payment_type: Any  # unknown
    photograph: str  # base64 jpeg
    pre_sales_expiry_date: Any  # unknown
    prepaid_balance: float
    renewable: Any  # unknown
    replaceable: bool
    replacement_reason_id: int  # unknown
    revalidation_expiry_date: datetime.datetime  # unknown
    scheme: CardScheme
    show_cancel_direct_debit: Any  # unknown
    tickets: List[CardTicket]
    upgradable: bool
    upgraded_application_id: int  # unknown
    work_placement: Any  # unknown

    @staticmethod
    def from_json(source: Dict[str, Any]):
        return Card(
            source['applicationId'],
            source['applicationType'],
            source['barredPerson'],
            source['canReapply'],
            source['cardId'],
            "https://photocard.tfl.gov.uk/" + source['cardImage'],
            source['cardNumber'],
            CardStatus(source['cardStatus']),
            CardType(source['cardType']),
            source['concessionType'],
            datetime.datetime.strptime(source['createdDate'], "%Y-%m-%dT%H:%M:%S.%fZ"),
            source['ddpaymentFailed'],
            source['errors'],
            datetime.datetime.strptime(source['expiryDate'], "%Y-%m-%dT%H:%M:%S"),
            source['hotlist'],
            source['infoMessage'],
            source['manageLinks'],
            source['oysterCardId'],
            source['oysterCardNumber'],
            source['paymentType'],
            source['photograph'],
            source['preSalesExpiryDate'],
            float(source['prepaidBalance']),
            source['renewable'],
            source['replaceable'],
            source['replacementReasonId'],
            source['revalidationExpiryDate'],
            source['scheme'],
            source['showCancelDD'],
            source['tickets'],
            source['upgradable'],
            source['upgradedApplicationId'],
            source['workPlacement']
        )


def _card_from_json(source: Dict[str, Any]):
    keys = source.keys()
    if all(k in keys for k in ['id', 'name', 'description']):
        return ManageLink.from_json(source)
    elif all(k in keys for k in ['startDate', 'expiryDate', 'product', 'zone']):
        return CardTicket.from_json(source)
    elif 'scheme' in keys:
        return Card.from_json(source)


@dataclasses.dataclass
class PhotocardSession:
    forename: str
    people: List[int]
    session_token: str
    web_account_id: int

    @staticmethod
    def from_json(source: Dict[str, Any]):
        return PhotocardSession(source["forename"], source["people"], source["sessionToken"], source["webAccountId"])


@dataclasses.dataclass()
class WebAccountSettings:
    applications_in_progress: bool
    borough: str
    email: str
    london_resident: bool
    failed_consecutive_logins: int
    person: Person
    security_answer: str
    security_question: str
    status: str  # TODO: enum (known: VERIFIED), not in the scope of this project atm
    tenant_id: int  # no idea what this is, not documented or shown in frontend anywhere
    web_account_id: int

    @staticmethod
    def from_json(source: Dict[str, Any]):
        return WebAccountSettings(
            source['applicationsInProgress'],
            source['borough'],
            source['email'],
            source['londonResident'],
            source['numberOfFailedConsecutiveLogins'],
            source['person'],
            source['securityAnswer'],
            source['securityQuestion'],
            source['status'],
            source['tenantId'],
            source['webAccountId']
        )


def web_account_from_json(source: Dict[str, Any]):
    keys = source.keys()
    if 'borough' in keys:
        return WebAccountSettings.from_json(source)
    elif 'personId' in keys:
        return Person.from_json(source)


@dataclasses.dataclass
class Expiry:
    def __post_init__(self) -> None:
        self.expiry = datetime.datetime.now() + datetime.timedelta(seconds=self.expiry_after)
        self.check_expiry = datetime.datetime.now() + datetime.timedelta(seconds=self.check_expiry_after)

    check_expiry_after: int
    expiry_after: int

    @staticmethod
    def from_json(source: Dict[str, Any]):
        return Expiry(
            source['checkExpiryAfter'],
            source['expiryAfter']
        )


def generate_cursed_novacroft_uuid():
    # This function was generated entirely by ChatGPT - i have no idea what it does, but it comes from TfL's
    # frontend: ApiService#generateUUID()
    now = int(time.time() * 1000)

    if hasattr(time, 'perf_counter_ns'):
        now += time.perf_counter_ns() // 1000000

    def replace_char(match):
        if match.group(0) == 'x':
            return f'{random.randint(0, 15):x}'
        elif match.group(0) == 'y':
            return f'{random.randint(8, 11):x}'

    return re.sub('[xy]', replace_char, 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx')


class PhotocardAuthenticationRequiredException(Exception):
    def __str__(self):
        return "This method requires authentication"


class PhotocardServiceException(Exception):
    def __init__(self, response):
        self.response = response
        super().__init__(str(self))

    def __str__(self) -> str:
        return f"Expected HTTP 200, got HTTP {self.response.status}. ({self.response.geturl()})"


class PhotocardService:
    def __init__(self, session: PhotocardSession = None, client: urllib3.PoolManager = None,
                 base_url: str = "https://photocard-api.tfl.gov.uk/v1/") -> None:
        if client is None:
            client = urllib3.PoolManager()

        self.client = client
        self.base_url = base_url
        self.session = session
        self.transaction_reference = None
        self.security_token = None

    def _generate_headers(self) -> Dict[str, str]:
        headers = {
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0",
            "novacroft-global-transaction-reference": self.transaction_reference,
            "novacroft-operator-uuid": "undefined",
            "novacroft-security-token": '',
            "novacroft-tenant-id": 100000,
            "novacroft-web-account-id": ''
        }
        if self.session is not None:
            headers["novacroft-security-token"] = self.session.session_token
            headers["novacroft-web-account-id"] = self.session.web_account_id
        return headers

    def logon(self, email: str, password: str) -> None:
        """
        Logs onto the photocard service. Required for other API calls.
        Raises PhotocardServiceException with HTTP 500 if password is invalid.
        No known rate limits.

        :param email: Email to log on with
        :param password: Password to log on with
        :return:
        """
        self.transaction_reference = generate_cursed_novacroft_uuid()

        body = json.dumps({
            "email": email,
            "password": password
        })

        response: urllib3.HTTPResponse = self.client.request('POST', self.base_url + "logon", body=body,
                                                             headers=self._generate_headers())
        if response.status == 200:
            self.session = json.loads(response.data, object_hook=PhotocardSession.from_json)
        else:
            raise PhotocardServiceException(response)

    def get_people(self) -> List[Person]:
        """
        Gets people associated with this account
        :return: A list of Person objects representing people associated with the account id
        """
        if self.session is None:
            raise PhotocardAuthenticationRequiredException()
        response: urllib3.HTTPResponse = self.client.request('GET', self.base_url + "webAccount/people",
                                                             headers=self._generate_headers())
        if response.status == 200:
            return json.loads(response.data, object_hook=_person_from_json)
        else:
            raise PhotocardServiceException(response)

    def cards_for_person(self, person: int or Person) -> List[Card]:
        """
        Get the cards associated with the person
        :param person: PersonID or Person object
        :return: list of cards associated with the provided person
        """
        if self.session is None:
            raise PhotocardAuthenticationRequiredException()

        if isinstance(person, Person):
            person: int = person.person_id

        response: urllib3.HTTPResponse = self.client.request('GET', self.base_url + "cards/" + str(person),
                                                             headers=self._generate_headers())
        if response.status == 200:
            return json.loads(response.data, object_hook=_card_from_json)
        else:
            raise PhotocardServiceException(response)

    def web_account_settings(self) -> WebAccountSettings:
        """
        Get the web account settings. Side effect of extending the session.
        :return: A WebAccountSettings object.
        """
        if self.session is None:
            raise PhotocardAuthenticationRequiredException()

        # https://photocard-api.tfl.gov.uk/v1/webAccount/6215536
        response: urllib3.HTTPResponse = self.client.request('GET', self.base_url + "webAccount/" + str(
            self.session.web_account_id), headers=self._generate_headers())
        if response.status == 200:
            return json.loads(response.data, object_hook=web_account_from_json)
        else:
            raise PhotocardServiceException(response)

    def extend_session(self) -> None:
        """
        Renew the session. Calls web_account_settings
        :return:
        """
        self.web_account_settings()

    def check_session_expiry(self) -> Expiry:
        """
        Check when the session expires. The TfL frontend runs this every minute.
        :return: Expiry object
        """
        if self.session is None:
            raise PhotocardAuthenticationRequiredException()

        response: urllib3.HTTPResponse = self.client.request('GET', self.base_url + "webAccount/session/expiry",
                                                             headers=self._generate_headers())
        if response.status == 200:
            return json.loads(response.data, object_hook=Expiry.from_json)
        else:
            raise PhotocardServiceException(response)
