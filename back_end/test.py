from flask import Flask,request

api = Flask(__name__)

@api.route('/robot', methods=['GET'])
def robot():
    robot= {
        "name": "Robot",
        "version": "1.0",
        "description": "This is a robot API",
    }
    field = request.args.get('field', default='name', type=str)
    if field == 'name':
        return robot['name'], 200, {'Content-Type': 'text/plain'}
    elif field == 'version':
        return robot['version'], 200, {'Content-Type': 'text/plain'}
    elif field == 'description':
        return robot['description'], 200, {'Content-Type': 'text/plain'}
    elif field == 'robot':
        return robot, 200, {'Content-Type': 'application/json'}
    else:   
        return {"error": "Field not found"}, 404

if __name__ == '__main__':
    api.run(debug=True, port=5000, host='0.0.0.0')