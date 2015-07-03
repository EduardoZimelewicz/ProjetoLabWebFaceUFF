import webapp2
import os
import jinja2
from funcoes import senhaValida
from funcoes import emailValido
from google.appengine.ext import db
from google.appengine.api import mail


JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"))

USER_NOME = 0
USER_IDADE = 0
USER_CURSO = 0
USER_EMAIL = 0

class FaceUffBD(db.Model):
    nome = db.StringProperty(required=True)
    idade = db.IntegerProperty(required=True)
    curso = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)
    senha = db.StringProperty(required=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('login-v2.html')
        self.response.out.write(template.render())

    def post(self):

        global USER_EMAIL
        USER_EMAIL = self.request.get('email')

        senha = self.request.get('senha')

        email = emailValido(USER_EMAIL)
        senha = senhaValida(senha)

        self.query = FaceUffBD.all()
        for self.faceuff in self.query:
            if((self.faceuff.email == email) and (self.faceuff.senha == senha)):
                global USER_NOME
                USER_NOME = self.faceuff.nome
                global USER_IDADE
                USER_IDADE = self.faceuff.idade
                global USER_CURSO
                USER_CURSO = self.faceuff.curso
                self.redirect("/perfil.html")
                break
        self.response.out.write("There is no such account")

class CriarContaHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('criarConta-v2.html')
        self.response.out.write(template.render())

    def post(self):
        nomeUsuario = self.request.get('nome')
        idadeUsuario = int(self.request.get('idade'))
        cursoUsuario = self.request.get('curso')
        emailUsuario = self.request.get('email')
        senhaUsuario = self.request.get('senha')
        senhaconfUsuario = self.request.get('senhaConf')

        user_email = emailValido(emailUsuario)
        user_senha = senhaValida(senhaUsuario)

        if not(user_email and user_senha and (user_senha == senhaconfUsuario)):
            self.response.out.write("Cannot add user to DB")
        else:
            novousuario = FaceUffBD(nome=nomeUsuario, email=emailUsuario, senha=senhaUsuario, idade=idadeUsuario,
                                    curso=cursoUsuario)
            novousuario.put()
            self.redirect("/")

class RecuperarSenhaHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('recuperarSenha.html')
        self.response.out.write(template.render())
    def post(self):
        user_email = self.request.get('email')
        mail.send_mail(sender="Eduardo<eduardo.zimelewicz@gmail.com>", to=user_email, subject="teste",
                       body="Hello user!")
        self.redirect("/")


class PerfilHandler(webapp2.RequestHandler):
    def get(self):
        templates = {"nome":USER_NOME,"idade":USER_IDADE,"curso":USER_CURSO}
        template = JINJA_ENVIRONMENT.get_template('perfil.html')
        self.response.out.write(template.render(templates))

    def post(self):
        self.redirect("/editarPerfil-v2.html")

class EditarPerfil(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('editarPerfil-v2.html')
        self.response.out.write(template.render())

    def post(self):
        nomeUsuario = self.request.get('nome')
        idadeUsuario = int(self.request.get('idade'))
        cursoUsuario = self.request.get('curso')
        senhaUsuario = self.request.get('novaSenha')
        senhaconfUsuario = self.request.get('senhaConf')

        if(senhaconfUsuario == senhaUsuario):
            self.query = FaceUffBD.all()
            for self.faceuff in self.query:
                if((self.faceuff.email == USER_EMAIL)):
                    self.faceuff.delete()
                    usuarioEditado = FaceUffBD(nome=nomeUsuario, email=USER_EMAIL, senha=senhaUsuario,
                                               idade=idadeUsuario,
                                               curso=cursoUsuario)
                    usuarioEditado.put()
                    self.redirect("/")
                    break
        self.response.out.write("password do not match")

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/login-v2.html', MainHandler),
                               ('/criarConta-v2.html', CriarContaHandler),
                               ('/recuperarSenha.html', RecuperarSenhaHandler),
                               ('/perfil.html', PerfilHandler),
                               ('/editarPerfil-v2.html', EditarPerfil)],
                              debug=True)
