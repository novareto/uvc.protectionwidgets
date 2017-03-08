# -*- coding: utf-8 -*-

import grokcore.component as grok
from os import path
from zope.i18nmessageid import MessageFactory
from zope.component import getMultiAdapter, getUtility
from zope.interface import Interface
from zope.interface import implementer
from zope.schema import ASCIILine
from zope.schema.interfaces import IASCIILine
from norecaptcha.captcha import displayhtml, submit, VERIFY_SERVER
from ..fields import ICaptcha
#from uvc.api.api import get_template

try:
    from zeam.form.base.markers import NO_VALUE
    from zeam.form.base.widgets import WidgetExtractor
    from grokcore.chameleon.components import ChameleonPageTemplateFile
    def get_template(dir, filename):
        return ChameleonPageTemplateFile(filename, dir)

    from zeam.form.ztk.fields import (
        SchemaField, registerSchemaFi1eld, SchemaFieldWidget)
except ImportError:
    from dolmen.forms.base.markers import NO_VALUE
    from dolmen.forms.base.widgets import WidgetExtractor
    from dolmen.template import TALTemplate
    from dolmen.forms.ztk.fields import (
        SchemaField, registerSchemaField, SchemaFieldWidget)

    def get_template(filename, dir=None):
        return TALTemplate(path.join(path.dirname(dir), filename))


class IRecaptchaConfiguration(Interface):

    public_key = ASCIILine(
        title=u"Public key",
        required=True,
        )

    private_key = ASCIILine(
        title=u"Private key",
        required=True,
        )

    server = ASCIILine(
        title=u"Base API Server",
        required=False,
        default=VERIFY_SERVER,
        )

    
class IRecaptcha(IRecaptchaConfiguration):

    def display(lang):
        pass

    def validate(value, ip):
        pass


@implementer(IRecaptcha)
class Recaptcha(object):

    def __init__(self, public_key, private_key, server=VERIFY_SERVER):
        self.public_key = public_key
        self.private_key = private_key
        self.server = server

    def display(self, lang):
        return displayhtml(self.public_key, language=lang)

    def validate(self, value, ip):
        return submit(value, self.private_key, ip, verify_server=self.server)


class CaptchaSchemaField(SchemaField):

    def validate(self, value, field=None):
        return super(CaptchaSchemaField, self).validate(value)


class CaptchaFieldWidget(SchemaFieldWidget):
    grok.adapts(CaptchaSchemaField, Interface, Interface)
    template = get_template('captcha_templates/captchafieldwidget.cpt', __file__)

    def image_tag(self):
        lang = 'de'
        captcha = getUtility(IRecaptcha)
        return captcha.display(lang)


class CaptchaWidgetExtractor(WidgetExtractor):
    grok.adapts(CaptchaSchemaField, Interface, Interface)

    def extract(self):
        from uvc.api import UVCLIGHT, ENV
        if ENV is UVCLIGHT:
            value = self.request.form.get('g-recaptcha-response')
        else:
            value = self.request.get('g-recaptcha-response')
        if value:
            if ENV is UVCLIGHT:
                remote_addr = self.request.remote_addr
            else:
                remote_addr = self.request.get('HTTP_X_FORWARDED_FOR', '').split(',')[0]
                if not remote_addr:
                    remote_addr = self.request.get('REMOTE_ADDR')

            captcha = getUtility(IRecaptcha)
            res = captcha.validate(value, remote_addr)
            if res.error_code:
                return (None, _(u"Invalid captcha input."))
            return ("OK", None)
        return (value, None)


def register():
    registerSchemaField(CaptchaSchemaField, ICaptcha)
