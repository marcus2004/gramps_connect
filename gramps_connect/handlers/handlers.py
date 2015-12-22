import tornado.web

from gramps.gen.utils.grampslocale import GrampsLocale, _
from gramps.gen.dbstate import DbState

db = DbState().open_database("Gramps Connect")

template_functions = {}
exec("from gramps_connect.template_functions import *", 
     globals(), template_functions)

class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ = _

    def get_current_user(self):
        return self.get_secure_cookie("user")
		
    def set_language(self, language):
        if language == GrampsLocale.DEFAULT_TRANSLATION_STR:
            language = None
        locale = GrampsLocale(lang=language)
        self._ = locale.translation.gettext
 
    def get_template_dict(self, **kwargs):
        dict = {
            "action": "", 
            "menu": [], 
            "user": self.current_user, 
            "sitename": "SITENAME",
            "css_theme": "Web_Mainz.css",
            "gramps_version": "5.0",
            "messages": [],
            "_": self._,
            "next": self.get_argument("next", None),
        }
        dict.update(kwargs)
        dict.update(template_functions)
        return dict

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        #self.write(self._("Person"))
        self.render('index.html', **self.get_template_dict())

class LoginHandler(BaseHandler):
    def get(self):
        self.set_language("fr_FR.UTF-8")
        self.render('login.html', 
                    **self.get_template_dict())
    def post(self):
        getusername = self.get_argument("username")
        getpassword = self.get_argument("password")
        # TODO : Check data from DB
        if "demo" == getusername and "demo" == getpassword:
            self.set_secure_cookie("user", self.get_argument("username"))
            self.redirect(self.get_argument("next", 
                                            self.reverse_url("main")))
        else:
            wrong = self.get_secure_cookie("wrong")
            if not wrong:
                wrong = 0
            self.set_secure_cookie("wrong", str(int(wrong)+1))
            self.write('Something Wrong With Your Data <a href="/login">Back</a> '+str(wrong))

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", 
                                        self.reverse_url("main")))

class PersonHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, user):
        person = db.get_person_from_gramps_id("I0000")
        person.probably_alive = True
        self.render("view_person_detail.html", 
                    **self.get_template_dict(tview="person", 
                                             person=person,
                                             logform=None))
