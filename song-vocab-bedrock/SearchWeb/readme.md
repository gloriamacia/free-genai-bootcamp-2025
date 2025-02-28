
### **1️⃣ Rebuild Docker Image for `x86_64`**
```sh
docker build --platform linux/amd64 -t searchweb-lambda .
```

### **2️⃣ Tag the Image**
```sh
docker tag searchweb-lambda:latest 913524948358.dkr.ecr.us-east-1.amazonaws.com/searchweb-lambda:latest
```

### **3️⃣ Push to AWS ECR**
```sh
docker push 913524948358.dkr.ecr.us-east-1.amazonaws.com/searchweb-lambda:latest
```

### Example event
```json
{
  "query": "Die Philosoffen lyrics"
}
```

### Example response
```json
{
  "statusCode": 200,
  "body": "[{\"title\": \"Wise Guys - Die Philosoffen Lyrics - Genius\", \"url\": \"https://genius.com/Wise-guys-die-philosoffen-lyrics\"}, {\"title\": \"Wise Guys - Die Philosoffen (English translation) - Lyrics Translate\", \"url\": \"https://lyricstranslate.com/en/die-philosoffen-drunk-philosophers.html\"}, {\"title\": \"Die Philosoffen lyrics & translation - Wise Guys | Lyrics-ON\", \"url\": \"https://lyrics-on.net/en/1051123-die-philosoffen-lyrics.html\"}, {\"title\": \"DIE PHILOSOFFEN (Lyrics in English) - Wise Guys - Letras.com\", \"url\": \"https://www.letras.com/wise-guys/604028/english.html\"}, {\"title\": \"The Wiseguys - Die Philosoffen lyrics\", \"url\": \"https://www.allthelyrics.com/lyrics/the_wiseguys/die_philosoffen-lyrics-856297.html\"}]"
}
```