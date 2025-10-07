# Superset Day 2 Setup

```
docker compose build --no-cache superset
```

```
docker compose up --build
```

```
docker exec -it superset_mysql bash
```

# now inside container shell:


# connect as root

```
mysql -uroot -pmysql_root_pass
```

Once in the mysql> prompt you can run:

```sql
SHOW DATABASES;
USE tpch;
SHOW TABLES;
SELECT COUNT(*) FROM <table_name>;
```

```
CREATE DATABASE IF NOT EXISTS tpch;
USE tpch;
```

```
CREATE TABLE IF NOT EXISTS nations (
  n_nationkey INT NOT NULL PRIMARY KEY,
  n_name VARCHAR(25) NOT NULL,
  n_regionkey INT NOT NULL,
  n_comment VARCHAR(152)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

```
LOAD DATA INFILE '/tpch_csv/nations.csv'
INTO TABLE nations
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(n_nationkey, n_name, n_regionkey, n_comment);
```

```
CREATE TABLE IF NOT EXISTS regions (
  r_regionkey INT NOT NULL PRIMARY KEY,
  r_name VARCHAR(25) NOT NULL,
  r_comment VARCHAR(152)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

```
LOAD DATA INFILE '/tpch_csv/regions.csv'
INTO TABLE regions
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '\"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(r_regionkey, r_name, r_comment);
```

```
SELECT COUNT(*) AS rows_imported FROM regions;
SELECT * FROM regions;
```

```
CREATE TABLE IF NOT EXISTS suppliers (
  s_suppkey INT NOT NULL PRIMARY KEY,
  s_name VARCHAR(100) NOT NULL,
  s_address VARCHAR(200),
  s_nationkey INT,
  s_phone VARCHAR(30),
  s_acctbal DECIMAL(15,2),
  s_comment VARCHAR(300)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```
```
LOAD DATA INFILE '/tpch_csv/suppliers.csv'
INTO TABLE suppliers
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '\"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(s_suppkey, s_name, s_address, s_nationkey, s_phone, s_acctbal, s_comment);
```

```
SELECT COUNT(*) AS rows_imported FROM suppliers;
SELECT * FROM suppliers LIMIT 10;
```


```
CREATE TABLE IF NOT EXISTS customers (
  c_custkey INT NOT NULL PRIMARY KEY,
  c_name VARCHAR(50) NOT NULL,
  c_address VARCHAR(200),
  c_nationkey INT,
  c_phone VARCHAR(30),
  c_acctbal DECIMAL(15,2),
  c_mktsegment VARCHAR(20),
  c_comment VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

```
LOAD DATA INFILE '/tpch_csv/customers.csv'
INTO TABLE customers
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '\"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment);
```

```
SELECT COUNT(*) AS rows_imported FROM customers;

SELECT * FROM customers LIMIT 10;
```
```
CREATE TABLE IF NOT EXISTS parts (
  p_partkey INT NOT NULL PRIMARY KEY,
  p_name VARCHAR(120),
  p_mfgr VARCHAR(40),
  p_brand VARCHAR(20),
  p_type VARCHAR(40),
  p_size INT,
  p_container VARCHAR(20),
  p_retailprice DECIMAL(15,2),
  p_comment VARCHAR(200)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

```
LOAD DATA INFILE '/tpch_csv/parts.csv'
INTO TABLE parts
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '\"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(p_partkey, p_name, p_mfgr, p_brand, p_type, p_size, p_container, p_retailprice, p_comment);
```
```
SELECT COUNT(*) AS rows_imported FROM parts;
SELECT * FROM parts LIMIT 10;
```
```
CREATE TABLE IF NOT EXISTS parts_suppliers (
  ps_partkey INT NOT NULL,
  ps_suppkey INT NOT NULL,
  ps_availqty INT,
  ps_supplycost DECIMAL(15,2),
  ps_comment VARCHAR(300),
  PRIMARY KEY (ps_partkey, ps_suppkey)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

```
LOAD DATA INFILE '/tpch_csv/parts_suppliers.csv'
INTO TABLE parts_suppliers
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '\"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(ps_partkey, ps_suppkey, ps_availqty, ps_supplycost, ps_comment);
```

```
SELECT COUNT(*) AS rows_imported FROM parts_suppliers;
SELECT * FROM parts_suppliers LIMIT 10;
```
```
CREATE TABLE IF NOT EXISTS orders (
  o_orderkey INT NOT NULL PRIMARY KEY,
  o_custkey INT NOT NULL,
  o_orderstatus CHAR(1),
  o_totalprice DECIMAL(15,2),
  o_orderdate DATE,
  o_orderpriority VARCHAR(20),
  o_clerk VARCHAR(40),
  o_shippriority INT,
  o_comment VARCHAR(512)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

```
LOAD DATA INFILE '/tpch_csv/orders.csv'
INTO TABLE orders
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '\"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(o_orderkey, o_custkey, o_orderstatus, o_totalprice, o_orderdate, o_orderpriority, o_clerk, o_shippriority, o_comment);
```
```
SELECT COUNT(*) AS rows_imported FROM orders;
SELECT * FROM orders LIMIT 10;
```

```
CREATE TABLE IF NOT EXISTS lineitems (
  l_orderkey    INT NOT NULL,
  l_partkey     INT NOT NULL,
  l_suppkey     INT NOT NULL,
  l_linenumber  SMALLINT NOT NULL,
  l_quantity    DECIMAL(15,2),
  l_extendedprice DECIMAL(15,2),
  l_discount    DECIMAL(5,4),
  l_tax         DECIMAL(5,4),
  l_returnflag  CHAR(1),
  l_linestatus  CHAR(1),
  l_shipdate    DATE,
  l_commitdate  DATE,
  l_receiptdate DATE,
  l_shipinstruct VARCHAR(25),
  l_shipmode     VARCHAR(10),
  l_comment      VARCHAR(200),
  PRIMARY KEY (l_orderkey, l_linenumber)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

```
LOAD DATA INFILE '/tpch_csv/lineitems.csv'
INTO TABLE lineitems
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '\"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(l_orderkey, l_partkey, l_suppkey, l_linenumber, l_quantity, l_extendedprice, l_discount, l_tax, l_returnflag, l_linestatus, l_shipdate, l_commitdate, l_receiptdate, l_shipinstruct, l_shipmode, l_comment);
```

```
SELECT COUNT(*) AS rows_imported FROM lineitems;
```

```
docker exec -i superset_mysql bash 
```

-- create user if not exists and set password

```
CREATE USER IF NOT EXISTS 'tpchuser'@'%' IDENTIFIED BY 'tpch_pass';
CREATE USER IF NOT EXISTS 'tpchuser'@'localhost' IDENTIFIED BY 'tpch_pass';

-- grant full privileges on the tpch database (safer than global)
GRANT ALL PRIVILEGES ON tpch.* TO 'tpchuser'@'%' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON tpch.* TO 'tpchuser'@'localhost' WITH GRANT OPTION;

-- if you truly want global privileges (not recommended for prod), uncomment:
-- GRANT ALL PRIVILEGES ON *.* TO 'tpchuser'@'%' WITH GRANT OPTION;

FLUSH PRIVILEGES;
SHOW GRANTS FOR 'tpchuser'@'%';
SHOW GRANTS FOR 'tpchuser'@'localhost';
```





 
-- =====================
--  INDEXES FOR ANALYTICS
-- =====================
```
CREATE INDEX idx_nations_regionkey       ON nations(n_regionkey);
CREATE INDEX idx_suppliers_nationkey     ON suppliers(s_nationkey);
CREATE INDEX idx_customers_nationkey     ON customers(c_nationkey);
CREATE INDEX idx_orders_custkey          ON orders(o_custkey);
CREATE INDEX idx_lineitems_orderkey      ON lineitems(l_orderkey);
CREATE INDEX idx_lineitems_partkey       ON lineitems(l_partkey);
CREATE INDEX idx_lineitems_suppkey       ON lineitems(l_suppkey);
CREATE INDEX idx_lineitems_shipdate      ON lineitems(l_shipdate);
```

 
Data files here

Shall be shared via chat

```
sudo apt install unzip

unzip tpch_csv.zip -d tpch_csv

ls tpch_csv
```


