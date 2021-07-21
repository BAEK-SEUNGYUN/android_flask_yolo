from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

# Flask 인스턴스 정리
app = Flask(__name__)
api = Api(app)

# 웹화면에 띄울 json
Todos = {
    'todo1': {"task": "exercise"},
    'todo2': {'task': "eat delivery food"},
    'todo3': {'task': 'watch movie'}
}

# json을 반환하는 클래스
class TodoList(Resource):
    def get(self):
        return Todos


# api 에 반환값이 있는 클래스와 그 반환값이 나타날 경로를 입력
api.add_resource(TodoList, '/todos/')

# 서버를 실행할 host 와 port

if __name__ == '__main__':
    app.run(host="본인 컴퓨터 IP주소", port=5000, debug=True)