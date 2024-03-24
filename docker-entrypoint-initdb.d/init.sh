set -e

psql -v ON_ERROR_STOP=1 --username "${POSTGRES_USER}" <<-EOSQL
  CREATE DATABASE flask_products;
  CREATE DATABASE flask_orders;
  CREATE DATABASE flask_users;
EOSQL


echo "hello workd *****"