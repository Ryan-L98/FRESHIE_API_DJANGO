# FRESHIE_API_DJANGO
The backend API for the freshie app.

## Overview
The freshie API provides data stored in the backend. 

## Django frameworks used
1. [Django REST Framework](https://www.django-rest-framework.org/)
2. [Django-rest-auth](https://django-rest-auth.readthedocs.io/en/latest/)

## Views
- Class based
  - [Registration](#registration)
  - Login
  - Recipes
  - Calories
- Function based
  - profileView
  - clientList
  - clientProfile
  - addPersonalTrainer
  - getConsumedMealsOn
  - getDelConsumedMeal
  - addConsumedMeal
  - getFavMeals
  - getDelFavMeal
  - addFavMeal
  - getMealPlans
  - addMealPlans
  - getDelMealPlan

## Documentation

## Registration
The registration is done using a class based view, which extends django-rest-auth's `RegisterView` class.

Request method | API endpoint
--- | ---                                                 
`POST`|https://freshie-api.herokuapp.com/register/

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
## Login
Similar to register, the login is also a class based view which extends django-rest-auth's `LoginView` class.

Request method | API endpoint
--- | ---                                                 
`POST`| https://freshie-api.herokuapp.com/login/

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

## Profile
The profile is done using a function based view, [`profileView`](./API/views.py/), and returns the requesting user's information 
Request method | API endpoint
--- | ---                                                 
`GET`| https://freshie-api.herokuapp.com/api/bobby/

#### Output
```JSON
{
    "id": 1,
    "username": "james",
    "referralCode": "JAMES1",
    "user": {
        "id": 1,
        "password": "pbkdf2_sha256$260000$gj9PvJqUW4y1ewIf4qpQhR$WppJps88jtXA3H0ybem8i72hh0Ye//uYhMkNPbeGxYI=",
        "last_login": "2021-06-25T21:55:04.857808+08:00",
        "is_superuser": false,
        "username": "james",
        "first_name": "james",
        "last_name": "yeap",
        "email": "james@eamil.com",
        "is_staff": false,
        "is_active": true,
        "date_joined": "2021-06-23T17:11:11.774779+08:00",
        "isPersonalTrainer": true,
        "mealPlans": [
            1,
            2
        ]
    }
}
```
---
## Recipes
The recipes API is done using a class based view, which extends django rest framework's [generic class views](https://github.com/encode/django-rest-framework/blob/master/rest_framework/generics.py).
Request method | API endpoint | Output
--- | --- |  ---                                              
`GET`| https://freshie-api.herokuapp.com/api/recipes/ | A list of the recipes

```JSON
[
    {
        "id": 1,
        "title": "chicken",
        "ingredients": "chicken",
        "instructions": "cook it",
        "calories": 123,
        "servings": 1,
        "custom": false,
        "author": "james"
    },
    {
        "id": 2,
        "title": "fish",
        "ingredients": "fish",
        "instructions": "cook it",
        "calories": 321,
        "servings": 1,
        "custom": false,
        "author": "james"
    },
    {
        "id": 3,
        "title": "crab",
        "ingredients": "crab",
        "instructions": "cook it",
        "calories": 213,
        "servings": 1,
        "custom": false,
        "author": "james"
    },
    {
        "id": 4,
        "title": "fish",
        "ingredients": "fish",
        "instructions": "cook it",
        "calories": 321,
        "servings": 1,
        "custom": false,
        "author": "james"
    },
    {
        "id": 5,
        "title": "crab",
        "ingredients": "crab",
        "instructions": "cook it",
        "calories": 213,
        "servings": 1,
        "custom": false,
        "author": "james"
    }
]
```
---
Request method | API endpoint | Output
--- | --- | ---                                               
`GET`| https://freshie-api.herokuapp.com/api/recipes/1/ | The recipe with the recipe ID
#### Output
```JSON
{
    "id": 1,
    "title": "chicken",
    "ingredients": "chicken",
    "instructions": "cook it",
    "calories": 123,
    "servings": 1,
    "custom": false,
    "author": "james"
}
```
---
Request method | API endpoint | Output
--- | --- | ---                                                
`PATCH`| https://freshie-api.herokuapp.com/api/recipes/1/ | Updates the recipe with the recipe ID
#### Input
```JSON
{
    "title": "chicken",
    "ingredients": "chicken and egg",
    "instructions": "cook it",
    "calories": 123,
    "servings": 1,
    "custom": false,
    "author": "james"
}
```

#### Output
```JSON
{
    "id": 1,
    "title": "chicken",
    "ingredients": "chicken and egg",
    "instructions": "cook it",
    "calories": 123,
    "servings": 1,
    "custom": false,
    "author": "james"
}
```
##### Note: Only the author of the recipe is allowed to make changes to the recipe.
---
Request method | API endpoint | Output
--- | --- | ---                                                
`DELETE`| https://freshie-api.herokuapp.com/api/recipes/1/ | Deletes the recipe with the recipe ID
---
## Calories
The calories API is done using class based view, which extends django rest framework's [generic class views](https://github.com/encode/django-rest-framework/blob/master/rest_framework/generics.py).

Request method | API endpoint | Output
--- | --- | ---                                                
`GET`| https://freshie-api.herokuapp.com/api/bobby/calories/ | The client's calories

#### Output
```JSON
{
    "id": 4,
    "dailyCalories": 2000,
    "currentCalories": 0,
    "client": "bobby"
}
```
##### Note: The client will only be able to view his own calorie count.
---
Request method | API endpoint | Output
--- | --- | ---                                                
`PATCH`| https://freshie-api.herokuapp.com/api/bobby/calories/ | Edit the client's calories
#### Input
```JSON
{
    "currentCalories": 532
}
```

#### Output 
```JSON
{
    "id": 4,
    "dailyCalories": 2000,
    "currentCalories": 532,
    "client": "bobby"
}
```
##### Note: Only the client or his personal trainer will be able to update his calories.

---
## Clients view as a personal trainer
The client views are done using function based views, [`clientList`](./API/views.py) and [`clientProfile`](./API/views.py).

Function | Request method | API endpoint | Output
--- | --- | --- | ---                                                
[`clientList`](./API/views.py) | `GET`| https://freshie-api.herokuapp.com/api/james/clients/ | The personal trainer's clients
#### Output
```JSON
[
    {
        "id": 1,
        "username": "bob",
        "user": {
            "id": 2,
            "password": "pbkdf2_sha256$260000$EsA4WqV9P0BqSIBb4qYVqI$sro4B8EGCzCnKIv/ZyzG/7dBNAdhWYwxZHCtUSA75Is=",
            "last_login": "2021-06-24T16:32:13.063393+08:00",
            "username": "bob",
            "first_name": "bob",
            "last_name": "bee",
            "email": "",
            "date_joined": "2021-06-23T17:19:28.358985+08:00",
            "isPersonalTrainer": false,
            "mealPlans": [
                1
            ]
        },
        "personalTrainer": {
            "id": 1,
            "username": "james",
            "referralCode": "JAMES1",
            "user": "james"
        }
    },
    {
        "id": 3,
        "username": "Q",
        "user": {
            "id": 4,
            "password": "pbkdf2_sha256$260000$zWMyFNScojkjtS8hyCYouY$AxrFmC2OEWeR0jmIobWp9pHxIr/vVTHsbA0SD+rQKRI=",
            "last_login": "2021-06-23T23:00:39.117705+08:00",
            "username": "Q",
            "first_name": "Q",
            "last_name": "Q",
            "email": "Q@email.com",
            "date_joined": "2021-06-23T18:14:35.098894+08:00",
            "isPersonalTrainer": false,
            "mealPlans": []
        },
        "personalTrainer": {
            "id": 1,
            "username": "james",
            "referralCode": "JAMES1",
            "user": "james"
        }
    },
    {
        "id": 4,
        "username": "bobby",
        "user": {
            "id": 6,
            "password": "pbkdf2_sha256$260000$Bapflp65ZoA7YIH20MV8Qr$kljzhFs39Xd2bfGKVjPoha9KhP9khhBTiq/xZcNU8Nk=",
            "last_login": "2021-06-25T22:27:05.566278+08:00",
            "username": "bobby",
            "first_name": "bobby",
            "last_name": "lee",
            "email": "bob@email.com",
            "date_joined": "2021-06-25T21:38:26.984507+08:00",
            "isPersonalTrainer": false,
            "mealPlans": []
        },
        "personalTrainer": {
            "id": 1,
            "username": "james",
            "referralCode": "JAMES1",
            "user": "james"
        }
    }
]
```
---

Function | Request method | API endpoint | Output
--- | --- | --- | ---                                                
[`clientProfile`](./API/views.py) | `GET`| https://freshie-api.herokuapp.com/api/james/client/bobby/view/ | The personal trainers client
#### Output
```JSON
{
    "id": 4,
    "username": "bobby",
    "user": {
        "id": 6,
        "password": "pbkdf2_sha256$260000$Bapflp65ZoA7YIH20MV8Qr$kljzhFs39Xd2bfGKVjPoha9KhP9khhBTiq/xZcNU8Nk=",
        "last_login": "2021-06-25T22:27:05.566278+08:00",
        "username": "bobby",
        "first_name": "bobby",
        "last_name": "lee",
        "email": "",
        "date_joined": "2021-06-25T21:38:26.984507+08:00",
        "isPersonalTrainer": false,
        "mealPlans": []
    },
    "personalTrainer": {
        "id": 1,
        "username": "james",
        "referralCode": "JAMES1",
        "user": "james"
    }
}
```
---

Function | Request method | API endpoint | Output
--- | --- | --- | ---                                                
[`clientProfile`](./API/views.py) | `GET`| https://freshie-api.herokuapp.com/api/james/client/bobby/meal-plans/ | The meal plans the client is on
#### Output
```JSON
[
    {
        "id": 2,
        "title": "week 2",
        "meal": [
            {
                "id": 2,
                "title": "fish",
                "ingredients": "fish",
                "instructions": "cook it",
                "calories": 321,
                "servings": 1,
                "custom": false,
                "author": "james"
            },
            {
                "id": 3,
                "title": "crab",
                "ingredients": "crab",
                "instructions": "cook it",
                "calories": 213,
                "servings": 1,
                "custom": false,
                "author": "james"
            }
        ]
    }
]
```

---
Function | Request method | API endpoint | Output
--- | --- | --- | ---                                                
[`clientProfile`](./API/views.py) | `POST`| https://freshie-api.herokuapp.com/api/james/client/bobby/assign-meal-plan/ | Assigns a meal plan to the client
#### Input
```JSON
{
    "mealPlanID": 2
}
```

#### Output
```JSON
"week 2 assigned to bobby!"
```

---
Function | Request method | API endpoint | Output
--- | --- | --- | ---                                                
[`clientProfile`](./API/views.py) | `DELETE`| https://freshie-api.herokuapp.com/api/james/client/bobby/remove-meal-plan/ | Deletes a meal plan the client is on
#### Input
```JSON
{
    "mealPlanID": 2
}
```
#### Output
```JSON
"Successfully removed week 2 from bobby's meal plans!"
```
---
Function | Request method | API endpoint | Output
--- | --- | --- | ---                                                
[`clientProfile`](./API/views.py) | `DELETE`| https://freshie-api.herokuapp.com/api/james/client/bobby/remove/ | Deletes client from personal trainer's clients
#### Output
```JSON
"You have successfully removed bobby as your client."
```

















