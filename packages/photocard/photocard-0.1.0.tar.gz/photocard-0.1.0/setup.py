# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['photocard']

package_data = \
{'': ['*']}

install_requires = \
['urllib3>=1.26.15,<2.0.0']

setup_kwargs = {
    'name': 'photocard',
    'version': '0.1.0',
    'description': "A Pythonic interface for TfL's Photocard service",
    'long_description': '# photocard\n\nA Pythonic interface for TfL\'s Photocard service.\n\nTfL couldn\'t be bothered to add photocard support to their app, so I made an API for their photocard service in half a\nday.\nNot too difficult after all, huh?\n\n## Benefits\n\n* Full read access to TfL\'s Photocard service\n* 11-15 Photocard support\n\n## Limitations:\n\n* All API endpoints, require [logging on](#logon).\n* All API endpoints are read only\n* Limited support for 5-10, 16+, 18+, and 60+ photocards. If you need support for these please provide screenshots of\n  the\n  network inspector calling the card endpoint for these, please open an issue in the issues tab.\n\n## CLI\n\nA CLI tool is available.\n\n```\npython -m photocard\n```\n\n## Usage\n\n### Logon\n\nLogon requires email and password.\n\nTry not to get the password wrong - TfL has been known to lock you out of your account for 30 minutes if you get your\npassword wrong just once.\n\n### Example: Getting People & Cards\n\n```python\nfrom photocard import PhotocardService\n\nphotocard = PhotocardService()\nphotocard.logon(input("Enter email: "), input("Enter password: "))\n\n# Gets all people associated with the web account\npeople = photocard.get_people()\nfor person in people:\n    # Get cards for person\n    cards = photocard.cards_for_person(person)  # More than one card can be associated with a person\n    for card in cards:\n        print(f"Balance for card {card.oyster_card_number}: £{card.prepaid_balance:.2f}")\n        # Example output (censored PII): Balance for card 0*********5: £3.50\n```\n\n## Disclaimer\n\nThis doesn\'t appear to break any T&C, but I\'m not a lawyer, so get one to read TfL\'s:\nhttps://tfl.gov.uk/corporate/terms-and-conditions/\n',
    'author': 'Oskar',
    'author_email': '56176746+OskarZyg@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
