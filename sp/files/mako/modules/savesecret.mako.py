# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1363337250.91776
_enable_loop = True
_template_filename = '/Users/haho0032/IdPproxy/src/idpsetup/files/mako/htdocs/savesecret.mako'
_template_uri = 'savesecret.mako'
_source_encoding = 'utf-8'
_exports = []


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
        home = context.get('home', UNDEFINED)
        sp = context.get('sp', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n    <p class="description">\n        The settings for ')
        # SOURCE LINE 4
        __M_writer(unicode(sp))
        __M_writer(u' have been saved.\n    </p>\n    <a href="')
        # SOURCE LINE 6
        __M_writer(unicode(home))
        __M_writer(u'">Click here to configure a new Service Provider.</a>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


