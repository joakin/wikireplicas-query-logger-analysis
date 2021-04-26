from typing import Set, List, Dict, Any
import re
import csv
import time
import json

def get_csv(path: str) -> List[Dict[str, Any]]:
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        queries = [query for query in reader]
        return queries

def get_users_json(path: str) -> Dict[str, Dict[str, str]]:
    with open(path) as file:
        return json.load(file) # type: ignore


def sort_rows(row: Dict[str, str]) -> Any:
    return (row['user'], row['query_stripped'], row['db'], row['dbs'])


def main() -> None:
    queries = get_csv('joaquin/multiuserqueriesstripped.csv')

    queries.sort(key=sort_rows)

    users = get_users_json('joaquin/user-data.json')

    for query in queries:
        query['user'] = users[query['user']]

    html = """
<style>
    table {
        table-layout: fixed;
        width: 100%;  
    }
    td {
        word-break: break-word;
        vertical-align: top;
    }
    pre {
        max-width: 100%;
        max-height: 500px;
        word-break: break-word;
        overflow-y: auto;
    }
</style>
<table><thead><tr>
<th style="width: 150px;">db</th>
<th style="width: 150px;">dbs</th>
<th style="width: 150px;">user</th>
<th style="">query_stripped</th>
<th style="">query</th>
</tr></thead><tbody>
"""

    for row in queries:
        # "host","user","db","query","date","time","dbs"
        html += f"""
<tr>
<td>{row['db']}</td>
<td>{row['dbs']}</td>
<td>{row['user']['cn']} ({row['user']['id']})</td>
<td><pre>{row['query_stripped']}</pre></td>
<td><pre>{row['query']}</pre></td>
</tr>
"""
    html += "</tbody></table>"

    with open("joaquin/report.html", "w") as report:
        report.write(html)

if __name__ == "__main__":
    main()
