FROM python:3.8
COPY . .
WORKDIR .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install gunicorn -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD ["gunicorn", "-c", "gunicorn.py", "manage:app"]
EXPOSE 5001