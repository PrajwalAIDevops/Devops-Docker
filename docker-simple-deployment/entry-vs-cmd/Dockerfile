FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . . 
ENTRYPOINT ["python","app1.py"] 
# --> python app1.py not python app2.py ..!
CMD ["app2.py"]


# ENTRYPOINT ["python"] --> python app1.py 
# CMD ["app1.py"] 

# ENTRYPOINT ["python"] --> python app2.py 
# CMD ["app2.py"] 

# CMD ["python","app1.py"]
#  docker run -p 8080:5002 flaskwebapp app2.py --> It will override with app2.py file 