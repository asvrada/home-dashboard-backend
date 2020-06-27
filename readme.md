# Home dashboard backend

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