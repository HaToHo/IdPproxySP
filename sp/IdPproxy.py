from urlparse import parse_qs
from saml2.mdstore import MetadataStore

__author__ = 'Hans Hoerberg'

import os
import sys
import time
import xmldsig
import xmlenc
import json

from rb.authorization import DeclarativeAuth
from repoze.who.config import make_middleware_with_config
from saml2.httputil import Unauthorized, Response, NotFound
from saml2 import time_util
from saml2 import attribute_converter
from saml2 import saml
from saml2.extension import mdui
from saml2.extension import idpdisc
from saml2.extension import dri
from saml2.extension import mdattr
from saml2.extension import ui
from saml2 import md
from saml2.sigver import get_xmlsec_binary
from mako.lookup import TemplateLookup
from idpproxy import utils

class IdpSetupSp(object):

    spKeyList = []
    socialServiceKeyList = []

    #File that contains secret configuration, if not metadata file is used.
    secretFile = ""

    #Contains the singleton
    _instance = None

    def __init__(self):
        """
        Will initialize the declarative authorization from a json file.
        :param authSetupFile:
        """


    @staticmethod
    def getInstance():
        """
        Get the instance for the class.
        """
        if not IdpSetupSp._instance:
            IdpSetupSp._instance = IdpSetupSp()
        return IdpSetupSp._instance


    def initAuthApp(self, application, metadataList, conf, secretFile, configfilePath=None):
        """
        Will add authentication middleware to the WSGI application.

        :param self:
        :param application: Function for main WSGI application
        :rtype : PluggableAuthenticationMiddleware
        :return:
        """

        self.CONST_SETUP = "/setup"
        self.CONST_SETUPSERVICE = "/setup/service"
        self.CONST_SETUPSTYLES = "/setup/styles"
        self.CONST_SAVESECRET = "/setup/SaveSecret"
        self.CONST_SETUPABOUT = "/setup/about"
        self.CONST_SETUPLOGUT = "/setup/logout"
        self.CONST_SESSION_USER = "_cp_uid"

        self.CONST_KEY = "key"
        self.CONST_SECRET = "secret"

        if configfilePath is None:
            self.CONST_ROOT = os.path.dirname(os.path.abspath(__file__))
        else:
            self.CONST_ROOT = configfilePath

        self.CONST_AUTH_FILE = IdpSetupSp._instance.CONST_ROOT + "/auth.json"
        self.CONST_STATIC_FILE = IdpSetupSp._instance.CONST_ROOT + "/files/static/"
        self.CONST_STATIC_MAKO = IdpSetupSp._instance.CONST_ROOT + "/files/mako/"
        self.CONST_LOOKUP = TemplateLookup(directories=[self.CONST_STATIC_MAKO + 'templates', self.CONST_STATIC_MAKO + 'htdocs'],
                                           module_directory=self.CONST_STATIC_MAKO + 'modules',
                                           input_encoding='utf-8', output_encoding='utf-8')

        self.CONST_ONTS = {
            saml.NAMESPACE: saml,
            mdui.NAMESPACE: mdui,
            mdattr.NAMESPACE: mdattr,
            dri.NAMESPACE: dri,
            ui.NAMESPACE: ui,
            idpdisc.NAMESPACE: idpdisc,
            md.NAMESPACE: md,
            xmldsig.NAMESPACE: xmldsig,
            xmlenc.NAMESPACE: xmlenc
        }

        self.CONST_ATTRCONV = attribute_converter.ac_factory("attributemaps")


        try:
            xmlsec_path = get_xmlsec_binary(["/opt/local/bin"])
        except:
            try:
                xmlsec_path = get_xmlsec_binary(["/usr/local/bin"])
            except:
                xmlsec_path = '/usr/bin/xmlsec1'

        for metadata in metadataList:
            mds = MetadataStore(self.CONST_ONTS.values(), self.CONST_ATTRCONV, xmlsec_path,
                                disable_ssl_certificate_validation=True)
            mds.imp(metadata)
            for entityId in mds.keys():
                self.spKeyList.append(entityId)

        for key in conf:
            self.socialServiceKeyList.append(conf[key]["name"])

        self.secretFile = secretFile

        currentPath = os.path.dirname(os.path.abspath(__file__))
        lib_path = os.path.abspath(self.CONST_ROOT)
        sys.path.append(lib_path)
        DeclarativeAuth.getInstance(self.CONST_AUTH_FILE)
        app_with_auth = make_middleware_with_config(application, {"here": "."},
                                                    self.CONST_ROOT+'/who.ini',
                                                    log_file=self.CONST_ROOT+"/repoze_who.log")
        return app_with_auth


    def expiration(self, timeout, tformat="%a, %d-%b-%Y %H:%M:%S GMT"):
        """

        :param timeout:
        :param tformat:
        :return:
        """
        if timeout == "now":
            return time_util.instant(tformat)
        elif timeout == "dawn":
            return time.strftime(tformat, time.gmtime(0))
        else:
            # validity time should match lifetime of assertions
            return time_util.in_a_while(minutes=timeout, format=tformat)

    def unauthorized(self, environ, start_response):
        """
        WSGI application method that will force saml authentication according to pysaml2.
        :param environ:
        :param start_response:
        :return: An unauthorized unknown user.
        """
        resp = Unauthorized('Unknown user')
        return resp(environ, start_response)


    def verifyHandleRequest(self, path):
        return DeclarativeAuth.getInstance().ruleMatch(path)

    def getQueryDict(self, environ):
        query = environ.get('s2repoze.body', ' ')
        if not query:
            query = environ.get("QUERY_STRING", "")

        qs = dict( (k, v if len(v)>1 else v[0] )
                   for k, v in parse_qs(query).iteritems() )
        return qs


    def handleRequest(self, environ, start_response, path, consumer_info):
        """
        Will handle the setup of the Idp.
        The user must be authenticated.
        :param environ:
        :param start_response:
        :param filePath:
        :return:
        """
        identity = None
        try:
            identity = environ["repoze.who.identity"]["user"]
        except:
            return self.unauthorized(environ, start_response)
        #try:
        if identity is None or len(identity) == 0:
            return self.unauthorized(environ, start_response)
        elif DeclarativeAuth.getInstance().userMatchRule(path, identity["uid"][0]):
            qs = self.getQueryDict(environ)
            if path == self.CONST_SETUPLOGUT:
                return self.handleLogout(environ, start_response)
            if path == self.CONST_SETUPABOUT:
                return self.handleAbout(environ, start_response)
            elif path == self.CONST_SETUPSTYLES:
                return self.handleStyles(environ, start_response)
            elif path == self.CONST_SETUP:
                return self.handleSetup(environ, start_response)
            elif path == self.CONST_SETUPSERVICE:
                return self.handleSetupService(environ, start_response, qs, consumer_info)
            elif path == self.CONST_SAVESECRET:
                return self.handleSaveSecret(environ, start_response, qs)
            else:
                return self.handleUnknown(environ, start_response, path)
        else:
            return self.handleNotAuthorized(environ, start_response)
        #except Exception as e:
        #        resp = self.handleUnknownError(environ, start_response, path)


    def handleStyles(self, environ, start_response):
        return self.static(environ, start_response, self.CONST_STATIC_FILE + "/style.css")

    def handleLogout(self, environ, start_response):
        return self.static(environ, start_response, self.CONST_STATIC_FILE + "/help.html")

    def handleAbout(self, environ, start_response):
        return self.static(environ, start_response, self.CONST_STATIC_FILE + "/help.html")

    def handleUnknownError(self, environ, start_response):
        return self.static(environ, start_response, self.CONST_STATIC_FILE + "/unknownError.html")

    def handleNotAuthorized(self, environ, start_response):
        return self.static(environ, start_response, self.CONST_STATIC_FILE + "/notAuth.html")

    def handleUnknown(self, environ, start_response, path):
        return self.static(environ, start_response, self.CONST_STATIC_FILE + "/unknown.html")

    def handleSetupService(self, environ, start_response, qs, consumer_info):
        resp = Response(mako_template="setupservice.mako", template_lookup=self.CONST_LOOKUP,
                        headers=[])
        #('Content-Type', 'text/html')
        entityId = qs["sp"]
        serviceList = []
        #This code reads all settings (metadata and secrets file), but this SP only supports the secret file so far.
        #for service in self.socialServiceKeyList:
        #    settingExist = False
        #    try:
        #        consumer_info(service,entityId)
        #        settingExist = True
        #    except KeyError as e:
        #        pass
        #    serviceList.append({service : settingExist})

        secretData = None
        if self.secretFile is not None:
            with open(self.secretFile) as fileData:
                try:
                    secretData = json.load(fileData)
                except:
                    #Log "Not a correct JSON syntax!"
                    pass
        for service in self.socialServiceKeyList:
            settingExist = False
            if secretData is not None and entityId in secretData and service in secretData[entityId]:
                settingExist = True
            serviceList.append({service : settingExist})

        argv = {
            "action": self.CONST_SAVESECRET,
            "back": self.CONST_SETUP,
            "sp": entityId,
            "sociallist": serviceList
        }
        return resp(environ, start_response, **argv)


    def handleSetup(self, environ, start_response):
        resp = Response(mako_template="setup.mako", template_lookup=self.CONST_LOOKUP,
                        headers=[])
        #('Content-Type', 'text/html')
        argv = {
            "action": self.CONST_SETUPSERVICE,
            "splist": self.spKeyList,
            "sociallist": self.socialServiceKeyList
        }
        return resp(environ, start_response, **argv)

    def handleSaveSecret(self, environ, start_response, qs):
        resp = Response(mako_template="savesecret.mako", template_lookup=self.CONST_LOOKUP,
                        headers=[])

        secretData = None
        if self.secretFile is not None:
            with open(self.secretFile) as fileData:
                try:
                    secretData = json.load(fileData)
                except:
                    #Log "Not a correct JSON syntax!"
                    pass

        secretDataNew = {}
        noChange = "********************"
        entityId = qs["sp"]
        if secretData is None:
            secretData = secretDataNew
        for secretEntityId in secretData:
            secretDataNew[secretEntityId] = secretData[secretEntityId]

        if entityId not in secretDataNew:
            secretDataNew[entityId] = {}

        for i, service in enumerate(qs["service"]):
            secret = qs["secret"][i].strip()
            key = qs["key"][i].strip()
            if secret == "" or key == "":
                if entityId in secretDataNew and service in secretDataNew[entityId]:
                    del secretDataNew[entityId][service]
            else:
                if entityId in secretData and service in secretData[entityId]:
                    secretDataNew[entityId][service] = secretData[entityId][service]
                else:
                    secretDataNew[entityId][service] = {}
                if secret != noChange:
                    secretDataNew[entityId][service][self.CONST_SECRET] = secret
                if key != noChange:
                    secretDataNew[entityId][service][self.CONST_KEY] = key

        if len(secretDataNew[entityId]) == 0:
            del secretDataNew[entityId]

        if self.secretFile is not None:
            with open(self.secretFile, 'w') as outfile:
                json.dump(secretDataNew, outfile)

        #('Content-Type', 'text/html')
        argv = {
            "home": self.CONST_SETUP,
            "sp": entityId
        }
        return resp(environ, start_response, **argv)

    def static(self, environ, start_response, path):
        try:
            text = open(path).read()
            if path.endswith(".ico"):
                resp = Response(text, headers=[('Content-Type', "image/x-icon")])
            elif path.endswith(".html"):
                resp = Response(text, headers=[('Content-Type', 'text/html')])
            elif path.endswith(".txt"):
                resp = Response(text, headers=[('Content-Type', 'text/plain')])
            elif path.endswith(".css"):
                resp = Response(text, headers=[('Content-Type', 'text/css')])
            else:
                resp = Response(text, headers=[('Content-Type', 'text/xml')])
        except IOError:
            resp = NotFound()
        return resp(environ, start_response)




