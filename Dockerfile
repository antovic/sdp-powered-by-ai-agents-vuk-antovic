FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exit code 5 = no tests collected (expected during early scaffolding before Module 5)
CMD ["sh", "-c", "python -m pytest; code=$?; [ $code -eq 5 ] && exit 0 || exit $code"]
