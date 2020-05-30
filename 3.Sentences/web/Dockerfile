#Get python image from oficial docker hub
FROM python:3
#Setting working dir by convention
WORKDIR /usr/src/app
#Copy requirements to workingdir
COPY requirements.txt .
#Install requirements without cache packages
RUN pip install --no-cache-dir -r requirements.txt
#Copy current files (app.py, requirements) into the system
COPY . .
#Correr python y la app
CMD ["python", "app.py"]