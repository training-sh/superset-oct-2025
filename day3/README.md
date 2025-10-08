```
docker exec -it superset_app superset load_examples
```
```
docker exec -it superset_mysql bash
```

# now inside container shell:
# connect as tpch user to tpch DB
```
mysql -uroot -pmysql_root_pass
```

-- yearly growth by region for line chart

-- Region-wise yearly sales and YoY growth (%)

```
use tpch;

WITH top_regions AS (
  SELECT
    r.r_regionkey,
    r.r_name,
    SUM(o.o_totalprice) AS total_sales_alltime
  FROM orders o
  JOIN customers c ON o.o_custkey = c.c_custkey
  JOIN nations n ON c.c_nationkey = n.n_nationkey
  JOIN regions r ON n.n_regionkey = r.r_regionkey
  WHERE o.o_orderdate >= '1990-01-01'
    AND o.o_orderdate <  '2014-01-02'
  GROUP BY r.r_regionkey, r.r_name
  ORDER BY total_sales_alltime DESC
  LIMIT 10
),

yearly_sales AS (
  SELECT
    r.r_regionkey,
    r.r_name AS region,
    YEAR(o.o_orderdate) AS year,
    MIN(MAKEDATE(YEAR(o.o_orderdate), 1)) AS __timestamp,  -- safe under ONLY_FULL_GROUP_BY
    SUM(o.o_totalprice) AS total_sales
  FROM orders o
  JOIN customers c ON o.o_custkey = c.c_custkey
  JOIN nations n ON c.c_nationkey = n.n_nationkey
  JOIN regions r ON n.n_regionkey = r.r_regionkey
  WHERE o.o_orderdate >= '1990-01-01'
    AND o.o_orderdate <  '2014-01-02'
    AND r.r_regionkey IN (SELECT r_regionkey FROM top_regions)
  GROUP BY r.r_regionkey, r.r_name, YEAR(o.o_orderdate)
)

SELECT
  __timestamp,
  year,                       -- included here for demo / readability
  region,
  total_sales,
  ROUND(
    100.0 * (total_sales - LAG(total_sales) OVER (PARTITION BY region ORDER BY year))
    / NULLIF(LAG(total_sales) OVER (PARTITION BY region ORDER BY year), 0),
    2
  ) AS yoy_growth_pct
FROM yearly_sales
ORDER BY region, year;

```

```

use tpch;

DROP TABLE IF EXISTS top_regions_ct;

CREATE TABLE top_regions_ct
ENGINE=InnoDB
AS
SELECT
  r.r_regionkey,
  r.r_name AS region,
  SUM(o.o_totalprice) AS total_sales_alltime
FROM orders o
JOIN customers c ON o.o_custkey = c.c_custkey
JOIN nations n ON c.c_nationkey = n.n_nationkey
JOIN regions r ON n.n_regionkey = r.r_regionkey
WHERE o.o_orderdate >= '1990-01-01'
  AND o.o_orderdate <  '2014-01-02'
GROUP BY r.r_regionkey, r.r_name
ORDER BY total_sales_alltime DESC
LIMIT 10;
```

```
SELECT count(*) from top_regions_ct;
SELECT *   from top_regions_ct LIMIT 5;
```

```
ALTER TABLE top_regions_ct ADD PRIMARY KEY (r_regionkey);
-- or if column name normalized:
ALTER TABLE top_regions_ct ADD INDEX idx_region (r_regionkey, region);
```

