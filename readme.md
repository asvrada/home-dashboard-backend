# Home dashboard backend

[![Build Status](https://travis-ci.com/asvrada/home-dashboard-backend.svg?token=ug58w9zF9PguvrQ5qbqS&branch=master)](https://travis-ci.com/asvrada/home-dashboard-backend)
![Django CI](https://github.com/asvrada/home-dashboard-backend/workflows/Django%20CI/badge.svg?branch=master)

Powered by Django

> This is the backend for home dashboard project, link to frontend: https://github.com/asvrada/home-dashboard-frontend


## To run

### In Prod

1. `export POSTGRES_PASSWORD=<some password here>`  
2. `docker-compose up` or `sudo -E docker-compose up`

If this is the first time you deploy this project, you will need to run below command to set up the db and super user

 ```shell script
 docker exec -it dashboard-backend-backend bash &&
 ./manage.py collectstatic &&
 ./manage.py makemigrations && ./manage.py migrate
 ./manage.py createsuperuser &&
 ./manage.py setbudget <your email> <monthly budget amount>
 ```


### In Beta

`./manage.py runserver 4444`


## Code Coverage

```bash
coverage erase && coverage run manage.py test && coverage report
```

## APIs

```
admin/

# JWT Token related
/google-login/
/token-refresh/
/token-verify/

# Main
/restful/
  user/
  summary/
  budget/
/graphql/

# Available to Beta env only
/graphqltest/
/graphqltest/<int:id>
/email-login/
```

## TODOS

1. Define GraphQL Null behavior
