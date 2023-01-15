class ProductionConfig:
    """ statistics db config """
    url = 'db'
    port = 3306
    login = 'dbuser'
    password = 'dbpassword'
    db = 'test_task'


class DebugDBConfig(ProductionConfig):
    """ debug statistics db config """
    url = '192.168.0.204'
    login = 'dbuser'
    password = 'dbpassword'
    db = 'db'
