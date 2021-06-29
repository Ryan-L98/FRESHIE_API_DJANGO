# FRESHIE_API_DJANGO
The backend API for the [freshie app](https://github.com/jamesyeap/freshie).

## Overview
The freshie API provides data stored in the backend. 

## Django frameworks used
1. [Django REST Framework](https://www.django-rest-framework.org/)
2. [Django-rest-auth](https://django-rest-auth.readthedocs.io/en/latest/)

## Views
- **Class based**
  - [Login](#login)
  - [Recipes](#recipes)
  - [Calories](#calories)
- **Function based**
  - [recipeList](#recipelist)  
  - [addRecipe](#addrecipe)  
  - [editDelRecipe](#editdelrecipe)  
  - [getMealPlans](#getmealplans)
  - [addMealPlan](#addmealplan)
  - [getDelMealPlan](#getdelmealplan)
  - [profileView](#profile)
  - [clientList](#clientlist)
  - [clientProfile](#clientprofile)
  - [addPersonalTrainer](#addpersonaltrainer)
  - [getConsumedMealsOn](#getconsumedmealson)
  - [getDelConsumedMeal](#getdelconsumedmeal)
  - [addConsumedMeal](#addconsumedmeal)
  - [getFavMeals](#getfavmeals)
  - [getDelFavMeal](#getdelfavmeal)
  - [addFavMeal](#addfavmeal)


## Documentation

## Registration
The registration is done using a class based view, which extends django-rest-auth's `RegisterView` class.

Request method | API endpoint
--- | ---                                                 
`POST`|https://freshie-api.herokuapp.com/register/

<details><summary>Sample input and output</summary>
  
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
  
</details>

##### *key: The key returned is the authentication token that is required for further request after logging in.*
----
## Login
Similar to register, the login is also a class based view which extends django-rest-auth's `LoginView` class.

Request method | API endpoint
--- | ---                                                 
`POST`| https://freshie-api.herokuapp.com/login/

<details><summary>Sample input and output</summary>
  
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
</details>


##### *key: The key returned is the authentication token that is required for further request after logging in.*
---

## Profile
The profile is done using a function based view, [`profileView`](./API/views.py/), and returns the requesting user's information 
Request method | API endpoint
--- | ---                                                 
`GET`| https://freshie-api.herokuapp.com/api/james/

<details><summary>Sample output</summary>

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
  
  </details>
  
---
## Recipes

### [`recipeList`](./API/views.py)
Request method | API endpoint | Output
--- | --- |  ---                                              
`GET`| https://freshie-api.herokuapp.com/api/recipes/custom/ | A list of the recipes created by the user
`GET`| https://freshie-api.herokuapp.com/api/recipes/search/ | A list of the recipes created by the user and personal trainers

<details><summary>Sample output</summary>

#### Output
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
  
  </details>

---
### [`addRecipe`](./API/views.py)

Request method | API endpoint | Output
--- | --- | ---                                                
`POST`| https://freshie-api.herokuapp.com/api/recipes/ | Adds a new recipe to the database

<details><summary>Sample input and output</summary>
  
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
  
  </details>
  

---

### [`editDelRecipe`](./API/views.py)
Request method | API endpoint | Output
--- | --- | ---                                                
`POST`| https://freshie-api.herokuapp.com/api/recipes/edit/1/ | Edits the recipe with the recipe ID
##### Note: Only the author of the recipe is allowed to make changes to the recipe.
<details><summary>Summary input and output</summary>

#### Output
```JSON
{
        "title": "crab",
        "ingredients": "crab",
        "instructions": "cook it",
        "calories": 503,
        "servings": 1,
        "custom": true
}
```
#### Input

```JSON
{
    "id": 23,
    "title": "crab",
    "ingredients": "crab",
    "instructions": "cook it",
    "calories": 503,
    "servings": 1,
    "custom": null,
    "author": "bob"
}
```

</details>

Request method | API endpoint | Output
--- | --- | ---                                                
`DELETE`| https://freshie-api.herokuapp.com/api/recipes/edit/1/ | Deletes the recipe with the recipe ID
---

## Meal Plans
The Meal Plans can be created, read, updated and deleted with these function based views.
#### [`getMealPlans`](./API/views.py)
Request method | API endpoint | Output
--- | --- | ---                                                
 `GET`| https://freshie-api.herokuapp.com/api/bob/mealplans/ | The user's meal plans
 
 <details><summary>Sample output</summary>

#### Output
```JSON
[
  {
      "id": 1,
      "title": "week 1",
      "meal": [
          {
              "id": 1,
              "title": "chicken",
              "ingredients": "chicken and egg",
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
          }
      ]
  },
  {
      "id": 8,
      "title": "week 2",
      "meal": [
          {
              "id": 9,
              "title": "fish",
              "ingredients": "fish",
              "instructions": "cook it",
              "calories": 321,
              "servings": 1,
              "custom": false,
              "author": null
          },
          {
              "id": 10,
              "title": "crab",
              "ingredients": "crab",
              "instructions": "cook it",
              "calories": 213,
              "servings": 1,
              "custom": false,
              "author": null
          }
      ]
  }
]
  ```
  
  </details>
  
  ---
  
#### [`addMealPlan`](./API/views.py)
Request method | API endpoint | Output
--- | --- | ---                                                
`POST`| https://freshie-api.herokuapp.com/api/bob/add-mealplan/ | Adds a meal plan to the user

<details><summary>Sample output</summary>
  
#### Input
```JSON
{
  "meals" : [2,9],
  "title" : "Week 24"
}
  ```
#### Output
```JSON  
{
    "id": 9,
    "title": "Week 24",
    "meal": [
        {
            "id": 14,
            "title": "fish",
            "ingredients": "fish",
            "instructions": "cook it",
            "calories": 321,
            "servings": 1,
            "custom": false,
            "author": null
        },
        {
            "id": 15,
            "title": "fish",
            "ingredients": "fish",
            "instructions": "cook it",
            "calories": 321,
            "servings": 1,
            "custom": false,
            "author": null
        }
    ]
}
  ```
  
  </details>
  
  ---
#### [`getDelMealPlan`](./API/views.py)
Request method | API endpoint | Output
--- | --- | ---                                                
`GET`| https://freshie-api.herokuapp.com/api/bob/mealplan/8/ | Returns the meal plan

<details><summary>Sample output</summary>
  
#### Output
  ```JSON
  {
    "id": 8,
    "title": "week 2",
    "meal": [
        {
            "id": 9,
            "title": "fish",
            "ingredients": "fish",
            "instructions": "cook it",
            "calories": 321,
            "servings": 1,
            "custom": false,
            "author": null
        },
        {
            "id": 10,
            "title": "crab",
            "ingredients": "crab",
            "instructions": "cook it",
            "calories": 213,
            "servings": 1,
            "custom": false,
            "author": null
        }
    ]
}
  ```
  
  </details>

Request method | API endpoint | Output
--- | --- | ---                                                
`POST`| https://freshie-api.herokuapp.com/api/bob/mealplan/8/ | Edits the meal plan

<details><summary>Sample input and output</summary>

#### Input
```JSON
{
  "title" : "Week 2 edited",
  "meals" : [9,10,1]
}
 ```
#### Ouput
```JSON
{
    "id": 8,
    "title": "Week 2 edited",
    "meal": [
        {
            "id": 16,
            "title": "chicken",
            "ingredients": "chicken and egg",
            "instructions": "cook it",
            "calories": 123,
            "servings": 1,
            "custom": false,
            "author": null
        },
        {
            "id": 17,
            "title": "fish",
            "ingredients": "fish",
            "instructions": "cook it",
            "calories": 321,
            "servings": 1,
            "custom": false,
            "author": null
        },
        {
            "id": 18,
            "title": "crab",
            "ingredients": "crab",
            "instructions": "cook it",
            "calories": 213,
            "servings": 1,
            "custom": false,
            "author": null
        }
    ]
}
```
  
  </details>

Request method | API endpoint | Output
--- | --- | ---                                                
`DELETE`| https://freshie-api.herokuapp.com/api/bob/mealplan/8/ | Deletes the meal plan

---
## Personal trainer methods
##### *Methods that can only be used if logged in as a personal trainer.*
#### [`clientList`](./API/views.py)
Request method | API endpoint | Output
--- | --- | ---                                                
 `GET`| https://freshie-api.herokuapp.com/api/james/clients/ | The personal trainer's clients
 
 <details><summary>Sample output</summary>
  
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
  
  </details>
  
---

#### [`clientProfile`](./API/views.py)
Request method | API endpoint | Output
 --- | --- | ---                                                
`GET`| https://freshie-api.herokuapp.com/api/james/client/bobby/view/ | The personal trainers client

<details><summary>Sample output</summary>
  
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
  
  </details>

 Request method | API endpoint | Output
--- | --- | ---                                                
 `GET`| https://freshie-api.herokuapp.com/api/james/client/bobby/meal-plans/ | The meal plans the client is on
 
 <details><summary>Sample output</summary>
  
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
</details>

Request method | API endpoint | Output
 --- | --- | ---                                                
`POST`| https://freshie-api.herokuapp.com/api/james/client/bobby/assign-meal-plan/ | Assigns a meal plan to the client

<details><summary>Sample input and output</summary>
  
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
  </details>

Request method | API endpoint | Output
 --- | --- | ---                                                
 `DELETE`| https://freshie-api.herokuapp.com/api/james/client/bobby/remove-meal-plan/ | Deletes a meal plan the client is on
 
 <details><summary>Sample input and output</summary>
  
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
  
  </details>
  
 Request method | API endpoint | Output
--- | --- | ---                                                
`DELETE`| https://freshie-api.herokuapp.com/api/james/client/bobby/remove/ | Deletes client from personal trainer's clients

<details><summary>Sample output</summary>
  
#### Output
```JSON
"You have successfully removed bobby as your client."
```
  
  </details>

---
#### [`addPersonalTrainer`](./API/views.py/)
 Request method | API endpoint | Output
--- | --- | ---                                                
`POST`| https://freshie-api.herokuapp.com/api/bobby/add-personal-trainer/ | Adds personal trainer to client using a referral code

<details><summary>Sample input and output</summary>
  
#### Input
```JSON
{
  "referralCode" : "JAMES1"
}
```
#### Output
```
"James is now your personal trainer!"
```
  </details>
  
---
## Client methods
##### *Methods that can only be used when logged in as a client.*

## Calories
The calories API is done using class based view, which extends django rest framework's [generic class views](https://github.com/encode/django-rest-framework/blob/master/rest_framework/generics.py).

Request method | API endpoint | Output
--- | --- | ---                                                
`GET`| https://freshie-api.herokuapp.com/api/bobby/calories/ | The client's calories
##### Note: The client will only be able to view his own calorie count.
<details><summary>Sample output</summary>
  
#### Output
```JSON
{
    "id": 4,
    "dailyCalories": 2000,
    "currentCalories": 0,
    "client": "bobby"
}
```
  </details>

Request method | API endpoint | Output
--- | --- | ---                                                
`PATCH`| https://freshie-api.herokuapp.com/api/bobby/calories/ | Edit the client's calories
##### Note: Only the client or his personal trainer will be able to update his calories.
<details><summary>Sample input and output</summary>
  
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
  </details>

---
#### [`getConsumedMealsOn`](./API/views.py/)
 Request method | API endpoint | Output
--- | --- | ---                                                
`POST`| https://freshie-api.herokuapp.com/api/bobby/consumed-meals/ | Returns a list of the consumed meals on provided date

<details><summary>Sample input and output</summary>
  
#### Input
```JSON
{
  "day" : 24,
  "month" : 6,
  "year" : 2021
}
```
#### Output 
```JSON
[
    {
        "id": 18,
        "mealType": "Supper",
        "date": "2021-06-24",
        "calories": 123,
        "meal": {
            "id": 1,
            "title": "chicken",
            "ingredients": "chicken and egg",
            "instructions": "cook it",
            "calories": 123,
            "servings": 1,
            "custom": false,
            "author": "james"
        },
        "client": {
            "id": 1,
            "username": "bob",
            "user": "bob",
            "personalTrainer": "james"
        }
    },
    {
        "id": 25,
        "mealType": "Supper",
        "date": "2021-06-24",
        "calories": 123,
        "meal": {
            "id": 1,
            "title": "chicken",
            "ingredients": "chicken and egg",
            "instructions": "cook it",
            "calories": 123,
            "servings": 1,
            "custom": false,
            "author": "james"
        },
        "client": {
            "id": 1,
            "username": "bob",
            "user": "bob",
            "personalTrainer": "james"
        }
    },
    {
        "id": 26,
        "mealType": "Supper",
        "date": "2021-06-24",
        "calories": 321,
        "meal": {
            "id": 4,
            "title": "fish",
            "ingredients": "fish",
            "instructions": "cook it",
            "calories": 321,
            "servings": 1,
            "custom": false,
            "author": "james"
        },
        "client": {
            "id": 1,
            "username": "bob",
            "user": "bob",
            "personalTrainer": "james"
        }
    }
]
```
  
  </details>
  
---
#### [`getDelConsumedMeal`](./API/views.py/)
 Request method | API endpoint | Output
--- | --- | ---                                                
`GET`| https://freshie-api.herokuapp.com/api/bobby/consumed-meal/18/ | Returns a consumed meal

<details><summary>Sample output</summary>
  
#### Output
```JSON 
{
    "id": 18,
    "mealType": "Supper",
    "date": "2021-06-24",
    "calories": 123,
    "meal": {
        "id": 1,
        "title": "chicken",
        "ingredients": "chicken and egg",
        "instructions": "cook it",
        "calories": 123,
        "servings": 1,
        "custom": false,
        "author": "james"
    },
    "client": {
        "id": 1,
        "username": "bob",
        "user": "bob",
        "personalTrainer": "james"
    }
}
```
  </details>
  
 Request method | API endpoint | Output
--- | --- | ---                                                
`DELETE`| https://freshie-api.herokuapp.com/api/bobby/consumed-meal/18/ | deletes a consumed meal
---

#### [`addConsumedMeal`](./API/views.py/)
 Request method | API endpoint | Output
--- | --- | ---                                                
`POST`| https://freshie-api.herokuapp.com/api/bobby/add-consumed-meal/ | Adds a consumed meal to client

<details><summary>Sample input and output</summary>
  
#### Input
```JSON
{
  "mealType" : "Supper",
  "recipeID" : 18
}
```
#### Ouput
```JSON
{
    "id": 18,
    "mealType": "Supper",
    "date": "2021-06-24",
    "calories": 123,
    "meal": {
        "id": 1,
        "title": "chicken",
        "ingredients": "chicken and egg",
        "instructions": "cook it",
        "calories": 123,
        "servings": 1,
        "custom": false,
        "author": "james"
    },
    "client": {
        "id": 1,
        "username": "bob",
        "user": "bob",
        "personalTrainer": "james"
    }
}
```
  </details>
  
---
#### [`getFavMeals`](./API/views.py/)
 Request method | API endpoint | Output
--- | --- | ---                                                
`GET`| https://freshie-api.herokuapp.com/api/bobby/fav-meals/ | Returns a list of the client's favourite meals

<details><summary>Sample output</summary>

#### Ouput
```JSON
  [
    {
        "id": 1,
        "meal": {
            "id": 11,
            "title": "chicken",
            "ingredients": "chicken and egg",
            "instructions": "cook it",
            "calories": 123,
            "servings": 1,
            "custom": false,
            "author": null
        },
        "client": {
            "id": 1,
            "username": "bob",
            "user": "bob",
            "personalTrainer": "james"
        }
    },
    {
        "id": 2,
        "meal": {
            "id": 12,
            "title": "fish",
            "ingredients": "fish",
            "instructions": "cook it",
            "calories": 321,
            "servings": 1,
            "custom": false,
            "author": null
        },
        "client": {
            "id": 1,
            "username": "bob",
            "user": "bob",
            "personalTrainer": "james"
        }
    }
]
  ```
  </details>
  
  ---
#### [`getDelFavMeal`](./API/views.py/)
Request method | API endpoint | Output
--- | --- | ---                                                
`GET`| https://freshie-api.herokuapp.com/api/bobby/fav-meals/1/ | Returns the client's favourite meal

<details><summary>Sample output</summary>

  #### Output
```JSON
{
    "id": 1,
    "meal": {
        "id": 11,
        "title": "chicken",
        "ingredients": "chicken and egg",
        "instructions": "cook it",
        "calories": 123,
        "servings": 1,
        "custom": false,
        "author": null
    },
    "client": {
        "id": 1,
        "username": "bob",
        "user": "bob",
        "personalTrainer": "james"
    }
}
  ```
  
  </details>

Request method | API endpoint | Output
--- | --- | ---                                                
`DELETE`| https://freshie-api.herokuapp.com/api/bobby/fav-meal/1/ | deletes a favourite meal
---
---  
#### [`addFavMeal`](./API/views.py/)
Request method | API endpoint | Output
--- | --- | ---                                                
`POST`| https://freshie-api.herokuapp.com/api/bobby/add-fav-meal/ | Adds an existing recipe to client's favourites

<details><summary>Sample input and output</summary>

#### Output
```JSON
{
    "recipeID" : 3
}
```
#### Input
```JSON
{
    "id": 3,
    "meal": {
        "id": 13,
        "title": "crab",
        "ingredients": "crab",
        "instructions": "cook it",
        "calories": 213,
        "servings": 1,
        "custom": false,
        "author": null
    },
    "client": {
        "id": 1,
        "username": "bob",
        "user": "bob",
        "personalTrainer": "james"
    }
}
  ```
  
  </details>
  

















