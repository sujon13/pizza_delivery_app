# pizza_delivery_app

Documentation link: [Link](https://docs.google.com/document/d/1UaGnvdA0l_Inf_6FzmS-QZW6JkYmO6qaEauwMXp21TY/edit?fbclid=IwAR05cu2NkytxsuDxxSToCsirURAE3-JeYrWEfZ8p7BKyDjaouQ8GPFFgTaw)

## How to run it locally ##
1. Go to the folder where you want to clone it. suppose it's name is `backend-project`

2. Then you need to clone this repository `git clone <copied url>`

3. create virtual environment if you want and activate it

4. go to `pizza_delivery_app ` 

5. type `pip install -r requirements.txt`

6. Create a `.env` file inside  `pizza_app` directory

7. You need to include folowing key in `.env` file
 ```
DEBUG=on
SECRET_KEY=<secret_key>
DATABASE_URL=psql://<db_username>:<db_password>@127.0.0.1:<db_port>/<db_name>
```

8. type `python manage.py makemigrations`

9. type `python manage.py migrate`

10. type `python manage.py runserver`

11. server will run in `127.0.0.1:8000` url by default

12. create super user and test the api
