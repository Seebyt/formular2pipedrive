from pipedrive.client import Client
from imap_tools import MailBox, Q
from time import sleep


client = Client(domain='client.domain')
client.set_api_token('apitoken')

data_list = []


def main():
    username = "client.email"
    password = "email.password"

    with MailBox('imap.strato.de').login(username, password) as mailbox:
        # lese ungelesene emails aus postfach
        for msg in mailbox.fetch(Q(seen=False)):
            mail = msg.text
            for line in mail.splitlines():
                data_list.append(line)

            data_list.pop()

            title = data_list[0].split(":")[1]

            anrede = data_list[1].split(":")[1]

            fullname = data_list[2].split(":")[1]
            phone = data_list[3].split(":")[1]
            email = data_list[4].split(":")[1]
            plz = data_list[5].split(":")[1]

            standorte = data_list[6].split(":")[1]
            if standorte == "ein-standort":
                standorte = "Einzelner Standort"
            else:
                standorte = "Mehrere Standorte"

            art_des_standortes = data_list[7].split(":")[1]
            if art_des_standortes == "buero":
                art_des_standortes = "Buero"

            elif art_des_standortes == "praxis-klinik":
                art_des_standortes = "Praxis"

            else:
                art_des_standortes = art_des_standortes.capitalize()

            frequenz = data_list[8].split(":")[1]
            if frequenz == "taeglich":
                frequenz = "Täglich"

            elif frequenz == "2-3-mal-woechentlich":
                frequenz = "2-3 wöchentlich"

            else:
                frequenz = "Wöchentlich"


            # api requests
            # erstellt deal mit deal_id
            deal_title = {"title": f"{title}"}
            response = client.deals.create_deal(deal_title)
            print("Ein neuer Deal wurde erstellt.")

            deal_response = response["data"]
            deal_id = deal_response["id"]

            # erstellt eine organisation mit org_id
            org_data = {"name": f"{title}"}
            response = client.organizations.create_organization(org_data)
            print("Eine neue Organisation wurde registriert.")

            org_response = response["data"]
            org_id = org_response["id"]

            # erstellt einen Kontakt
            person_data = {"name": f"{fullname}",
                           "email": f"{email}",
                           "phone": f"{phone}"}
            response = client.persons.create_person(person_data)
            print("Ein neuer Kontakt wurde registriert.")

            person_response = response["data"]
            person_id = person_response["id"]

            person_update = {"8801a4c9d9526bad4ebffdc8d0344d95d3d814c3": f"{anrede}"}
            response = client.persons.update_person(person_id, person_update)


            # updatet den deal mit den anderen daten
            deal_data = {"plz api token": f"{plz}",
                         "standort api token": f"{standorte}",
                         "art des standorts api token": f"{art_des_standortes}",
                         "frequenz api token": f"{frequenz}",
                         "org_id api": f"{org_id}",
                         "person_id": f"{fullname}"}

            response = client.deals.update_deal(deal_id, deal_data)


counter = 0
while True:
    try:
        main()
        counter += 1
        if counter < 2:
            print(f"Es wurde 1 Pipedrive-Eintrag generiert.")
        else:
            print(f"Es wurden {counter} Pipedrive-Einträge generiert.")
    except:
        pass
    sleep(3600)

