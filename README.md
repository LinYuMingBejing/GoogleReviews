# Google Review System
## Environment:
* Backend: Django Rest Framework
* Deploy: Docker, Docker Compose


## Google Review APIs 
|  Resources  | Method  | Permission  | Response  | 
| --------    | -----|  -----| -----| 
| /register/  | POST | X | <code>{"username": "cycarrier","email": "cycarrier@trendmicro.com","first_name": "Jack","last_name": "Wu"}</code>`
| /login/     | POST | X |<code> {"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMDMzMTU1NCwiaWF0IjoxNzEwMjQ1MTU0LCJqdGkiOiJjMDY0MjQ4NTc1MDI0ZTU1ODlmYzBmZjdhMjM4MDhjZiIsInVzZXJfaWQiOjJ.pr6M2pnJ3Jyf_cFSJ5rj2-4sOc3zGQpbmaKIqEQpyoc","access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEwMjQ2MzU0LCJpYXQiOjE3MTAyNDUxNTQsImp0aSI6ImVmNDVhZDFlZmY2ODRmOTA5YTA5MmUyMTJmNDE5NzU5IiwidXNlcl9pZCI6Mn0iHNAFsjlxiKkrSmWoyF5iV2YG-YtCk11eLNUGaj6ZIw"} </code>` |
| /user/      | GET | O (Admin) | <code> {"count": 2,"next": null,"previous": null,"results": [ {"id": 1, "username": "root", "email": "root@yahoo.com"}.....]} </code>` |
| /user/{id}/ | GET | O (Admin) | <code> {"id": 1, "username": "root", "email": "root@yahoo.com"} </code>`|
| /user/{id}/reviews/  | GET | X | <code> [{"id": 1, "title": "此味僅天上有", "content": "香港必推美食", "score": 5,"restaurant": 1},...] </code>`|
| /restaurant/  | GET | X | | <code> {"count": 1, "next": null,"previous": null, "results": [{"id": 1, "name": "添好運", "review_count": 4,"score": 4.75}]} <code>`|  
| /restaurant/?search=xx  | GET | X | <code> {"count": 1, "next": null,"previous": null, "results": [{"id": 1, "name": "添好運", "review_count": 4,"score": 4.75}]} <code>`|  
| /restaurant/{id}/  | GET | X |  <code> {"id": 4, "name": "八里美味雞排", "review_count": 0, "score": 0} </code>`|
| /restaurant/  | POST | O (Admin) | <code> {"id": 4, "name": "八里鹽酥雞", "review_count": 0, "score": 0}</code>` |
| /restaurant/{id}/  | PUT | O (Admin) | <code> { "id": 4, "name": "八里美味雞排", "review_count": 0, "score": 0 }</code>` |
| /restaurant/{id}/  | DELETE | O (Admin) | <code>{"detail": "Not found."} </code>`|
| /restaurant/{id}/reviews/  | GET | O | <code> [{"id": 1,"title": "此味僅天上有", "content": "香港必推美食", "score": 5, "user": 1}] </code>`  |
| /review/  | GET | X | <code> {"count": 6,"next": "http://localhost:8000/review/?page=2","previous": null,"results": [{"id": 1, "title": "此味僅天上有", "content": "香港必推美食","score": 5, "restaurant": 1, "user": 1},....]} </code>` |
| /review/{id}/  | GET | X | <code> {"id": 1, "title": "此味僅天上有", "content": "香港必推美食", "score": 5, "restaurant": 1, "user": 1} </code>` |
| /review/  | POST | O |<code> {"id": 7, "title": "好好吃", "content": "絕世美味", "score": 5, "restaurant": 1, "user": 2} </code>` |
| /review/{id}/  | PUT | O | <code> [{"id": 1,"title": "此味僅天上有", "content": "香港必推美食", "score": 5, "user": 1}] </code>`  |
| /review/{id}/  | DELETE | O | <code>{"detail": "Not found."} </code>`|

## Permission Error
```
 curl -X GET http://localhost/user
 -H {"Authorization": "Bearer [access_token]"}
```
|  Statud Code  | Response  | 
| --------    | -----|
| 401  | <code> {"detail": "Authentication credentials were not provided."}</code>`|   
| 401  |<code> {"detail": "Given tokenREADME.md not valid for any token type","code": "token_not_valid", "messages": [{"token_class": "AccessToken", "token_type": "access","message": "{}"}]}</code>` |

## API SPEC
### User Register
|  Parameter  | Requirement  | 
| --------    | -----| 
| username  | 1. A user with that username already exists. <br> 2. Ensure this field has no more than 150 characters.| 
| password  | 1. Password must contain at least 1 uppercase letter, 1 lowercase letter, and 1 number.<br> 2. Password must be a string between 8 and 16 letters.|
| password2  | Password fields didn't match. | 
| email  | 1. This field must be unique. <br> 2. Enter a valid email address. | 

### Restaurant API
|  Parameter  | Requirement  | 
| --------    | -----| 
| name  | 1. Ensure this field has no more than 64 characters. <br> 2. This field must be unique.| 

### Review API
|  Parameter  | Requirement  | 
| --------    | -----| 
| title  | Ensure this field has no more than 64 characters. | 
| score  | Score must between 1 and 5 | 
| user  | 1. The fields user, restaurant must make a unique set. <br> 2. Invalid pk - object does not exist. | 
| restaurant  | 1. The fields user, restaurant must make a unique set. <br> 2. Invalid pk - object does not exist. | 


## DB Schema Desgin
![img](https://upload.cc/i1/2024/03/12/1Ubnrg.png)

* Unique fileds: <br> 1. Review: (restaurant, user)<br> 2. Restaurant: (name)

## Start Djagno Application
```
$ cd src/
$ docker build -t google-reviews .
$ docker run -p 8001:8001 google-reviews:latest
```

## Create root user
```
$ docker exec -it container_id python manage.py createsuperuser
```

## Note
### DB Migrate
```
$ python manage.py makemigrations
$ python manage.py migrate
```

### TODO List
* Custom response format

