from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

headers = {"Content-Type": "application/json", "Cookie": "key=first-value"}


def test_creation_all_params():
    body = {"date": "2023-01-14", "views": 100, "clicks": 100, "cost": 100.00}
    response = client.post("statistics/stats", json=body, headers=headers)
    assert response.status_code == 201


def test_creation_only_required():
    body = {"date": "2023-01-15"}
    response = client.post("statistics/stats", json=body, headers=headers)
    assert response.status_code == 201


def test_creation_without_required():
    body = {"views": 7, "clicks": 9, "cost": 8.34}
    response = client.post("statistics/stats", json=body, headers=headers)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "date"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }


def test_creation_with_invalid_data():
    body = {"date": "2023-01-09", "views": -1, "clicks": "asd", "cost": 15.00}
    response = client.post("statistics/stats", json=body, headers=headers)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "views"
                ],
                "msg": "views value must be >= 0, current -1",
                "type": "value_error"
            },
            {
                "loc": [
                    "body",
                    "clicks"
                ],
                "msg": "value is not a valid integer",
                "type": "type_error.integer"
            }
        ]
    }


def test_get_stat():
    body = {"date": "2023-01-15", "views": 100, "clicks": 10, "cost": 10.00}
    client.post("statistics/stats", json=body, headers=headers)

    response = client.get("statistics/stats?start_date=2020-11-11&end_date=2025-11-11")
    assert response.status_code == 200
    assert response.json() == [
        {
            'date': '2023-01-14',
            'views': 100,
            'clicks': 100,
            'cost': 100.0,
            'cpc': 1.0,
            'cpm': 1000.0
        },
        {
            'date': '2023-01-15',
            'views': 100,
            'clicks': 10,
            'cost': 10.0,
            'cpc': 1.0,
            'cpm': 1000.0
        }
    ]


def test_get_stat_with_ordering():
    response = client.get("statistics/stats?start_date=2020-11-11&end_date=2025-11-11&order_by=clicks")
    assert response.status_code == 200
    assert response.json() == [
        {
            'date': '2023-01-15',
            'views': 100,
            'clicks': 10,
            'cost': 10.0,
            'cpc': 1.0,
            'cpm': 1000.0
        },
        {
            'date': '2023-01-14',
            'views': 100,
            'clicks': 100,
            'cost': 100.0,
            'cpc': 1.0,
            'cpm': 1000.0
        }
    ]


def test_get_stat_with_ordering_invalid_column():
    response = client.get("statistics/stats?start_date=2023-01-01&end_date=2023-01-12&order_by=invalid_column")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "param - order_by",
                    "value - invalid_column"
                ],
                "msg": "non allowed filter field",
                "type": "value_error"
            }
        ]
    }


def test_get_stat_no_data_per_period():
    response = client.get("statistics/stats?start_date=2025-01-01&end_date=2026-01-12")
    assert response.status_code == 204


def test_reset_data():
    response = client.get("statistics/stats?start_date=2020-01-01&end_date=2025-01-12")
    assert response.status_code == 200
    response = client.delete("/statistics/stats")
    assert response.status_code == 200
    response = client.get("statistics/stats?start_date=2023-01-01&end_date=2023-01-12")
    assert response.status_code == 204
