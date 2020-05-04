# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

Here are the features of the application:

1) Display questions 
2) Delete questions.
3) Add questions and answers if the questions
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category.  

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.
Make sure that you have a virtual environment before installing all the dependencies packages. if you don't have it please
run the following command: `virtualenv venv` and in order to have access to your virtualenv environment run the following
command: `$source venv/bin/activate`

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000. 

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality. 

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

## Error Handling

Errors are returned as JSON objects in the following format:
```
{
    "success": False,
    "error": 404,
    "message": 'Can not find Resources'
}
```
The API will return two errors types when the requests fail:

- 404: Can not find Resources
- 422: Can not process the request

## Endpoints
#### GET `/categories`
This endpoint returns a list of categories
- sample: `curl http://127.0.0.1:5000/categories`
```
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Games"
    }, 
    {
      "id": 3, 
      "type": "Art"
    }
  ], 
  "success": true
}
```
#### GET `/questions`
this endpoint returns a list of questions
- sample: `curl http://127.0.0.1:5000/questions?page=1`
```
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Games"
    }, 
    {
      "id": 3, 
      "type": "Art"
    }
  ], 
  "current_category": null, 
  "questions": [
    {
      "answer": "frank", 
      "category": 1, 
      "difficulty": 1, 
      "id": 6, 
      "question": "what is your name"
    }, 
    {
      "answer": "trump", 
      "category": 1, 
      "difficulty": 1, 
      "id": 7, 
      "question": "what is your last name"
    }, 
  ], 
  "questions_num": 2, 
  "success": true, 
  "total_questions": 2
}
```
#### DELETE `/questions/<question_id>`
this endpoint returns true if successfully deleted
- sample : `curl -X DELETE  http://127.0.0.1:5000/questions/10?page=1`
```
{"success": true}
```
#### POST `/questions`
This endpoint create a new question and returns true if successfully created 
- sample: `curl  http://127.0.0.1:5000/questions?page=1 -X POST -H "Content-Type: application/json" -d '{"question": "what is your surname", "answer": "frank", "difficulty": 1, "category": 1}'`
'

```
{"success": true }
```
### POST `/searchQuestions?page=1`
This API returns a list of questions, number of total questions and current category.

Example Request Payload
```{"searchTerm":"a"}```
response
```
{
  "current_category": null, 
  "questions": [
    {
      "answer": "frank", 
      "category": 3, 
      "difficulty": 1, 
      "id": 14, 
      "question": "what is your name"
    }, 
    {
      "answer": "dijon", 
      "category": 3, 
      "difficulty": 1, 
      "id": 15, 
      "question": "What is your surname"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```
#### GET `/categories/<int:category_id>/questions`
This endpoint returns a list of question by categories
-sample: `curl  http://127.0.0.1:5000/categories/3/questions?page=1`
```
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Games"
    }, 
    {
      "id": 3, 
      "type": "Art"
    }
  ], 
  "current_category": {
    "id": 3, 
    "type": "Art"
  }, 
  "questions": [
    {
      "answer": "frank", 
      "category": 3, 
      "difficulty": 1, 
      "id": 14, 
      "question": "what is your name"
    }, 
    {
      "answer": "dijon", 
      "category": 3, 
      "difficulty": 1, 
      "id": 15, 
      "question": "What is your surname"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```

#### POST `/quizzes`
- To get questions to play the quiz.
- Returns: Random questions within the given category.

Example Request Payload
```
{"previous_questions":[],"quiz_category":{"type":"sport","id":1}}
```

Example Response
```
{"question":{"answer":"Leo Messi","category":1,"difficulty":4,"id":22,"question":"Who is the best soccer player"},"success":true}
```
