# **🔹 Lambda 3: `ExtractVocabulary`**
### **📌 Purpose**
✅ Takes **song lyrics** as input.  
✅ Extracts **unique vocabulary words** from the text.  
✅ Filters **common words** (stopwords) and **short words**.  
✅ Returns a **sorted list of useful words** for language learning.

---

## **🔄 Deploy `ExtractVocabulary` Lambda**
### **1️⃣ Log in to AWS ECR**
```sh
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 913524948358.dkr.ecr.us-east-1.amazonaws.com
```

### **2️⃣ Create AWS ECR Repository**
If you haven’t already created an **ECR repository**, run:
```sh
aws ecr create-repository --repository-name extractvocabulary-lambda
```

### **3️⃣ Build Docker Image for AWS Lambda**
```sh
docker build --platform linux/amd64 -t extractvocabulary-lambda .
```

### **4️⃣ Tag the Docker Image**
```sh
docker tag extractvocabulary-lambda:latest 913524948358.dkr.ecr.us-east-1.amazonaws.com/extractvocabulary-lambda:latest
```

### **5️⃣ Push the Image to AWS ECR**
```sh
docker push 913524948358.dkr.ecr.us-east-1.amazonaws.com/extractvocabulary-lambda:latest
```

### **6️⃣ Deploy to AWS Lambda (x86_64)**
```sh
aws lambda create-function \
    --function-name ExtractVocabularyLambda \
    --package-type Image \
    --code ImageUri=913524948358.dkr.ecr.us-east-1.amazonaws.com/extractvocabulary-lambda:latest \
    --role arn:aws:iam::913524948358:role/AWSLambdaBasicExecutionRole \
    --architectures x86_64
```

---

## **📌 Expected Input**
This function takes **song lyrics** as input.

```json
{
    "text": "Diese Welt ist eine Illusion, doch ich trinke und philosophiere."
}
```

## **📌 Expected Output**
This function **returns useful vocabulary words**.

```json
{
    "statusCode": 200,
    "body": {
        "vocabulary": ["welt", "illusion", "trinke", "philosophiere"]
    }
}
```
