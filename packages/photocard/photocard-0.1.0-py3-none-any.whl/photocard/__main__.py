from photocard import PhotocardService

photocard = PhotocardService()
photocard.logon(input("Enter email: "), input("Enter password: "))
print("loading cards...")
people = photocard.get_people()
cards = dict()
for person in people:
    print(f"Cards for {person.forenames} {person.middle_name} {person.surname}:")
    for card in photocard.cards_for_person(person):
        print(f"  Card Number: {card.oyster_card_number}    Expiry: {card.expiry_date.strftime('%d/%m/%Y')}")
        print(f"  Card Type: {card.card_type.value}     Status: {card.card_status.value}")
        print(f"    Credit: £{card.prepaid_balance:.2f}")
        print(f"    Tickets ({len(card.tickets)}):")
        for ticket in card.tickets:
            print(
                f"      {ticket.product} {ticket.zone} "
                f"({ticket.start_date.strftime('%d/%m/%Y')} - {ticket.expiry_date.strftime('%d/%m/%Y')})")

print("done.")
