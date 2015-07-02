import webapp2
import os
import jinja2
from funcoes import senhaValida
from funcoes import emailValido
#from funcoes import escape_html
from google.appengine.ext import db
from google.appengine.api import mail


JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"))

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
        user_email = self.request.get('email')
        user_senha = self.request.get('senha')

        email = emailValido(user_email)
        senha = senhaValida(user_senha)

        self.query = FaceUffBD.all()
        for self.faceuff in self.query:
            if((self.faceuff.email == email) and (self.faceuff.senha == senha)):
                self.response.out.write("logged as: %s, email: %s" % (self.faceuff.nome, self.faceuff.email))
                break

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

"""
class EditarPerfilHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('editarPerfil-v2.html')
        self.response.out.write(template.render())
    def post(self):
   """


app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/criarConta-v2.html', CriarContaHandler),
                               ('/recuperarSenha.html', RecuperarSenhaHandler)],
                              debug=True)
