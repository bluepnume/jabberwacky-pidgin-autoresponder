#!/usr/bin/env python

import re, urllib, os

import dbus, gobject
from dbus.mainloop.glib import DBusGMainLoop

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()
obj = bus.get_object('im.pidgin.purple.PurpleService', '/im/pidgin/purple/PurpleObject')
purple = dbus.Interface(obj, 'im.pidgin.purple.PurpleInterface')

class Jabber(object):

  regex = ('vText%s|' * 7) %tuple(range(2, 9)) + 'conv_id|prevref'
  regex = re.compile('NAME=(%s) TYPE=hidden VALUE="([^"]*)"' % regex, re.M)
  data = {}

  def initiate(self):
    return self.speak()

  def speak(self, text=''):
    if self.data:
      self.data['vText1'] = text
    html = urllib.urlopen('http://jabberwacky.com/', urllib.urlencode(self.data)).read()
    self.data = dict(self.regex.findall(html))
    return self.data['vText2']

conversations = {}

def msg(account, sender, msg, convo, flags):
  if purple.PurpleSavedstatusGetType(purple.PurpleSavedstatusGetCurrent()) in (3, 5):
    if not convo in conversations:
      conversations[convo] = Jabber()
      msg = conversations[convo].initiate()
    else:
      msg = conversations[convo].speak(msg)
    purple.PurpleConvImSend(purple.PurpleConvIm(convo), msg)

bus.add_signal_receiver(msg, dbus_interface="im.pidgin.purple.PurpleInterface", signal_name="ReceivedImMsg")

loop = gobject.MainLoop()
loop.run()
