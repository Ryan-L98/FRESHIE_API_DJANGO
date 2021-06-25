# FRESHIE_API_DJANGO
The backend API for the freshie app.

## Overview
The freshie API provides data stored in the backend. 

## Django frameworks used
1. [Django REST Framework](https://www.django-rest-framework.org/)
2. [Django-rest-auth](https://django-rest-auth.readthedocs.io/en/latest/)

## Data
- Users
  - Clients
    - Calories
    - Recipes
    - Meal plans
    - Personal information
    - Personal trainer
  - Personal Trainers
    - Clients
    - Meal plans
    - Recipes
    - Personal information

## Documentation

### Registration
The registration is done using a class based view, which extends django-rest-auth's `RegisterView` class.

Request method | API endpoint
--- | ---                                                 
`POST`|[Register](https://freshie-api.herokuapp.com/register/)

#### Input 
```JSON
{
  "username" : "bobby",
  "firstName" : "bobby",
  "lastName" : "lee",
  "email" : "bob@email.com",
  "password1" : ,
  "password2" : ,
  "isPersonalTrainer" : false,
  "referralCode" : "JAMES1",
  "calories" : 2000
}
  ```
#### Output
```JSON
{
    "key": "c502905e8f6f0b3a8aafd8054e688f1cc4fec401",
    "user": {
        "id": 6,
        "password": "pbkdf2_sha256$260000$Bapflp65ZoA7YIH20MV8Qr$kljzhFs39Xd2bfGKVjPoha9KhP9khhBTiq/xZcNU8Nk=",
        "last_login": "2021-06-25T21:38:27.082979+08:00",
        "username": "bobby",
        "first_name": "bobby",
        "last_name": "lee",
        "email": "bob@email.com",
        "date_joined": "2021-06-25T21:38:26.984507+08:00",
        "isPersonalTrainer": false,
    },
    "Signed up": "With personal Trainer",
    "status": "ok"
}
```
##### *key: The key returned is the authentication token that is required for further request after logging in.*
----
### Login
Similar to register, the login is also a class based view which extends django-rest-auth's `LoginView` class.

Request method | API endpoint
--- | ---                                                 
`POST`|[Login](https://freshie-api.herokuapp.com/login/)

#### Input 
```JSON
{
  "username" : "bobby",
  "password" : ,
}
  ```
#### Output
```JSON
{
    "key": "885282472e653902cf735251f8ddd147b16fda45",
    "user": {
        "id": 1,
        "password": "pbkdf2_sha256$260000$gj9PvJqUW4y1ewIf4qpQhR$WppJps88jtXA3H0ybem8i72hh0Ye//uYhMkNPbeGxYI=",
        "last_login": "2021-06-25T21:55:04.857808+08:00",
        "username": "bobby",
        "first_name": "bobby",
        "last_name": "lee",
        "email": "bob@email.com",
        "date_joined": "2021-06-25T21:38:26.984507+08:00",
        "isPersonalTrainer": true,
    }
}
```
##### *key: The key returned is the authentication token that is required for further request after logging in.*
---

