#syntax=docker/dockerfile:1
#builder
FROM python:3.11-alpine AS builder

#git i klient ssh
RUN apk add --no-cache git openssh-client
WORKDIR /app

#konfiguracja ssh
RUN mkdir -p -m 0700 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
RUN --mount=type=ssh git clone git@github.com:MRachubik/PAChZadanie1.git .

#zależności
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

#obraz końcowy
FROM python:3.11-alpine
WORKDIR /app

#user
RUN adduser -D appuser

#metadane
LABEL org.opencontainers.image.authors="Maksymilian Rachubik"

#pliki
COPY --from=builder /root/.local /home/appuser/.local
COPY --from=builder --chown=appuser:appuser /app/app.py .

#ścieżki oraz wyłączenie buforowania
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

#zmiana uzytkownika
USER appuser

#healthchecl
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health') or exit(1)"

EXPOSE 5000

CMD ["python", "app.py"]
