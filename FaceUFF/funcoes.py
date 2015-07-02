__author__ = 'Eduardo'
import cgi

def emailValido(email):
        if email != "":
            if len(email) < 10:
                return None
            return email
        return None

def senhaValida(senha):
        if senha != "":
            if len(senha) < 5:
                return None
            return senha
        return None

def escape_html(s):
    return cgi.escape(s, quote=True)

