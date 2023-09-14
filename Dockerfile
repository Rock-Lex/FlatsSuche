FROM python:3.10
WORKDIR /bot
COPY . /bot
RUN pip install -r requirements.txt
EXPOSE 3000
CMD python3 ./main.py