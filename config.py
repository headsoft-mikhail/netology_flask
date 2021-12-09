postgres_owner = 'postgres'
postgres_password = 'postgres'
postgres_host = 'localhost'
postgres_port = '5432'
postgres_db_name = 'flask_test'

POSTGRES_URI = f'postgresql://{postgres_owner}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db_name}'

SALT = 'my_example_SaLt'

SECRET_KEY = 'My_secreT'
EXPIRE_TIME = 600
