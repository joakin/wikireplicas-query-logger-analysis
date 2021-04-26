from typing import Set, Pattern, Any, List, Dict, Tuple
import re
import csv
import time

def get_csv(path: str) -> List[Dict[str, str]]:
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        queries = [query for query in reader]
        return queries

def main() -> None:
    queries = get_csv('brooke/userqueries.csv')

    multiqueries = set()
    for row in get_csv('joaquin/multiuserqueries.csv'):
        multiqueries.add(row['query'])

    tally = 0
    for row in queries:
        q = row['query']
        if q in multiqueries:
            tally += 1

    print(f"Found {tally} multi DB queries from all {len(queries)} queries")

if __name__ == "__main__":
    main()
