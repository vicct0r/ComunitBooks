# Use the official Python runtime image
FROM python:3.13-bookworm
 
# Create the app directory
RUN mkdir /app
 
# Set the working directory inside the container
WORKDIR /app
 
# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 

ENV DJANGO_SETTINGS_MODULE=config.settings.dev \
DATABASE_URL=sqlite:///db.sqlite3 \
SECRET_KEY='django-insecure-qf3b$-v5w&_4a4(2!-zzls16ipy8!^0^ia&t^+obylrt*ab4=('

 
# Upgrade pip
RUN pip install --upgrade pip 
 
# Copy the Django project  and install dependencies
COPY requirements/docker.txt  /app/
COPY entrypoint.sh /entrypoint.sh

# run this command to install all dependencies 
RUN pip install --no-cache-dir -r docker.txt
 
# Copy the Django project to the container
COPY . /app/
 
# Expose the Django port
EXPOSE 8000
 
# Run Django’s development server
ENTRYPOINT [ "/entrypoint.sh" ]