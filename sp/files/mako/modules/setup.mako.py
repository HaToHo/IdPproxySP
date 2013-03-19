# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1363699863.013937
_enable_loop = True
_template_filename = '/Users/haho0032/IdPproxySP/sp/files/mako/htdocs/setup.mako'
_template_uri = 'setup.mako'
_source_encoding = 'utf-8'
_exports = []


# SOURCE LINE 3

def setupEntityIdList(spList):
    optionList = ""
    for entityId in spList:
      optionList += "<option value='" + entityId + "'>" + entityId + "</option>"
    return optionList


# SOURCE LINE 11

def setupJavaScriptEntityIdArray(spList):
  first = True
  entityIdArray = "["
  for entityId in spList:
    if not first:
        entityIdArray += ","
    entityIdArray += "{'value' : '" + entityId + "','text' : '" + entityId + "'}"
    first = False
  entityIdArray += "];"
  return entityIdArray


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
        splist = context.get('splist', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 9
        __M_writer(u'\n\n')
        # SOURCE LINE 22
        __M_writer(u'\n\n    <script language="JavaScript">\n        function filterOptions(str)\n        {\n            var dataArr = ')
        # SOURCE LINE 27
        __M_writer(unicode(setupJavaScriptEntityIdArray(splist)))
        __M_writer(u'\n            //alert(dataArr[0][\'text\']);\n            //alert(\'.*\'+str+\'.*\');\n            //alert(dataArr[0][\'text\'].match(\'.*\'+str+\'.*\'));\n            $("#sp option").remove();\n            $.each(dataArr,\n                    function(i) {\n                             if (dataArr[i][\'text\'].match(\'.*\'+str+\'.*\') != null) {\n                                 $("#sp").append($("<option></option>")\n                                         .attr("value",dataArr[i][\'value\'])\n                                         .text(dataArr[i][\'text\']));\n                             }\n                    }\n            )\n        }\n\n    </script>\n\n    <p class="description">\n        Click on the entity id for the service provider you wish to configure.\n    </p>\n    <form action="')
        # SOURCE LINE 48
        __M_writer(unicode(action))
        __M_writer(u'" method="post">\n        <p>\n            <label for=\'filter\'>Filter SP\'s</label><br />\n            <input type=\'text\' class=\'inputValue\' onkeyup="filterOptions(this.value)" name=\'filter\' id=\'filter\' value=\'\'/>\n            <br />\n            <label for="sp">Service Provider</label><br />\n            <select name=\'sp\' id="sp" size=30>")\n                ')
        # SOURCE LINE 55
        __M_writer(unicode(setupEntityIdList(splist)))
        __M_writer(u'\n            </select>\n        </p>\n        <input class="submit" type="submit" name="form.submitted" value="Next >"/>\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


