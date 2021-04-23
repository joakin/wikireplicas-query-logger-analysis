from typing import Set, List, Dict
import re
import csv
import time
import json

def get_csv(path: str) -> List[Dict[str, str]]:
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        queries = [query for query in reader]
        return queries


def get_users_json(path: str) -> Dict[str, Dict[str, str]]:
    with open(path) as file:
        return json.load(file)
 
def main():
    errors = []

    queries = get_csv('joaquin/multiuserqueriesstripped.csv')
    users = get_users_json('joaquin/user-data.json')

    for query in queries:
        query['user_cn'] = users[query['user']]['cn']

    with open("joaquin/multiuserqueriesstrippedpublic.csv", "w") as multi_file:
        fieldnames = ["user_cn", "user" , "db", "dbs", "query", "query_stripped"]
        writer = csv.DictWriter(multi_file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL, extrasaction='ignore')
        writer.writeheader()

        for row in queries:
            try:
                writer.writerow(row)
            except Exception as e:
                print(e)
                print("oops")
                print(row)
                errors.append({ "error": e, "row": row })

    for error in errors:
        print(error["error"])
        print(error["row"])

if __name__ == "__main__":
    main()
