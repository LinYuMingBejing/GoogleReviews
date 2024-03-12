# Google Review System
## API SPEC
|  Resources  | Method  | Permission  | Response  | 
| --------    | -----|  -----| -----| 
| /register/  | POST | X | <code>{"username": "cycarrier","email": "cycarrier@trendmicro.com","first_name": "Jack","last_name": "Wu"}</code>`
| /login/     | POST | X |<code> {"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMDMzMTU1NCwiaWF0IjoxNzEwMjQ1MTU0LCJqdGkiOiJjMDY0MjQ4NTc1MDI0ZTU1ODlmYzBmZjdhMjM4MDhjZiIsInVzZXJfaWQiOjJ.pr6M2pnJ3Jyf_cFSJ5rj2-4sOc3zGQpbmaKIqEQpyoc","access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEwMjQ2MzU0LCJpYXQiOjE3MTAyNDUxNTQsImp0aSI6ImVmNDVhZDFlZmY2ODRmOTA5YTA5MmUyMTJmNDE5NzU5IiwidXNlcl9pZCI6Mn0iHNAFsjlxiKkrSmWoyF5iV2YG-YtCk11eLNUGaj6ZIw"} </code>` |
| /user/      | GET | O | <code> {"count": 2,"next": null,"previous": null,"results": [ {"id": 1, "username": "root", "email": "root@yahoo.com"}.....]} </code>` |
| /user/{id}/ | GET | O | <code> {"id": 1, "username": "root", "email": "root@yahoo.com"} </code>`|
| /user/{id}/reviews/  | GET | O | <code> [{"id": 1, "title": "此味僅天上有", "content": "香港必推美食", "score": 5,"restaurant_id": 1},...] </code>`|
| /restaurant/  | GET | X | | <code> {"count": 1, "next": null,"previous": null, "results": [{"id": 1, "name": "添好運倒閉", "review_count": 4,"score": 4.75}]} <code>`|  
| /restaurant/?search=xx  | GET | X | <code> {"count": 1, "next": null,"previous": null, "results": [{"id": 1, "name": "添好運倒閉", "review_count": 4,"score": 4.75}]} <code>`|  
| /restaurant/{id}/  | GET | X |  <code> {"id": 4, "name": "八里美味雞排", "review_count": 0, "score": 0} </code>`|
| /restaurant/  | POST | O | <code> {"id": 4, "name": "八里鹽酥雞", "review_count": 0, "score": 0}</code>` |
| /restaurant/{id}/  | PUT | O | <code> { "id": 4, "name": "八里美味雞排", "review_count": 0, "score": 0 }</code>` |
| /restaurant/{id}/  | DELETE | O | <code>{"detail": "Not found."} </code>`|
| /restaurant/{id}/reviews/  | GET | O | <code> [{"id": 1,"title": "此味僅天上有", "content": "香港必推美食", "score": 5, "user_id": 1}] </code>`  |
| /review/  | GET | X | <code> {"count": 6,"next": "http://localhost:8000/review/?page=2","previous": null,"results": [{"id": 1, "title": "此味僅天上有", "content": "香港必推美食","score": 5, "restaurant_id": 1, "user_id": 1},....]} </code>` |
| /review/{id}/  | GET | X | <code> {"id": 1, "title": "此味僅天上有", "content": "香港必推美食", "score": 5, "restaurant_id": 1, "user_id": 1} </code>` |
| /review/  | POST | O |<code> {"id": 7, "title": "好好吃", "content": "絕世美味", "score": 5, "restaurant_id": 1, "user_id": 2} </code>` |
| /review/{id}/  | PUT | O | <code> [{"id": 1,"title": "此味僅天上有", "content": "香港必推美食", "score": 5, "user_id": 1}] </code>`  |
| /review/{id}/  | DELETE | O | <code>{"detail": "Not found."} </code>`|

## Permission Error
|  Statud Code  | Response  | 
| --------    | -----|
| 401  | <code> {"detail": "Authentication credentials were not provided."}</code>`|   
| 401  |<code> {"detail": "Given token not valid for any token type","code": "token_not_valid", "messages": [{"token_class": "AccessToken", "token_type": "access","message": "{}"}]}</code>` |

## DB Schema Desgin
![img](https://upload.cc/i1/2024/03/12/1Ubnrg.png)


### Start Djagno Application
```
$ django-admin startproject CyCarrier
$ python manage.py startapp restaurant
```

### DB Migrate
```
$ python manage.py makemigrations
$ python manage.py migrate
```

### Create root user
```
python3 manage.py createsuperuser
```
