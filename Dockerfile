FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir asteval==1.0.5

RUN useradd -m -u 10001 ctf
WORKDIR /app
COPY server.py /app/server.py

ENV FLAG="ZCTF2026{fake_flag_run_against_remote}" \
    PORT=5000 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

USER ctf
EXPOSE 5000

CMD ["sh","-c","exec socat -T120 TCP-LISTEN:${PORT},reuseaddr,fork,nodelay EXEC:'python3 -u /app/server.py',stderr"]
