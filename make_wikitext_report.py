from typing import Set, List, TypedDict, Dict, Any, Tuple, Union
import re
import csv
import time
import json
from pprint import pp

def get_csv(path: str) -> List[Dict[str, Any]]:
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        queries = [query for query in reader]
        return queries

def get_users_json(path: str) -> Dict[str, Dict[str, str]]:
    with open(path) as file:
        return json.load(file) # type: ignore


def sort_rows(row: Dict[str, Any]) -> Any:
    return (row['user'], row['query_stripped'], row['db'], row['dbs'])

def key_and_sorted_dbs(dbs: str) -> Tuple[str, List[str]]:
    dbs_list = sorted(dbs.split(','))
    return ', '.join(dbs_list), dbs_list

def main() -> None:
    queries = get_csv('joaquin/multiuserqueriesstripped.csv')

    queries.sort(key=sort_rows)

    users = get_users_json('joaquin/user-data.json')

    for query in queries:
        # "host","user","db","query","query_stripped""date","time","dbs"
        query['user'] = users[query['user']]
    
    queries_by_user: Dict[str, Any] = {}
    for row in queries:
        key = row['user']['cn']
        if key not in queries_by_user:
            queries_by_user[key] = {'queries': [], 'dbs': {}}
        stats = queries_by_user[key]

        stats['queries'].append(row)

        dbs, dbs_list = key_and_sorted_dbs(row['dbs'])
        stats['dbs'][dbs] = stats['dbs'].get(dbs, 0) + 1


    queries_by_normalized: Dict[str, Any] = {}
    for row in queries:
        key = row['query_stripped']
        if key in queries_by_normalized:
            q = queries_by_normalized[key]
        else:
            q = row.copy()
            q['queries'] = []
            queries_by_normalized[key] = q
        q['queries'].append(row['query'])

    db_stats = {}
    for query_normalized, query in queries_by_normalized.items():
        dbs, dbs_list = key_and_sorted_dbs(query['dbs'])
        if dbs not in db_stats:
            db_stats[dbs] = {'queries': [], 'dbs': dbs_list}
        stats = db_stats[dbs]
        stats['queries'].append(query)

    out = ""
    def add_line(s: str) -> None:
        nonlocal out
        out += s + "\n"

    db_stats_sorted_by_usage = sorted(db_stats.items(), key=lambda x: -len(x[1]['queries'])) # type: ignore

    add_line("""===DBs queried together, with frequencies and users===
{| class="wikitable mw-collapsible" style="table-layout: fixed; max-width: 100%; overflow-x: auto"
! style='width: 240px;' | DBs joined
! style='width: 100px;' | Unique normalized queries
!Tools/Users""")
    for db, stats in db_stats_sorted_by_usage:
        add_line("|-")
        add_line(f"| style='vertical-align: top;' | <div style='max-height: 100px; overflow-y: auto; word-break: break-all;'>{db}</div>")
        add_line(f"| style='vertical-align: top;' | {len(stats['queries'])}")
        tools = set([f"{row['user']['cn']} ({row['user']['id']})" for row in stats['queries']])
        add_line(f"| style='vertical-align: top;' | {', '.join(tools)}")
        # print(f"{db}: {len(stats['queries'])}")
    add_line("|}")

    add_line("""===Tools/Users' number of cross-DB queries performed, and DBs queried===
{| class="wikitable mw-collapsible" style="table-layout: fixed; max-width: 100%; overflow-x: auto"
! style='width: 100px;' | Tool/User
! style='width: 200px;' | Number of queries
!DBs queried""")
    queries_by_user_sorted = sorted(queries_by_user.items(), key=lambda x: -len(x[1]['queries']))
    for user_cn, row in queries_by_user_sorted:
        add_line("|-")
        add_line(f"| style='vertical-align: top;' | {user_cn}")
        unique_normalized = set([query['query_stripped'] for query in row['queries']])
        add_line(f"| style='vertical-align: top;' | \n*Unique normalized: {len(unique_normalized)}\n*Unique: {len(row['queries'])}")
        add_line(f"| style='vertical-align: top;' | ")
        
        sorted_dbs = sorted(row['dbs'].items(), key=lambda x: -x[1]) # type: ignore
        for dbs, n in sorted_dbs:
            add_line(f"* ({n}) <div style='display: inline-block; max-width: 300px; overflow-x: auto; white-space: nowrap;'>{dbs}</div>")
    add_line("|}")

    print(out)
    with open("joaquin/report.wiki", "w") as report:
        report.write(out)

if __name__ == "__main__":
    main()
