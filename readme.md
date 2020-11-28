# Home dashboard backend

[![Build Status](https://travis-ci.com/asvrada/home-dashboard-backend.svg?token=ug58w9zF9PguvrQ5qbqS&branch=master)](https://travis-ci.com/asvrada/home-dashboard-backend)
![Django CI](https://github.com/asvrada/home-dashboard-backend/workflows/Django%20CI/badge.svg?branch=master)

Powered by Django

> This is the backend for home dashboard project, link to frontend: https://github.com/asvrada/home-dashboard-frontend

## How to do a fresh deploy

0. `export POSTGRES_PASSWORD=<some password here>`
1. `docker-compose up` or `sudo -E docker-compose up`
3. 
    ```shell script
    docker exec -i -t dashboard-backend-backend bash &&
    ./manage.py collectstatic &&
    ./manage.py makemigrations && ./manage.py migrate
    ./manage.py createsuperuser &&
    ./manage.py setbudget <your email> <monthly budget amount>
    ```

## Code Coverage

```bash
coverage erase && coverage run manage.py test && coverage report
```

## APIs

```
admin/

#JWT Token related
google-login/
token-refresh/
token-verify/

restful/
  user/
  summary/
  budget/
graphql/

# Test use only
graphqltest/
graphqltest/<int:id>
email-login/
```