```
DROP TABLE IF EXISTS yearly_sales_ct;
```
```
CREATE TABLE yearly_sales_ct
ENGINE=InnoDB
AS
SELECT
  r.r_regionkey,
  r.r_name AS region,
  YEAR(o.o_orderdate) AS year,
  MIN(MAKEDATE(YEAR(o.o_orderdate), 1)) AS __timestamp,  -- safe aggregate
  SUM(o.o_totalprice) AS total_sales
FROM orders o
JOIN customers c ON o.o_custkey = c.c_custkey
JOIN nations n ON c.c_nationkey = n.n_nationkey
JOIN regions r ON n.n_regionkey = r.r_regionkey
WHERE o.o_orderdate >= '1990-01-01'
  AND o.o_orderdate <  '2014-01-02'
  AND r.r_regionkey IN (SELECT r_regionkey FROM top_regions_ct)
GROUP BY r.r_regionkey, r.r_name, YEAR(o.o_orderdate);
```
```
SELECT count(*) from yearly_sales_ct;

SELECT * from yearly_sales_ct LIMIT 5;
```
```
ALTER TABLE yearly_sales_ct ADD PRIMARY KEY (r_regionkey, year);
ALTER TABLE yearly_sales_ct ADD INDEX idx_region_year (region, year);
ALTER TABLE yearly_sales_ct ADD INDEX idx_timestamp (__timestamp);
```

-- only if you expect many years and very large rows
```
ALTER TABLE yearly_sales_ct
PARTITION BY RANGE (year) (
  PARTITION p1990 VALUES LESS THAN (2000),
  PARTITION p2000 VALUES LESS THAN (2010),
  PARTITION p2010 VALUES LESS THAN (2020),
  PARTITION pmax VALUES LESS THAN MAXVALUE
);
```

```
DROP TABLE IF EXISTS yearly_sales_yoy_ct;
```
```
CREATE TABLE yearly_sales_yoy_ct
ENGINE=InnoDB
AS
SELECT
  cur.r_regionkey,
  cur.region,
  cur.year,
  cur.__timestamp,
  cur.total_sales,
  CASE
    WHEN prev.total_sales IS NULL OR prev.total_sales = 0 THEN NULL
    ELSE ROUND(100.0 * (cur.total_sales - prev.total_sales) / prev.total_sales, 2)
  END AS yoy_growth_pct
FROM yearly_sales_ct cur
LEFT JOIN yearly_sales_ct prev
  ON cur.r_regionkey = prev.r_regionkey AND cur.year = prev.year + 1;
```

```
ALTER TABLE yearly_sales_yoy_ct ADD PRIMARY KEY (r_regionkey, year);
ALTER TABLE yearly_sales_yoy_ct ADD INDEX idx_region_ts (region, __timestamp);
```

now for superset dataset,


for superset dataset,
```
SELECT
  __timestamp AS __timestamp,   -- Superset expects a column named __timestamp or use this as the time column in dataset settings
  region,
  year,
  total_sales,
  yoy_growth_pct
FROM yearly_sales_yoy_ct
ORDER BY region, __timestamp;
```

Now if we look into, all the CTAS tables are part of Data Engineering Team, creating, updating, refreshing the tables are part of Data Engineering tasks. Tools & Frameworks like 
Apache Flink, Spark SQL, DataBricks, or other Dataware houses, Delta Tables, Delta Lakes, Delta Lakehouses are deployed for that purpose.

Create charts for world map, we don't have region marking so, the output is mean to particular country..

