# Assignment 2: RESTful microservices architectures
This is a simple URL shortener service implemented in Python using the Flask web framework. The service allows users to shorten long URLs into unique and compact identifiers, making them easier to share and manage. Firstly, users need to create an account with unique 'username' and 'password', then login to get a JWT token. With the token, users are able to manipulating their urls.
## Getting Started
1. Install the required dependencies(flask and requests):
```
pip install -r requirements.txt
```
2. Run the Flask web server:
```
python(3) URL_shortening.py
python(3) auth_service.py
```
3. The url-shortening service will start running locally on http://127.0.0.1:5000/
 
4.   The authentication service will start running locally on http://127.0.0.1:5001/
   
5. Run the test file:
```
python(3) -s test_1_marking_mk2.py
python(3) test_auth.py
```
