from jwt import encode as cod, decode as dcod

SECRET_KEY = 'UM_CODIGO_SUPER_SECRETO_PRA_NINNGUEM_HACKEAR_A_GENTE'
ALGORITHM  = 'HS256'

def encode(payload):
    return cod(payload, SECRET_KEY, algorithm=ALGORITHM).decode("utf-8")

def decode(encoded):
    return dcod(encoded, SECRET_KEY, algorithms=[ALGORITHM])
    
