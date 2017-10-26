# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de
#

import binascii

from os import urandom
from zeam.form.base import Fields
from zope import interface, schema
from uvc.protectionwidgets import MF as _
from zope.session.interfaces import ISession


class IInvalidCSRFToken(interface.Interface):

    def doc():
        """The form submit could not be handled as the CSRF token is missing
        or incorrect.
        """


@interface.implementer(IInvalidCSRFToken)
class InvalidCSRFToken(Exception):
    """The form submit could not be handled as the CSRF token is missing
    or incorrect.
    """


class CSRFTokenGenerationError(Exception):
    """The form submit could not be save or load the CSRF token.
    """


def getSession(request):
    return ISession(request)['CSRF_PROTECTION']


class CSRFMixin(object):

    def setUpToken(self):
        session = getSession(self.request)
        if session is None:
            raise CSRFTokenGenerationError("No session.")
        self.csrftoken = session.get('__csrftoken__')
        if self.csrftoken is None:
            self.csrftoken = str(binascii.hexlify(urandom(32)))
            session['__csrftoken__'] = self.csrftoken

    def checkToken(self):
        session = getSession(self.request)
        if session is None:
            raise CSRFTokenGenerationError("No session.")
        cookietoken = session.get('__csrftoken__')
        if cookietoken is None:
            raise InvalidCSRFToken(_('Invalid CSRF token'))
        if cookietoken != self.request.form.get('form.field.__csrftoken__', None):
            raise InvalidCSRFToken(_('Invalid CSRF token'))

    def get_csrftoken(self):
        return unicode(self.csrftoken)

    def validateData(self, fields, data):
        errors = super(CSRFMixin, self).validateData(fields, data)
        self.checkToken()
        return errors

    def update(self, *args, **kwargs):
        self.setUpToken()
        class ICSRF(interface.Interface):
            __csrftoken__ = schema.TextLine(title=u'csrf', defaultFactory=self.get_csrftoken)
        if '__csrftoken__' not in self.fields.keys():
            self.fields.extend(Fields(ICSRF))
            self.fields['__csrftoken__'].mode = 'hidden'
