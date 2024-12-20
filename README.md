# Todo-App
A todo application

## Description
A simple to-do app to manage your daily tasks efficiently.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/iftakharuddin/Todo-App.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Todo-App
   ```
3. Activate virtual environment(for windows):
   ```bash
   .\myenv\Scripts\activate
   ```
   For linux and macOs, create your own virtual environment and enter to it.
4. Install pip.
5. Upgrade pip.
   ```sh
   pip install --upgrade pip
   ```
6. Install dependencies or requirements.
   ```sh
   pip install -r requirements.txt
   ```
## Database configuration(PostgreSQL)
In this application, I used postgreSQL to store data of todo list and user's information. You can use any other database like mysql, sqlite and MariaDB. To use these database, change configure file accordingly.
Change this line of code:
```sh
SQLALCHEMY_DATABASE_URI = os.environ.get(
   "DATABASE_URL", "postgresql://test:test@localhost:5432/test"
)
```
Here, 
Schema/protocol = postgresql://  
User credentials = [username]:[password] = test:test  
Host = localhost  
Port = 5432. It is the default port for postgreSQL.  
Database Name = test  

## Database creation and migration
You can automatically create database tables executing following command: 
```sh
flask db init
flask db migrate
flask db upgrade
```
Or, if these command doesn't work. You have to manually create database table using following SQL command:
1. Create user table: 
```sh
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY, -- Automatically increments and acts as the primary key
    email VARCHAR(100) UNIQUE, -- Unique constraint on email
    password VARCHAR(255) NOT NULL, -- Password cannot be null
    username VARCHAR(100) NOT NULL, -- Username cannot be null
    is_verified BOOLEAN DEFAULT FALSE, -- Default value is False
    verified_on TIMESTAMP NULL, -- Nullable datetime for when the user was verified
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Default is the current timestamp
    is_admin BOOLEAN NOT NULL DEFAULT FALSE -- Default value is False and cannot be null
);
```
2. Create todo table:
```sh
CREATE TABLE todo (
    id SERIAL PRIMARY KEY, -- Auto-incrementing primary key
    title VARCHAR(100) NOT NULL, -- Title cannot be null
    complete BOOLEAN, -- Boolean field to mark task completion
    created_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Default current timestamp
    priority_level VARCHAR(10) DEFAULT 'medium' NOT NULL, -- Priority with default value 'medium'
    user_id INTEGER NOT NULL, -- Foreign key for user association
    deleted BOOLEAN DEFAULT FALSE NOT NULL, -- Boolean field with default value 'false'
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES "user"(id) -- Foreign key constraint
);
```
3. Create tag table:
```sh
CREATE TABLE tag (
    id SERIAL PRIMARY KEY, -- Auto-incrementing primary key
    name VARCHAR(100) NOT NULL, -- Tag name cannot be null
    user_id INTEGER NOT NULL, -- Foreign key linking to the user table
    deleted BOOLEAN DEFAULT FALSE NOT NULL, -- Boolean field to mark if the tag is deleted
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES "user"(id) -- Foreign key constraint
);
```
4. Create todotag table:
```sh
CREATE TABLE todotag (
    id SERIAL PRIMARY KEY, -- Auto-incrementing primary key
    todo_id INTEGER NOT NULL, -- Foreign key linking to the todo table
    tag_id INTEGER NOT NULL, -- Foreign key linking to the tag table
    CONSTRAINT fk_todo FOREIGN KEY (todo_id) REFERENCES todo(id), -- Foreign key constraint for todo
    CONSTRAINT fk_tag FOREIGN KEY (tag_id) REFERENCES tag(id) -- Foreign key constraint for tag
);
```

## Usage
Now you are all set to run the app. Run the app using following command:
```sh
flask run
```
[Visit link](http://localhost:5000/login)

## Run the application using Docker Container
You can also run the application using docker container. Which is very handy to use. To do this, install docker. Uncomment the web service portion of docker-compose.yaml file. Run the following command in the terminal: 
```sh
docker-compose up --build
```
If you want to enter into the database of docker container named todoapp-db-1, execute the following command: Here database name is test.
```sh
docker exec -it todoapp-db-1 psql -U test
```

## Features of this application:

1. User authentication(Session-based)
2. User sign up / login
3. User email verification
4. Forgot password
5. Create, read, update, delete Todo items
6. Marking priority label of a todo task as high, medium, low
7. Giving tag mark to todo items.
8. Searching and filtering todo items from all todos
9. History of todo list

