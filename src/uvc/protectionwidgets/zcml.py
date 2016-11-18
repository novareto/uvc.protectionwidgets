# -*- coding: utf-8 -*-

import zope.component
from zope.interface import Interface
from norecaptcha.captcha import VERIFY_SERVER
from .widgets.captcha import IRecaptcha, Recaptcha


def recaptcha_handler(_context, public_key, private_key,
                      server_url=VERIFY_SERVER):

    captcha_utility = Recaptcha(public_key, private_key, server_url)

    _context.action(
        discriminator=('utility', IRecaptcha),
        callable=zope.component.provideUtility,
        args=(captcha_utility, IRecaptcha, ''),
    )