```
SELECT
  region,
  total_sales_alltime        AS total_sales,

  -- representative country ISO alpha-3 per region (one country per region)
  CASE
    WHEN UPPER(region) LIKE '%AMERICA%'      THEN 'USA'
    WHEN UPPER(region) LIKE '%ASIA%'         THEN 'CHN'
    WHEN UPPER(region) LIKE '%AFRICA%'       THEN 'EGY'
    WHEN UPPER(region) LIKE '%EUROPE%'       THEN 'GBR'
    WHEN UPPER(region) LIKE '%MIDDLE%' 
      OR UPPER(region) LIKE '%EAST%'         THEN 'SAU'
    ELSE NULL
  END AS iso_alpha3,

  -- approximate centroid lat / lon per region
  CASE
    WHEN UPPER(region) LIKE '%AMERICA%'      THEN 37.0902
    WHEN UPPER(region) LIKE '%ASIA%'         THEN 34.0479
    WHEN UPPER(region) LIKE '%AFRICA%'       THEN 1.6508
    WHEN UPPER(region) LIKE '%EUROPE%'       THEN 54.5260
    WHEN UPPER(region) LIKE '%MIDDLE%' 
      OR UPPER(region) LIKE '%EAST%'         THEN 29.0000
    ELSE NULL
  END AS lat,

  CASE
    WHEN UPPER(region) LIKE '%AMERICA%'      THEN -95.7129
    WHEN UPPER(region) LIKE '%ASIA%'         THEN 100.6197
    WHEN UPPER(region) LIKE '%AFRICA%'       THEN 17.6021
    WHEN UPPER(region) LIKE '%EUROPE%'       THEN 15.2551
    WHEN UPPER(region) LIKE '%MIDDLE%' 
      OR UPPER(region) LIKE '%EAST%'         THEN 45.0000
    ELSE NULL
  END AS lon,

  -- optional normalized size for plotting (adjust divisor to taste)
  (total_sales_alltime / 1000000000)        AS total_sales_billion,

  -- optional log size (useful for point scaling)
  CASE WHEN total_sales_alltime > 0 THEN LOG(total_sales_alltime) ELSE NULL END AS total_sales_log

FROM top_regions_ct
ORDER BY total_sales_alltime DESC;
```

now sales by country with mapping,

```

DROP TABLE IF EXISTS sales_by_country_ct;

CREATE TABLE sales_by_country_ct
ENGINE=InnoDB
AS
SELECT
  n.n_nationkey                         AS n_nationkey,
  n.n_name                              AS nation,
  r.r_name                              AS region,

  -- ISO-3166 alpha-3 mapping for the 25 TPC-H nations in your dataset
  CASE UPPER(TRIM(n.n_name))
    WHEN 'ALGERIA'        THEN 'DZA'
    WHEN 'ARGENTINA'      THEN 'ARG'
    WHEN 'BRAZIL'         THEN 'BRA'
    WHEN 'CANADA'         THEN 'CAN'
    WHEN 'EGYPT'          THEN 'EGY'
    WHEN 'ETHIOPIA'       THEN 'ETH'
    WHEN 'FRANCE'         THEN 'FRA'
    WHEN 'GERMANY'        THEN 'DEU'
    WHEN 'INDIA'          THEN 'IND'
    WHEN 'INDONESIA'      THEN 'IDN'
    WHEN 'IRAN'           THEN 'IRN'
    WHEN 'IRAQ'           THEN 'IRQ'
    WHEN 'JAPAN'          THEN 'JPN'
    WHEN 'JORDAN'         THEN 'JOR'
    WHEN 'KENYA'          THEN 'KEN'
    WHEN 'MOROCCO'        THEN 'MAR'
    WHEN 'MOZAMBIQUE'     THEN 'MOZ'
    WHEN 'PERU'           THEN 'PER'
    WHEN 'CHINA'          THEN 'CHN'
    WHEN 'ROMANIA'        THEN 'ROU'
    WHEN 'SAUDI ARABIA'   THEN 'SAU'
    WHEN 'VIETNAM'        THEN 'VNM'
    WHEN 'RUSSIA'         THEN 'RUS'
    WHEN 'UNITED KINGDOM' THEN 'GBR'
    WHEN 'UNITED STATES'  THEN 'USA'
    ELSE NULL
  END                                    AS iso_alpha3,

  SUM(o.o_totalprice)                   AS total_sales

FROM orders o
JOIN customers c ON o.o_custkey = c.c_custkey
JOIN nations n   ON c.c_nationkey = n.n_nationkey
JOIN regions r   ON n.n_regionkey = r.r_regionkey

-- optional date filter (uncomment to restrict):
-- WHERE o.o_orderdate >= '1990-01-01' AND o.o_orderdate < '2014-01-02'

GROUP BY n.n_nationkey, n.n_name, r.r_name
ORDER BY total_sales DESC;
```

