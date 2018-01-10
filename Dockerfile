# Use an official Python runtime as a parent image
FROM python:3.6

# Set the working directory to /app
WORKDIR /app

# Copy the src directory contents into the container at /app
ADD . /app

# Move google credentials from app to proper location
RUN mkdir /root/.credentials && mv /app/client_secret.json /root/.credentials

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "src/app.py"]