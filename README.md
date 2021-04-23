Scripts used for analysis in
[T280152 Mitigate breaking changes from the new Wiki Replicas architecture](https://phabricator.wikimedia.org/T280152)
and
[Wiki_Replicas_Cross-DB_Query_Data](https://wikitech.wikimedia.org/wiki/News/Wikireplicas_2020_Redesign/Wiki_Replicas_Cross-DB_Query_Data)
report.

Excuse my python, this is just getting the job done, not a production service.

Some files excluded from the repository for privacy reasons (like the original
data). Reach out if you need it.

## Setup

Generate an environment, and install dependencies before running the scripts.

```
source wikireplicas-queries-env/bin/activate
pip install -r requirements.txt
```

## Files in order

1. filter_multi_from_distinct_user_queries.py
1. how_many_multi_from_user_queries.py
1. distinct_user_queries_with_stripping.py
1. unique_queries_when_removing_literals.py
1. get_users_info.py
1. make_html_report.py
1. make_wikitext_report.py
1. make_csv_for_public_viewing.py

## Results

### filter_multi_from_distinct_user_queries.py

18758 (764 multi, 0.04797315691589915s per row)

Found 764 multi DB queries

### how_many_multi_from_user_queries.py

Found 2937 multi DB queries from all 60007 queries

### distinct_user_queries_with_stripping.py

3858 unique out of 18758

### unique_queries_when_removing_literals.py

169 unique multi DB queries out of 3858 unique queries

### get_users_info.py

See joaquin/user-data.json

### make_html_report.py

See joaquin/report.html

### make_wikitext_report.py

See joaquin/report.wiki

### make_csv_for_public_viewing.py

See joaquin/multiuserqueriesstrippedpublic.csv
