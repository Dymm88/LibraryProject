FROM python:3.12-slim

WORKDIR /src

COPY . .
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN pip install --no-cache-dir -r requirements.txt &&  \
    chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]