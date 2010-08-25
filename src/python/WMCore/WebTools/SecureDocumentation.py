from cherrypy import expose, tools
import cherrypy
from WMCore.WebTools.Page import TemplatedPage
from os import listdir

def check_authz(permissions, fullname, dn):
    if (permissions.get('Admin',None) == 'T2_BR_UERJ') or \
           (permissions.get('L2',None) == 'CMS DMWM'):
        if fullname != 'Bad guy':
            return True # authorized
    return False

class SecureDocumentation(TemplatedPage):
    """
    The documentation for the framework
    """
    @expose
    @tools.cernoid()
    def index(self):
        templates = listdir(self.templatedir)
        oidinfo = cherrypy.session['SecurityModule']
        index = "<h1>Secure Documentation</h1>"
        index += "<div>\n"
        index += "Hello <b>%s</b>!\n" % oidinfo['fullname']
        index += "<ul>\n"
        index += "<li>Your <b>ID</b>: <a href='%s'>%s</a></li>\n" % \
                (oidinfo['openid_url'], oidinfo['openid_url'])
        index += "<li>Your <b>DN</b>: %s</li>\n" % oidinfo['dn']
        index += "<li>Your roles:\n"
        index += "<ul>\n"
        for k in oidinfo['permissions'].keys():
            index += "<li><b>%s</b>: %s</li>\n" % (k, oidinfo['permissions'][k])
        index += "</ul></li></ul>\n"
        index += "</div>\n"
        index += "<ol>"
        for t in templates:
            if '.tmpl' in t:
                index = "%s\n<li><a href='%s'>%s</a></li>" % (index, 
                                                      t.replace('.tmpl', ''), 
                                                      t.replace('.tmpl', ''))
        index = "%s\n<li><a href='https://twiki.cern.ch/twiki/bin/view/CMS/DMWebtools'>twiki</a>" % (index)
        index = "%s\n</ol>" % (index)
        return index

    @expose
    @tools.cernoid(authzfunc=check_authz)
    def SpecialDocs(self):
        return "This is a secret documentation for special docs"

    @expose
    @tools.cernoid()
    def UerjDocs(self):
        return "This is a secret documentation about the T2 UERJ site"

    @expose
    @tools.cernoid()
    def CernDocs(self):
        return "This is a secret documentation about the T1 CERN site"

    @expose
    def default(self, *args, **kwargs):
        if len(args) > 0:
            return self.templatepage(args[0])
        else:
            return self.index()

