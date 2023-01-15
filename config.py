class ProductionConfig:
    """ statistics db config """
    url = '127.0.0.1'
    port = 3306
    login = 'login'
    password = 'password'
    db = 'statistics'


class DebugDBConfig(ProductionConfig):
    """ debug statistics db config """
    url = 'pacs'
    login = 'dbuser'
    password = 'dbpassword'
    db = 'test_task'
