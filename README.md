# Flask-Sqlite3-JWT-authentication
Flask Signup, Login and Protected routes with FLask JWT extended


## SignUp /Registration CURL request

```
curl --location --request POST 'localhost:5000/signup' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "kavyansh1",
    "password": "testpass123"
}'
```

## Login Curl

```
curl --location --request POST 'localhost:5000/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "kavyansh1",
    "password": "testpass123"
}'
```

## Protected Route curl (Needs to add each route, which needs to be protected)
Protected routes can't be accessible without access_Token, that will generate on login

```
curl --location --request GET 'localhost:5000/protected' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCIIkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NTc4NTEzMSwianRpIjoiY2Q2NzU3OWYtYmMzYi00NDgzLTk1ZjgtMjRlZWViMmU0NmRmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjg1Nzg1MTMxLCJleHAiOjE2ODU3ODYwMzF9.RzlWEZrdAzFqsuHVxAk-YMGp3gIv-eJkbe83I_qst_Q' \
--data-raw ''
``
