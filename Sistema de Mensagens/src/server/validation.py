import logging
import controllers.users as UserController

def emailValidation(email):
    if(len(email) <= 3):
        return {
            'type': 'VALIDATION/ERROR', 
            'payload': 'Nome de usuario menor do que o requisitado! O minimo requisitado eh 3.'
        }
    if(UserController.findBy_email(email) != None):
        return {
            'type': 'VALIDATION/ERROR',
            'payload': 'Usuario ja cadastrado!'
        }
    return ''