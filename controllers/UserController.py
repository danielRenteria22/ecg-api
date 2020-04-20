from app import request
from .ResponseHelper import responde
from models.User import User
from flask import session

class UserController:

    @staticmethod
    def createAccount():
        request.get_json(force=True)
        name = request.json.get("name")
        if not name: return responde(400,True,'No name was provided',None)

        email = request.json.get('email')
        if not email: return responde(400,True,'No email was provided',None)

        password = request.json.get('password')
        if not password: return responde(400,True,'No password was provided',None)

        existingUser = None
        try:
            existingUser = User.objects.raw({'email': email})[0]
        except: 
            print('User does not exists')

        if existingUser: return responde(400,True,'Email already used',None)

        try:
            newUser = User(name,email,password,False).save()
            return responde(200,False,'User was created',newUser.toJson())
        except:
            return responde(500,True,'There was an error creating the user',None)

    @staticmethod
    def login():
        email = request.json.get('email')
        if not email: return responde(400,True,'No email was provided',None)

        password = request.json.get('password')
        if not password: return responde(400,True,'No password was provided',None)

        try:    
            currentUser = User.objects.raw({'email': email, 'password': password})[0]
        except:
            return responde(401,True,'Invalid log in data',None)

        session['userId'] = str(currentUser._id)
        return responde(200,False,'Log in was succesful',currentUser.toJson())





