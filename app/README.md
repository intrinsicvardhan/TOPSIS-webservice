# TOPSIS App (Technique for Order of preference by Similarity to Ideal Solution) 

## Requires
-  Python 3.x
-  Flask
-  Flask Mail
-  Gmail 

## Usage
```bash
python app.py
```
-  Open your web browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000).
-  Upload the csv file, specify weights and impacts (+,-) in comma separated form
-  Results will then be sent to your specified email

## Configuration
-  `MAIL_USERNAME`: Your Gmail email address
-  `MAIL_PASSWORD`: App password generated from your google account
-  `MAIL_DEFAULT_SENDER`: Can be your email address or some else's
