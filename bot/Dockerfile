FROM python:3.7-slim
WORKDIR /app
COPY ./ /app
RUN pip install -r /app/requirements.txt
RUN python3 -m pip install --upgrade Pillow
RUN python3 -m pip install "tablib[xls]"
CMD ["python3", "telegram_bot.py"] 
