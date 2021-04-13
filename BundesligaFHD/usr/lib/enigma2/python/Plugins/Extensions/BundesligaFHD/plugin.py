#!/usr/bin/python
# -*- coding: utf-8 -*-
#Plugin By Maggy Mod By RAED
from Components.ActionMap import ActionMap
from Components.config import config, getConfigListEntry, ConfigSelection, ConfigSubsection, configfile
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.Sources.List import List
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from Screens.PluginBrowser import PluginBrowser
from Components.ScrollLabel import ScrollLabel
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from Components.Sources.StaticText import StaticText
from Components.Pixmap import Pixmap
from Components.Console import Console as iConsole
from enigma import getDesktop
from os import environ
import time
import gettext
lang = language.getLanguage()
environ['LANGUAGE'] = lang[:2]
gettext.bindtextdomain('enigma2', resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain('enigma2')
gettext.bindtextdomain('BundesligaFHD', '%s%s' % (resolveFilename(SCOPE_PLUGINS), 'Extensions/BundesligaFHD/locale/'))


def _(txt):
    t = gettext.dgettext('BundesligaFHD', txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t


config.plugins.bundesligafhd = ConfigSubsection()
config.plugins.bundesligafhd.style = ConfigSelection(default='hsv', choices=[('hsv', _('hsv')),
 ('bvb', _('bvb')),
 ('fcb', _('fcb')),
 ('bmg', _('bmg')),
 ('rbl', _('rbl')),
 ('vflw', _('vflw')),
 ('ef', _('ef')),
 ('tsgh', _('tsgh')),
 ('hbsc', _('hbsc')),
 ('bayerl04', _('bayerl04')),
 ('svwb', _('svwb')),
 ('scf', _('scf')),
 ('fsvm05', _('fsvm05')),
 ('fcs04', _('fcs04')),
 ('fd', _('fd')),
 ('fca', _('fca')),
 ('vfbs', _('vfbs')),
 ('h96', _('h96')),
 ('1fcn', _('1fcn')),
 ('1fck', _('1fck')),
 ('1fcb', _('1fcb')),
 ('scp07', _('scp07')),
 ('fcstp', _('fcstp'))])


class BundesligaFHDConfig(ConfigListScreen, Screen):
    skin = '\n\t\t<screen name="BundesligaFHDConfig" position="center,110" size="750,520" title="BundesligaFHD sKIn setup">\n\t\t\t<widget position="15,10" size="720,75" name="config" scrollbarMode="showOnDemand" />\n\t\t\t<ePixmap position="10,475" zPosition="1" size="30,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BundesligaFHD/images/red.png" alphatest="blend" />\n\t\t\t<widget source="red_key" render="Label" position="45,477" zPosition="2" size="165,25" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />\n\t\t\t<ePixmap position="215,475" zPosition="1" size="30,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BundesligaFHD/images/green.png" alphatest="blend" />\n\t\t\t<widget source="green_key" render="Label" position="250,477" zPosition="2" size="165,25" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />\n\t\t\t<ePixmap position="420,475" zPosition="1" size="30,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BundesligaFHD/images/yellow.png" alphatest="blend" />\n\t\t\t<widget source="yellow_key" render="Label" position="455,477" zPosition="2" size="200,25" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />\n\t\t\t<widget name="CSPreview" position="175,120" size="400,225" zPosition="5" alphatest="blend" />\n\t\t</screen>'

    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)
        self.setTitle(_('BundesligaFHD Skin Setup'))
        self.iConsole = iConsole()
        self.list = []
        self.list.append(getConfigListEntry(_('Select Bundesliga team'), config.plugins.bundesligafhd.style))
        ConfigListScreen.__init__(self, self.list)
        self['CSPreview'] = Pixmap()
        self['red_key'] = StaticText(_('Close'))
        self['green_key'] = StaticText(_('Save'))
        self['yellow_key'] = StaticText(_('Restart GUI'))
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions'], {'red': self.cancel,
         'cancel': self.cancel,
         'green': self.save,
         'yellow': self.restart,
         'ok': self.save}, -2)
        self.onLayoutFinish.append(self.CSPreview)

    def CSPreview(self):
        self['CSPreview'].instance.setPixmapFromFile('/usr/lib/enigma2/python/Plugins/Extensions/BundesligaFHD/preview/%sstyle.png' % config.plugins.bundesligafhd.style.value)

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.CSPreview()

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.CSPreview()

    def exit(self):
        self.close()

    def cancel(self):
        for i in self['config'].list:
            i[1].cancel()
        self.close(False)

    def save(self):
        if config.osd.language.value == 'de_DE':
            self.iConsole.ePopen('tar -C/ -xzpvf /usr/share/enigma2/BundesligaFHD/tgz/buttons_de.tar.gz', self.saveColorStyle)
        else:
            self.iConsole.ePopen('tar -C/ -xzpvf /usr/share/enigma2/BundesligaFHD/tgz/buttons_en.tar.gz', self.saveColorStyle)

    def saveColorStyle(self, result, retval, extra_args):
        self.iConsole.ePopen('tar -C/ -xzpvf /usr/share/enigma2/BundesligaFHD/tgz/%sstyle.tar.gz' % config.plugins.bundesligafhd.style.value)
        config.plugins.bundesligafhd.style.save()
        configfile.save()
        self.mbox = self.session.open(MessageBox, _('configuration is saved'), MessageBox.TYPE_INFO, timeout=4)

    def restart(self):
        self.session.open(TryQuitMainloop, 3)


def main(session, **kwargs):
    session.open(BundesligaFHDConfig)


def Plugins(**kwargs):
    for line in open("/etc/enigma2/settings"):
        if "config.skin.primary_skin=BundesligaFHD/skin.xml" in line:
            return PluginDescriptor(name=_('BundesligaFHDConfig setup'), description=_('BundesligaFHDConfig setup'), where=[PluginDescriptor.WHERE_PLUGINMENU, PluginDescriptor.WHERE_EXTENSIONSMENU], icon='BundesligaFHD.png', fnc=main)
    return []
