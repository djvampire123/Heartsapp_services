
# Down
FROM python:3.7

COPY heartsapp/ /app/heartsapp/
COPY data/ /app/data/
WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:/${WORKDIR}"
COPY requirements.txt /app
COPY start_app.sh /app
RUN pip install -r ./requirements.txt

EXPOSE 8080

CMD sh start_app.sh

#CMD ["python", "heartsapp/get_hub_module_and_save.py"]
#CMD ["python", "heartsapp/run_app.py"]
