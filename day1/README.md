# Day 1 Introduction

Superset basics are discussed with Single instance of Superset using SQLite.

Subsequent days, we will discuss clustering, failover, caching, meta-database, replications, fault tolerance,
scheduling and multi-worker architecture.

# 0. requirements

- VS Code
- Docker Desktop

```
c:\> mkdir superset
c:\> cd superset
c:\superset> mkdir day1
c:\superset> cd day1
c:\superset\day1> code .
```

Create a folder superset_home under c:\superset\day1, this will store sqlite files. Sqlite is temporary, get starter, not a production option. For production, we will use postgresql for metadb.

c:\superset\day1> mkdir superset_home

Create a file named 'docker-compose.yml', paste the content of the docker compose file in day1 directory..


# 1. Export env (docker-compose will automatically read .env)

```
docker compose up  
```

# Monitor logs (optionally)

on another prompt..

```
docker compose logs -f superset_sqlite
```

After superset-init finishes, open browser:

http://localhost:8088

default admin user created above: admin / admin


----

fab stands for Flask App Builder


```
docker exec -it superset_sqlite bash
```

```
superset fab create-admin \
  --username admin \
  --firstname Admin \
  --lastname User \
  --email admin@superset.local \
  --password admin
```

```
docker exec -it superset_sqlite bash -c 'superset db upgrade && superset init'
```


```
docker exec -it superset_sqlite superset load_examples
```

```
docker restart superset_sqlite
```

Health check for nginx

```
http://localhost:8088/health
```


to remove all data, don't do this command

```
docker compose down --volumes --remove-orphans
```
