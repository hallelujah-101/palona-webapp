# Use an official lightweight Python image
FROM python:3.12-slim-bookworm

# Set the working directory
WORKDIR /app  

# Copy project files into the container
COPY . /app  

# Install dependencies
RUN pip install -r requirements.txt  

# Expose port 8080 for Flask
EXPOSE 8080

# Command to run the app
CMD ["flask", "--app", "app", "run", "--host", "0.0.0.0", "--port", "8080"]