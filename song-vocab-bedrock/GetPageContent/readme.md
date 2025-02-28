# **🔹 Lambda 2: `GetPageContent`**
### **📌 Purpose**
✅ Fetches a **webpage URL** (provided by `SearchWeb`).  
✅ Extracts **plain text** from the webpage using `html2text`.  
✅ Returns **cleaned text**, limited to 4000 characters (AWS Lambda's limit).  

---
## **🔄 Deploy `GetPageContent` Lambda**
### **1️⃣ Build Docker Image for AWS Lambda**
```sh
docker build --platform linux/amd64 -t getpagecontent-lambda .
```

### **2️⃣ Tag the Docker Image**
```sh
docker tag getpagecontent-lambda:latest 913524948358.dkr.ecr.us-east-1.amazonaws.com/getpagecontent-lambda:latest
```

### **3️⃣ Push the Image to AWS ECR**
```sh
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 913524948358.dkr.ecr.us-east-1.amazonaws.com
aws ecr create-repository --repository-name getpagecontent-lambda
docker push 913524948358.dkr.ecr.us-east-1.amazonaws.com/getpagecontent-lambda:latest
```

### **4️⃣ Deploy to AWS Lambda (x86_64)**
```sh
aws lambda create-function \
    --function-name GetPageContentLambda \
    --package-type Image \
    --code ImageUri=913524948358.dkr.ecr.us-east-1.amazonaws.com/getpagecontent-lambda:latest \
    --role arn:aws:iam::913524948358:role/AWSLambdaBasicExecutionRole \
    --architectures x86_64
```

---

## **📌 Expected Input**
This function takes a **URL** as input.

```json
{
    "url": "https://genius.com/artist-name-song-name-lyrics"
}
```

## **📌 Expected Output**
This function **returns clean text from the webpage**.

```json
{
  "statusCode": 200,
  "body": "{\"text\": \"![Home](https://lyricstranslate.com/sites/all/themes/lt7/images/ltlogo.png)\\n![Home](/misc/logo-48.png)\\n\\nSearch\\n\\nRequest a translationBecome a translator\\n\\n![Sign Up](/sites/all/themes/lt7/images/user-add.svg)\\n\\n  * Log in\\n  * Sign up\\n  * Become a translator\\n  * Request new lyrics translation\\n  * Frequently Asked Questions\\n  * Website Rules\\n\\n  * Lyrics****\\n\\n    * Artists\\n    * Songs\\n    * Translations\\n    * Languages\\n    * Requests\\n    * Transcription requests\\n    * Subtitles\\n    * Idioms\\n    * Collections\\n\\n  * Artists\\n  * Translations\\n  * Languages\\n  * Actions****\\n\\n    * Add new translation\\n    * Add new song\\n    * Request a translation\\n    * Request lyrics transcription\\n    * Add subtitles\\n    * Start forum thread\\n\\n  * Community****\\n\\n    * Members\\n    * Forum\\n    * New forum topics\\n    * Recent comments\\n    * Popular Content / Site statistics\\n\\n  * Help****\\n\\n    * Request new lyrics translation\\n    * Become a translator\\n    * Website Rules\\n    * Frequently Asked Questions\\n    * Useful Resources\\n    * lyricstranslate.com forum\\n\\n  * Log in\\n  * Sign up\\n\\nLT -> German, English, German (K\\u00f6lsch) -> Wise Guys -> Die Philosoffen ->\\nEnglish\\n\\n  * ![Wise Guys](https://lyricstranslate.com/files/styles/thumbnail/public/Wise%2BGuys%2B%2Balt.jpg)\\n\\nWise Guys \\u2013 Die Philosoffen\\n\\n# English translation\\n\\n\\u2715\\n\\n![Share](/sites/all/themes/lt7/images/share.svg)\\n\\n![Font Size](/sites/all/themes/lt7/images/font-size.svg)\\n\\nProofreading requested\\n\\nGerman\\n\\n**Original lyrics**\\n\\n## Die Philosoffen\\n\\nDer Mann Aristoteles\\n\\nwar bl\\u00f6d, doch ich erz\\u00e4hl es:\\n\\nEr spielte Philosoph\\n\\nund fragte wie klein Doof:\\n\\n\\u201eWarum ist etwas da,\\n\\nwas da vorher noch nicht war?\\n\\nHm, das hat bestimmt nen Grund\\u2026\\u201c\\n\\nVielen Dank f\\u00fcr diesen Fund!\\n\\n\\n\\nEin Mann, genannt Diogenes,\\n\\nder tat was Ungezogenes,\\n\\nder hat, wie alle wissen,\\n\\nsich selber weggeschmissen.\\n\\nSo lebte er mit Wonne\\n\\nin einer dicken Tonne\\n\\nund das war ein echter Renner \\u2013\\n\\nheute macht das jeder Penner.\\n\\n\\n\\nDie Philosoffen\\n\\nwarn alle besoffen.\\n\\nDas ist kein Witz und auch kein Neid,\\n\\ndie waren breit, die ganze Zeit.\\n\\nDie Philosoffen\\n\\nwarn alle besoffen.\\n\\nLiest man nur kurz in ihren Texten,\\n\\nmerkt man, dass sie Wodka exten.\\n\\nWahrheit ist zu sp\\u00e4ter Stund\\u2019\\n\\neben ein Fass ohne Grund.\\n\\nDoch mal ganz offen:\\n\\nDas l\\u00e4sst mich hoffen,\\n\\ndass mans im Leben zu was bringt,\\n\\nwenn man trinkt.\\n\\n\\n\\nEin Mann, der Schopenhauer,\\n\\nder macht mich wirklich sauer,\\n\\nder hatte einen Willen,\\n\\nden konnt\\u2019 er aber nicht stillen.\\n\\nEr fand, das sei Beschiss,\\n\\ndas die Welt is, wie se is.\\n\\nNun, das ist uns allen klar \\u2013\\n\\nSchopi machte das zum Star.\\n\\n\\n\\nEin Mann mit Namen Hegel,\\n\\ndas war ein rechter Flegel,\\n\\nder konnte etwas meinen\\n\\nund es gleichzeitig verneinen.\\n\\nEr widersprach sich st\\u00e4ndig;\\n\\ndas fand man wohl sehr wendig\\n\\nund man nannte diese Hektik\\n\\nhochtrabend Dialektik.\\n\\n\\n\\nDie Philosoffen\\n\\nwarn alle besoffen.\\n\\nSie sahn der Wahrheit ins Gesicht\\n\\nund waren hackesturzedicht.\\n\\nDie Philosoffen\\n\\nwarn alle besoffen.\\n\\nLiest man nur kurz in ihren Werken,\\n\\nmerkt man, wie sich Denker st\\u00e4rken:\\n\\nmit nem tiefen Blick ins Glas.\\n\\nIn vino veritas!\\n\\nDoch mal ganz offen:\\n\\nDas l\\u00e4sst mich hoffen,\\n\\ndass es im Leben besser l\\u00e4uft,\\n\\nwenn man s\\u00e4uft.\\n\\n\\n\\nEin Mann, das war der Platon\"}"
}
```


