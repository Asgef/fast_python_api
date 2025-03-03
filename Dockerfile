FROM python:3.13-slim
LABEL maintainer="asgefes1@gmail.com"

ENV SECRET_KEY='...' \
DATABASE_URL='...' DEBUG=True \
TEST_SERVICE_URL='https://randomuser.me/api'
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
ENTRYPOINT ["uvicorn", "fast_python_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
