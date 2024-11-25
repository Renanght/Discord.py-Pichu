FROM python:3.10-slim

RUN apt-get update && apt-get install -y git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

RUN git clone https://github.com/Renanght/Discord.py-Pichu.git /app


COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]
