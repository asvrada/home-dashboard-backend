FROM python

WORKDIR /app/

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . /app/

EXPOSE 80

ENTRYPOINT ["gunicorn", "-b", ":80", "dashboard.wsgi:application"]
