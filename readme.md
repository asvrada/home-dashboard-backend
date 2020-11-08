# Home dashboard backend

[![Build Status](https://travis-ci.com/asvrada/home-dashboard-backend.svg?token=ug58w9zF9PguvrQ5qbqS&branch=master)](https://travis-ci.com/asvrada/home-dashboard-backend)
![Django CI](https://github.com/asvrada/home-dashboard-backend/workflows/Django%20CI/badge.svg?branch=master)

Powered by Django

> This is the backend for home dashboard project, link to frontend: https://github.com/asvrada/home-dashboard-frontend

## How to do a fresh deploy

0. `export POSTGRES_PASSWORD=[some password here]`
1. `docker-compose up`
2. ssh into the backend container  
`docker exec -i -t dashboard-backend-backend bash`
    1. `./manager.py collectstatic`
    3. makemigrations && migrate
    4. Create super user
    5. `./manage.py shell` and make a MonthlyBudget object for super user

## Code Coverage

```bash
coverage erase && coverage run manage.py test && coverage report
```
