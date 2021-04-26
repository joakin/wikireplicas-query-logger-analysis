from typing import Set, Pattern, Any, List, Dict, Tuple
import re
import csv
import time

import sqlparse # type: ignore

def get_csv(path: str) -> List[Dict[str, str]]:
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        queries = [query for query in reader]
        return queries

 
db_patterns = ["centralauth", "meta_p"]


def get_dbs_from_parsed_query_sqlparse(db: str, token_list: Any, regex: Pattern[str]) -> Set[str]:
    dbs = set()
    for token in token_list.tokens:
        if isinstance(token, sqlparse.sql.Identifier) and "." in token.value:
            if token.value.split(".")[0] in db_patterns or regex.match(
                token.value.split(".")[0]
            ):
                dbs.add(token.value.split(".")[0])
                # print(f"1  {token}")
        elif isinstance(token, sqlparse.sql.Identifier) and (
            regex.match(token.value) or token.value in db_patterns
        ):
            dbs.add(token.value)
            # print(f"2  {token}")
        elif isinstance(token, sqlparse.sql.TokenList):
            # print(f"TokenList: {isinstance(token, sqlparse.sql.TokenList)}")
            dbs = dbs.union(get_dbs_from_parsed_query_sqlparse(db, token, regex))
        else:
            pass
    return dbs


def is_cross_database(db: str, sql: str, regex: Pattern[str]) -> Tuple[bool, Set[str]]:
    parsed_queries = sqlparse.parse(sql, "utf-8")
    dbs: Set[str] = set()
    if db.strip():
        dbs.add(db)
    for parsed_query in parsed_queries:
        statement_dbs = get_dbs_from_parsed_query_sqlparse(db, parsed_query, regex)
        dbs = dbs | statement_dbs

    return len(dbs) > 1, dbs


def main() -> None:
    wikidb = re.compile(r"[a-z]+wik.*_p")

    queries = get_csv('brooke/distinctuserqueries.csv')
    cross_joins = []
    errors = []
    tally = 0
    found = 0
    start = time.time()
    for row in queries:
        tally += 1
        # "host","user","db","query","date","time"
        try:
            is_multi, dbs = is_cross_database(row["db"], row["query"], wikidb)
        except Exception as e:
            is_multi = False
            print(e)
            print("oops")
            print(row)
            errors.append({ "error": e, "row": row })

        if is_multi:
            found += 1
            row["dbs"] = ",".join(dbs)
            cross_joins.append(row)

        end = time.time()
        print(f"{tally} ({found} multi, {(end - start) / tally}s per row)")

        # if tally > 100:
        #     break

    print(f"Found {len(cross_joins)} multi DB queries")

    with open("joaquin/multiuserqueries.csv", "w") as multi_file:
        fieldnames = ["host","user","db","query","date","time","dbs"]
        writer = csv.DictWriter(multi_file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()

        for row in cross_joins:
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
