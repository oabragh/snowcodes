FROM python:3.10-alpine

ENV DISCORD_TOKEN=<token_here>

WORKDIR /bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "-m", "bot" ]
