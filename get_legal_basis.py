import csv, requests

private_app_token = "abc123"
subscription_type_id = "4833949"

headers = {"Authorization":"Bearer " + private_app_token,
           'Content-Type': "application/json"}

output_dict = []

with open("email_list.csv", newline="") as f:
    reader = csv.reader(f)
    counter = 0
    for row in reader:
        counter += 1
        if counter % 1000 == 0:
            print("progress update: " + str(counter) + " contacts processed...")
        try:
            url = "https://api.hubapi.com/communication-preferences/v3/status/email/" + row[0]
            r = requests.get(url, headers=headers)
            statuses = r.json()
            if "subscriptionStatuses" in statuses:
                statuses = statuses["subscriptionStatuses"]
                for status in statuses:
                    if str(status["id"]) == str(subscription_type_id):
                        if "legalBasis" in status:
                            if status["legalBasis"]:
                                output_dict.append([row[0], status["legalBasis"]])
                if not r:
                    print("could not fetch the communication preferences of " + row[0])
        except ValueError:
            print("could not process this row: " + str(row))

                                            
with open('legal_basis.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(output_dict)
