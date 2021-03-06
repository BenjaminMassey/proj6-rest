# Laptop Service

from flask import Flask
from flask_restful import Resource, Api

# Instantiate the app
app = Flask(__name__)
api = Api(app)

class Laptop(Resource):

    def get(self):
        return {
            'Laptops': [
				'I', 
				'do', 
				'not',
				'understand',
				'what',
				'you',
				'want'
            ]
        }

# Create routes
# Another way, without decorators
api.add_resource(Laptop, '/')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
