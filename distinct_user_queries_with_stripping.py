from typing import Set, List, Dict
import re
import csv
import time

def get_csv(path: str) -> List[Dict[str, str]]:
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        queries = [query for query in reader]
        return queries

double_quote_string_literals = re.compile(r"\".+?\"", flags=re.MULTILINE)
single_quote_string_literals = re.compile(r"\'.+?\'", flags=re.MULTILINE)
digits = re.compile(r'\d+', flags=re.MULTILINE) 

def strip_query(q: str) -> str:
    s = q
    s = double_quote_string_literals.sub(r'?', s)
    s = single_quote_string_literals.sub(r"?", s)
    s = digits.sub(r"0", s)
    return s
 
def main():
    errors = []

    queries = get_csv('brooke/distinctuserqueries.csv')

    unique_queries = set()

    tally = 0

    for row in queries:
        tally += 1

        # if tally == 5:
        #     break

        # "host","user","db","query","date","time"
        row["query_stripped"] = strip_query(row["query"])
        unique_queries.add(row["query_stripped"])


    with open("joaquin/distinctuserqueriesstripped.csv", "w") as multi_file:
        fieldnames = ["host","user","db","query","query_stripped","date","time"]
        writer = csv.DictWriter(multi_file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
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

    print(f"{len(unique_queries)} unique out of {len(queries)}")

if __name__ == "__main__":
    main()
