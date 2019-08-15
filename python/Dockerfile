FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY clean_response_config.json ./
COPY clean_response_server.py ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./clean_response_server.py" ]