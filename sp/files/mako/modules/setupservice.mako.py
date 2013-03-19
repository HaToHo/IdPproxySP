# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1363356403.044068
_enable_loop = True
_template_filename = '/Users/haho0032/IdPproxySP/sp/files/mako/htdocs/setupservice.mako'
_template_uri = 'setupservice.mako'
_source_encoding = 'utf-8'
_exports = []


# SOURCE LINE 3

def setupServiceList(serviceList):
    htmlOutput = ""
    for service in serviceList:
      serviceName = service.keys()[0]
      settingsExists = service[serviceName]
      htmlOutput += "<p><span class='service'>" + serviceName + "</span><br />"
      hiddenKey = ""
      if settingsExists:
          hiddenKey = "********************"
      htmlOutput += "<input type='hidden' id='service' name='service' value='" + serviceName + "' />"
      htmlOutput += "<label for='secret'>Secret</label><br /><input type='text' class='inputValue' name='secret' id='secret' value='" + hiddenKey + "'/><br />"
      htmlOutput += "<label for='key'>Key</label><br /><input type='text' class='inputValue' name='key' id='key' value='" + hiddenKey + "'/><br />"
      htmlOutput += "</p>"
    return htmlOutput


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'root.mako', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        action = context.get('action', UNDEFINED)
        sociallist = context.get('sociallist', UNDEFINED)
        back = context.get('back', UNDEFINED)
        sp = context.get('sp', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 18
        __M_writer(u'\n\n\n    <script>\n        function setupInputFields() {\n            //$(":text:not([value])").val(" ");\n            $(\'form\').find("input[type=text]").each(function(ev) {\n                if($(this).val()==\'\') { $(this).val(\' \'); }\n            });\n\n\n        }\n    </script>\n\n    <p class="description">\n        Follow the guid at <a href="https://portal.nordu.net/display/SWAMID/Social2SAML">SWAMID</a> to retrive secret and key for the social service you which to configure.<br />\n        <br/>\n        Clear key and secret for a service if you wish to remove it from the IdPproxy.<br />\n        <br />\n        If a field contains ******************** it is already configured. Leave it if you do not wish to change it.\n    </p>\n    <form action="')
        # SOURCE LINE 39
        __M_writer(unicode(action))
        __M_writer(u'" method="post">\n        ')
        # SOURCE LINE 40
        __M_writer(unicode(setupServiceList(sociallist)))
        __M_writer(u'\n        <input type="hidden" id="sp" name="sp" value="')
        # SOURCE LINE 41
        __M_writer(unicode(sp))
        __M_writer(u'" />\n        <input class="back" type="button" onclick="window.location.href = \'')
        # SOURCE LINE 42
        __M_writer(unicode(back))
        __M_writer(u'\'" name="form.submitted" value="< Back"/>\n        <input class="submit" type="submit" onclick="setupInputFields();" name="form.submitted" value="Save changes >"/>\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


