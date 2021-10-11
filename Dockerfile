FROM python:3

WORKDIR /usr/src/EasyEats

# download dependencies
COPY requirements.txt ./

#install dependencies
RUN python3 -m pip install --user --no-cache-dir -r requirements.txt

COPY . .

CMD ["python","app.py"]