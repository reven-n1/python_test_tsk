<h1>Test task</h1>
<h3>Simple REST application powered by fastapi with data validation, db CRUD ...</h3>


<b>local run</b>
```html
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements/development.txt
```

<b>run with docker-compose</b>
```html
docker-compose up -d --build
```

<b>run test</b>
```html
docker-compose exec python_service pytest tests/test_statistics.py
```

<h3>Endpoints</h3>
<b>all other documentation provided by swagger ui (.../docs)</b>
```html
- save stats
curl -X POST http://url:port/statistics/stats -H "Content-Type: application/json" -d '{ "date" : "2023-01-09", "views": 1, "clicks" : 12, "cost": 13.00 }'

- get stats
curl -X GET http://url:port/statistics/stats?start_date=2023-01-01&end_date=2023-01-12&order_by=date

- reset stats
curl -X DELETE http://url:port/statistics/stats
```


<b>for generating models by existing bd schema(if needed)</b>
```html
sqlacodegen  --outfile src/statistics/db_models.py  mysql://user:password@server_url:port/schema
```

<b>create schema and table</b>
```sql
create database if not exists test_task;

use test_task;

create table if not exists statistics
(
    id     int auto_increment
        primary key,
    date   date                        not null comment 'event date',
    views  int            default 0    not null comment 'views num',
    clicks int            default 0    not null comment 'clicks num',
    cost   decimal(19, 2) default 0.00 not null comment 'click cost'
);
```