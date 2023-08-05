# photocard

A Pythonic interface for TfL's Photocard service.

TfL couldn't be bothered to add photocard support to their app, so I made an API for their photocard service in half a
day.
Not too difficult after all, huh?

## Benefits

* Full read access to TfL's Photocard service
* 11-15 Photocard support

## Limitations:

* All API endpoints, require [logging on](#logon).
* All API endpoints are read only
* Limited support for 5-10, 16+, 18+, and 60+ photocards. If you need support for these please provide screenshots of
  the
  network inspector calling the card endpoint for these, please open an issue in the issues tab.

## CLI

A CLI tool is available.

```
python -m photocard
```

## Usage

### Logon

Logon requires email and password.

Try not to get the password wrong - TfL has been known to lock you out of your account for 30 minutes if you get your
password wrong just once.

### Example: Getting People & Cards

```python
from photocard import PhotocardService

photocard = PhotocardService()
photocard.logon(input("Enter email: "), input("Enter password: "))

# Gets all people associated with the web account
people = photocard.get_people()
for person in people:
    # Get cards for person
    cards = photocard.cards_for_person(person)  # More than one card can be associated with a person
    for card in cards:
        print(f"Balance for card {card.oyster_card_number}: £{card.prepaid_balance:.2f}")
        # Example output (censored PII): Balance for card 0*********5: £3.50
```

## Disclaimer

This doesn't appear to break any T&C, but I'm not a lawyer, so get one to read TfL's:
https://tfl.gov.uk/corporate/terms-and-conditions/
