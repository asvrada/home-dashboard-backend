FROM python

WORKDIR /app/

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . /app/

EXPOSE 8000

ENTRYPOINT ["gunicorn", "-b", ":8000", "dashboard.wsgi:application"]
