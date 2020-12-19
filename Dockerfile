FROM python:3.8
COPY . /dashboard
WORKDIR /dashboard
RUN pip3 install -r requirements.txt
EXPOSE 8501
ENTRYPOINT ["streamlit","run"]
CMD ["Dashboard_streamlit.py"]
