# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0903,E0402,W0120


'status'


from opb.handler import Listens
from opb.objects import prt


def sts(event):
    for bot in Listens.objs:
        if 'state' in dir(bot):
            event.reply(prt(bot.state, skip='lastline'))
    else:
        event.reply("no status")
