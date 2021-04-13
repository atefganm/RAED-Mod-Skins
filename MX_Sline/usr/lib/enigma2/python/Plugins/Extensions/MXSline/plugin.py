#!/usr/bin/python
# -*- coding: utf-8 -*-
#Plugin By Maggy Mod By RAED
from Components.ActionMap import ActionMap
from Components.config import config, getConfigListEntry, ConfigText, ConfigPassword, ConfigClock, ConfigSelection, ConfigSubsection, ConfigYesNo, configfile, NoSave
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.Sources.List import List
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE, fileExists
from Screens.PluginBrowser import PluginBrowser
from Components.ScrollLabel import ScrollLabel
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from Components.Sources.StaticText import StaticText
from Components.Pixmap import Pixmap
from Components.Console import Console as iConsole
from enigma import getDesktop, eListboxPythonMultiContent, gFont
from os import environ
from os import environ, system
import time
import gettext

lang = language.getLanguage()
environ['LANGUAGE'] = lang[:2]
gettext.bindtextdomain('enigma2', resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain('enigma2')
gettext.bindtextdomain('MXSline', '%s%s' % (resolveFilename(SCOPE_PLUGINS), 'Extensions/MXSline/locale/'))


def _(txt):
    t = gettext.dgettext('MXSline', txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t


reswidth = getDesktop(0).size().width()
resheight = getDesktop(0).size().height()

config.plugins.MXSline = ConfigSubsection()
config.plugins.MXSline.style = ConfigSelection(default='Black', choices=[('Black', _('Black')),
 ('Blue', _('Blue')),
 ('Grey', _('Grey'))])


class MXSlineConfig(ConfigListScreen, Screen):
    if reswidth == 1920:
       skin = '''<screen name="MXSlineConfig" position="center,center" size="750,520" title="MXSline sKIn setup">
                 <widget position="15,10" size="720,75" name="config" font="Regular;30" itemHeight="40" scrollbarMode="showOnDemand" />
                 <ePixmap position="10,475" zPosition="1" size="30,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MXSline/images/red.png" alphatest="blend" />
                 <widget source="red_key" render="Label" position="45,477" zPosition="2" size="165,25" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
                 <ePixmap position="215,475" zPosition="1" size="30,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MXSline/images/green.png" alphatest="blend" />
                 <widget source="green_key" render="Label" position="250,477" zPosition="2" size="165,25" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
                 <ePixmap position="420,475" zPosition="1" size="30,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MXSline/images/yellow.png" alphatest="blend" />
                 <widget source="yellow_key" render="Label" position="455,477" zPosition="2" size="200,25" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
                 <widget name="CSPreview" position="175,120" size="400,225" zPosition="5" alphatest="blend" />
          </screen>'''
    else:
       skin = '''<screen name="MXSlineConfig" position="center,center" size="750,520" title="MXSline sKIn setup">
                 <widget position="15,10" size="720,75" name="config" scrollbarMode="showOnDemand" />
                 <ePixmap position="10,475" zPosition="1" size="30,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MXSline/images/red.png" alphatest="blend" />
                 <widget source="red_key" render="Label" position="45,477" zPosition="2" size="165,25" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
                 <ePixmap position="215,475" zPosition="1" size="30,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MXSline/images/green.png" alphatest="blend" />
                 <widget source="green_key" render="Label" position="250,477" zPosition="2" size="165,25" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
                 <ePixmap position="420,475" zPosition="1" size="30,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MXSline/images/yellow.png" alphatest="blend" />
                 <widget source="yellow_key" render="Label" position="455,477" zPosition="2" size="200,25" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
                 <widget name="CSPreview" position="175,120" size="400,225" zPosition="5" alphatest="blend" />
       </screen>'''

    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)
        self.setTitle(_('MX Sline Skin Setup'))
        self.iConsole = iConsole()
        self.list = []
        self.list.append(getConfigListEntry(_('Select MX Sline team'), config.plugins.MXSline.style))
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
        self['CSPreview'].instance.setPixmapFromFile('/usr/lib/enigma2/python/Plugins/Extensions/MXSline/preview/%sstyle.png' % config.plugins.MXSline.style.value)

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
        self.iConsole.ePopen('tar -C/ -xzpvf /usr/share/enigma2/MX_Sline/tgz/%sstyle.tar.gz' % config.plugins.MXSline.style.value)
        cmd = '/usr/share/enigma2/MX_Sline/R.sh'
        rc = system(cmd)
        cmd = 'rm -f /usr/share/enigma2/MX_Sline/R.sh'
        rc = system(cmd)
        config.plugins.MXSline.style.save()
        configfile.save()
        self.mbox = self.session.open(MessageBox, _('configuration is saved'), MessageBox.TYPE_INFO, timeout=4)

    def restart(self):
        self.session.open(TryQuitMainloop, 3)


def main(session, **kwargs):
    session.open(MXSlineConfig)


def Plugins(**kwargs):
    for line in open("/etc/enigma2/settings"):
        if "config.skin.primary_skin=MX_Sline/skin.xml" in line:
            return PluginDescriptor(name=_('MX Sline Config setup'), description=_('MX Sline Config setup'), where=[PluginDescriptor.WHERE_PLUGINMENU, PluginDescriptor.WHERE_EXTENSIONSMENU], icon='MXSline.png', fnc=main)
    return []
