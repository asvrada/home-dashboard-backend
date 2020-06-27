# Home dashboard backend

[![Build Status](https://travis-ci.com/asvrada/home-dashboard-backend.svg?token=ug58w9zF9PguvrQ5qbqS&branch=master)](https://travis-ci.com/asvrada/home-dashboard-backend)
![Django CI](https://github.com/asvrada/home-dashboard-backend/workflows/Django%20CI/badge.svg?branch=master)

Powered by Django

## Run Docker Postgres

`docker run -p 5432:5432 --name db -e POSTGRES_USER=dashboard -e POSTGRES_PASSWORD=password -e POSTGRES_DB=dashboard postgres`

## How to do a fresh deploy

`docker exec -i -t dashboard-backend-backend bash`

1. Generate static file  
`./manager.py collectstatic`
2. Generate DB folder by running docker-compose
3. Do migration 
4. Create super user

## Code Coverage

```bash
coverage erase && coverage run manage.py test && coverage report
```
