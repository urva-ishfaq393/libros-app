FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    ca-certificates \
    --no-install-recommends

RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable --no-install-recommends

RUN pip install --no-cache-dir selenium==4.18.1 pytest==8.1.1 webdriver-manager==4.0.1

WORKDIR /tests
COPY test_libros.py .

CMD ["python", "-m", "pytest", "test_libros.py", "-v", "--tb=short"]
