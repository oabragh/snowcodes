FROM python:3.10-alpine

ARG token

ENV DISCORD_TOKEN=$token

WORKDIR /bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "-m", "bot" ]
