# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker's layer caching
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the uvicorn server.
# Use 0.0.0.0 to listen on all available network interfaces inside the container.
# Do not use --reload in a production-like Docker environment.
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]