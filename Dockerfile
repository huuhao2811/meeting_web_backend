FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Update pip và cài dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code
COPY . .

# Chạy Flask
CMD ["flask", "run", "--host=0.0.0.0"]
