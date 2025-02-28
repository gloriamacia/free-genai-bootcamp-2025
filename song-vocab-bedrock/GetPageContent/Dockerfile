# Use AWS Lambda Python 3.13 base image for x86_64
FROM public.ecr.aws/lambda/python:3.13

# Set the working directory
WORKDIR /var/task

# Copy function code into container
COPY get_page_content.py .

# Install required dependencies
RUN pip install --no-cache-dir requests html2text -t .

# Command to start the Lambda function
CMD ["get_page_content.lambda_handler"]
