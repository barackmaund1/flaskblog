# personal-Blog

## Author 

[barack maundu]()

# Description

This is a flask  application that allows  users to post,edit and delete blogs.It also allows the registered users to post comments on various posts.

## Live Link

Click this link to view the live application /

## ScreenShots

[home]()

[comment]()

[addcomment]()
## User Story

* A user can view the most recent posts.
* View and comment the blog posts on the site.
* A user should an email alert when a new post is made by joining a subscription.
* Register to be allowed to log in to the application
* A user sees random quotes on the site
* A writer can create a blog from the application and update or delete blogs I have created.

## BDD
| Behaviour | Input | Output |
| :---------------- | :---------------: | ------------------: |
| Load the page | **On page load** | Get all blogs, Select between signup and login|
| Select SignUp| **Email**,**Username**,**Password** | Redirect to login|
| Select Login | **Username** and **password** | Redirect to page with posted blogs|
| Select comment button | **Comment** | Form that you input your comment|
| Subscription |Email Address  | Flash message is displayed|



## Development Installation
To get the code..

1. Cloning the repository:
  ```bash
 
  ```
2. Move to the folder and install requirements
  ```bash
  cd pitch-world
  pip install -r requirements.txt
  ```
3. Exporting Configurations
  ```bash
  export SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://{User Name}:{password}@localhost/{database name}
  ```
4. Running the application
  ```bash
  python3.6 manage.py server
  ```
5. Testing the application
  ```bash
  python3.6 manage.py test
  ```
Open the application on your browser `127.0.0.1:5000`.

## Technology used

* [Python3.6](https://www.python.org/)
* [Flask](http://flask.pocoo.org/)
* [Heroku](https://heroku.com)

## Known Bugs

The subscription form is not working properly.

## Contact Information 

If you have any question or contributions, please email me at [pmaundu49@gmail.com]

## License
* *MIT License:*
* Copyright (c) 2019 ** barack maundu**