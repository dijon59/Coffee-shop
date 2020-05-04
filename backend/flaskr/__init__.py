from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        header = response.headers
        header['Access-Control-Allow-Origin'] = '*'
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        """
        Get all categories
        """
        categories = [category.format() for category in Category.query.all()]

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories
        })

    @app.route('/questions', methods=['GET'])
    def get_questions():
        """
        Get all the questions
        """
        try:
            page = int(request.args.get('page'))
            questions = [question.format() for question in Question.query.order_by(Question.id).all()]
            categories = [category.format() for category in Category.query.all()]
            paginated_question = Question.query.paginate(page, QUESTIONS_PER_PAGE, False)

            if len(questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions_num': len(questions),
                'questions': questions,
                'total_questions': paginated_question.total,
                'categories': categories,
                'current_category': None,
            })
        except:
            abort(404)

    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """
        Delete question
        """
        question = Question.query.get(question_id)
        try:
            Question.delete(question)
            return jsonify({
                "success": True,
            })
        except:
            abort(404)

    @app.route('/questions', methods=['POST'])
    def post_questions():
        """
        post questions
        """
        if request.data:
            question_form_data = request.get_json()
            if 'question' in question_form_data and 'answer' in question_form_data and \
                    'difficulty' in question_form_data and 'category' in question_form_data:
                question = Question(
                    question=question_form_data['question'],
                    answer=question_form_data['answer'],
                    category=question_form_data['category'],
                    difficulty=question_form_data['difficulty']
                )
                question.insert()

                return jsonify({
                    'success': True,
                })
            abort(404)
        abort(422)

    @app.route("/searchQuestions", methods=['POST'])
    def search_questions():
        """
        search questions
        """
        if request.data:
            page = int(request.args.get('page'))
            search_term = request.get_json()
            if 'searchTerm' in search_term:
                question_qs = Question.query.filter(Question.question.ilike('%' + search_term['searchTerm'] + '%')) \
                    .paginate(page, QUESTIONS_PER_PAGE, False)
                questions = [question.format() for question in question_qs.items]
                if len(questions) > 0:
                    return jsonify({
                        "success": True,
                        "questions": questions,
                        "total_questions": question_qs.total,
                        "current_category": None,
                    })
            abort(404)
        abort(422)

    @app.route('/categories/<int:category_id>/questions')
    def get_question_by_category(category_id):
        """
        Get questions by category
        """
        category_obj = Category.query.get(category_id)
        page = int(request.args.get('page'))
        categories = [category.format() for category in Category.query.all()]
        questions_qs = Question.query.filter_by(category=category_id).paginate(page, QUESTIONS_PER_PAGE, False)
        questions = [question.format() for question in questions_qs.items]
        if len(questions) == 0:
            abort(404)
        else:
            return jsonify({
                "success": True,
                "questions": questions,
                "total_questions": questions_qs.total,
                "categories": categories,
                "current_category": Category.format(category_obj),
            })

    @app.route('/quizzes', methods=['POST'])
    def get_question_quiz():
        """
        Get quiz questions
        """

        try:
            searched_data = request.get_json()
            questions_qs = Question.query.filter_by(category=searched_data['quiz_category']['id']).filter(
                Question.id.notin_(searched_data['previous_questions'])).all()

            question_length = len(questions_qs)
            if question_length > 0:
                return jsonify({
                    'success': True,
                    'question': Question.format(
                        questions_qs[random.randrange(0, question_length)]
                    )
                })
            else:
                return jsonify({
                    'success': True,
                    'question': None
                })
        except:
            abort(422)

    ## Error Handling ##

    @app.errorhandler(404)
    def not_found(error):
        error_data = {
            "success": False,
            'error': 404,
            'message': 'Can not find Resources'
        }
        return jsonify(error_data), 404

    @app.errorhandler(422)
    def unprocessable_request(error):
        error_data = {
            "success": False,
            "error": 422,
            "message": "Can not process the request"
        }
        return jsonify(error_data), 422
    return app
