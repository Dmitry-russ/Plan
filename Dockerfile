FROM python:3.7-slim
WORKDIR /app/Plan/
COPY ./ /app
RUN pip install -r /app/requirements.txt
RUN python3 -m pip install --upgrade Pillow
RUN python3 -m pip install "tablib[xls]"
RUN rm -rf /etc/localtime
RUN ln -s /usr/share/zoneinfo/Asia/Yekaterinburg /etc/localtime
RUN echo "Asia/Yekaterinburg" > /etc/timezone
CMD ["gunicorn", "Plan.wsgi:application", "--bind", "0:8000" ] 
