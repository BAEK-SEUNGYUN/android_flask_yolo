from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

# Flask 인스턴스 정리
app = Flask(__name__)
api = Api(app)

#할 일 목록들
Todos = {
    'todo1': {"task": "exercise"},
    'todo2': {'task': "eat delivery food"},
    'todo3': {'task': 'watch movie'}
}

class TodoList(Resource):
    def get(self):
        return Todos

api.add_resource(TodoList, '/todos/')

if __name__ == '__main__':
    app.run(host="192.168.0.3", port=5000, debug=True)