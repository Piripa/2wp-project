import hashlib


def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


def comparar_senhas(hash_senha, senha_usuario):
    if hash_senha == hashlib.sha256(senha_usuario.encode()).hexdigest():
        return True
    else:
        return False