import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

            question1 = Question(
                question='What is your name',
                answer='test',
                category=1,
                difficulty=1
            )
            self.db.session.add(question1)
            self.db.session.commit()
            question2 = Question(
                question='What is your last name',
                answer='mytest',
                category=1,
                difficulty=1
            )
            self.db.session.add(question2)
            self.db.session.commit()
            category = Category(
                type='Science'
            )
            self.db.session.add(category)
            self.db.session.commit()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        """
        Test if all categories can be retrieved
        """
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_paginated_questions(self):
        """
        Test if all paginated questions can be retrieved
        """
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_question(self):
        """
        Test if questions can be successfully posted
        """
        new_data = {
            'question': 'test',
            'answer': 'answerTest',
            'difficulty': 1,
            'category': 1
        }
        res = self.client().post('/questions', json=new_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_post_new_question(self):
        """
        Test if wrong post can show a 404 page
        """
        post_data = {
            'question': 'test',
            'answer': 'answerTest',
            'category': 1
        }
        res = self.client().post('/questions', json=post_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Can not find Resources")

    def test_delete_question(self):
        """
        Test if questions can be deleted
        """
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_question_404(self):
        """

        """
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_post_questions_422(self):
        """
        Test a wrong post question
        """
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_post_data_search_questions(self):
        """
        Test if questions can be successfully searched
        """
        post_data = {
            'searchTerm': 'What',
        }
        res = self.client().post('/searchQuestions?page=1', json=post_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    def test_post_search_questions_404(self):
        search_data = {
            'searchTerm': 'test',
        }
        res = self.client().post('/searchQuestions?page=100', json=search_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"], "can not find Resources")

    def test_422_post_paginated_search_questions(self):
        res = self.client().post('/searchQuestions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Can not process the request")

    def test_question_by_category(self):
        res = self.client().get('/categories/1/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_question_by_category_404(self):
        res = self.client().get('/categories/1/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data["message"], "can not find Resources")

    def test_post_play_quiz(self):
        post_data = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'Science',
                'id': 1
            }
        }
        res = self.client().post('/quizzes', json=post_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_422_post_play_quiz(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Can not process the request")

# Make the tests conveniently executable


if __name__ == "__main__":
    unittest.main()
