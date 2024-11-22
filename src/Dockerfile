FROM python:3.13.0-alpine AS build
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./models ./models/
COPY ./utils ./utils/
COPY main.py main.py

EXPOSE 8000

CMD ["fastapi", "run", "main.py", "--port", "8000"]