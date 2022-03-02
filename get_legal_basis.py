import csv, requests, json

private_app_token = "abc123"

headers = {"Authorization":"Bearer " + private_app_token,
           'Content-Type': "application/json"}

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
                    if status["id"] == "4833949":
                        if "legalBasis" in status:
                            if status["legalBasis"]:
                                print(row[0] + "," + status["legalBasis"])
                if not r:
                    print(row[0] + ",FETCH_ERROR")
        except ValueError:
            print("could not process this row: " + str(row))
