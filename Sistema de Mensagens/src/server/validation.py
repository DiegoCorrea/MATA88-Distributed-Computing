import logging

def loginValidation(loginName):
    if(len(loginName) <= 3):
        return {
            'type': 'VALIDATION/TOOSMALL', 
            'payload': 'Nome de usuario menor do que o requisitado! O minimo requisitado eh 3.'
        }
    return ''