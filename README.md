<h1>Test task</h1>
<h3>Simple REST application powered by fastapi with data validation, db CRUD ...</h3>


<b>devel installation</b>
```text
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements/development.txt
```

<b>configuration</b>
```text
config.py
u need to change ProductionConfig
```

<b>for generating models by existing bd schema</b>
```text
sqlacodegen  --outfile src/statistics/db_models.py  mysql://user:password@server_url:port/schema
```


<h3>Endpoints</h3>
```text
- save stats
curl -X POST http://url:port/statistics/stats -H "Content-Type: application/json" -d '{ "date" : "2023-01-09", "views": 1, "clicks" : 12, "cost": 13.00 }'

- get stats
curl -X GET http://url:port/statistics/stats?start_date=2023-01-01&end_date=2023-01-12&order_by=date

- reset stats
curl -X DELETE http://url:port/statistics/stats
```
