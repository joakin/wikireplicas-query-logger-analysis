from typing import Set, List, Dict, Optional, TypeVar
import re
import csv
import time
import subprocess
import json

def get_csv(path: str) -> List[Dict[str, str]]:
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        queries = [query for query in reader]
        return queries

T = TypeVar('T')
def unwrap_optional(opt: Optional[T]) -> T:
    if opt is None:
        raise TypeError(f"Unexpected attempt to unwrap {opt}")
    else:
        return opt

def main() -> None:
    queries = [row for row in get_csv('joaquin/multiuserqueriesstripped.csv')]

    users_set = set([row['user'] for row in queries])

    ids = ""
    for user in users_set:
        id = re.sub(r'^(s|u)', '', user)
        ids += f"(uidNumber={id})"

    print(f"{len(users_set)} unique users doing multi DB queries")

    query_process = subprocess.run(
        ["/bin/bash", "-c", f"ssh labweb1001.wikimedia.org \"ldapsearch -o ldif-wrap=no -x '(|{ids})' uidNumber uid cn\""],
        text=True,
        capture_output=True
    )

    print(query_process.stderr)

    raw_results = query_process.stdout.split('\n\n')[1:-2]

    users : Dict[str, Dict[str, str]] = {}
    for result in raw_results:
        try:
            uid_number = unwrap_optional(re.search(r'^uidNumber: (.+)$', result, flags=re.MULTILINE)).group(1)
            cn = unwrap_optional(re.search(r'^cn: (.+)$', result, flags=re.MULTILINE)).group(1)
            uid = unwrap_optional(re.search(r'^uid: (.+)$', result, flags=re.MULTILINE)).group(1)
            id = ('s' if uid.startswith('tools.') else 'u') + uid_number
            users[id] = {
                "cn": cn,
                "uid_number": uid_number,
                "uid": uid,
                "id": id,
            }
        except Exception as e:
            print(e)
            print(result)

    with open('joaquin/user-data.json', 'w') as user_data_file:
        user_data_file.write(json.dumps(users, indent=2))


if __name__ == "__main__":
    main()
