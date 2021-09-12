FROM python:3.8.3
RUN set -x && \
    curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
ENV PATH /root/.poetry/bin:$PATH
RUN poetry config virtualenvs.create false
RUN pip install flask mongo
COPY ./src /home/app
EXPOSE 5000
CMD [ "python3", "app.py" ]
