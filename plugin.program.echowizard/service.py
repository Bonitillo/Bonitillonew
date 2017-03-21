"""
    Copyright (C) 2016 ECHO Wizard

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import urllib2,urllib
import requests
import shutil
import zipfile
from resources.lib.modules import extract
from resources.lib.modules import downloader
from resources.lib.modules import maintenance
from resources.lib.modules import installer
import re
from resources.lib.modules import backuprestore
import time
from resources.lib.modules import common as Common
from resources.lib.modules import wipe
from resources.lib.modules import runner
from resources.lib.modules import plugintools
from random import randint
from datetime import date
import calendar
from resources.lib.modules import acdays

my_date = date.today()
today = calendar.day_name[my_date.weekday()]
addon_id = 'plugin.program.echowizard'
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
SOURCES     =  xbmc.translatePath(os.path.join('special://home/userdata','sources.xml'))
ADDON     =  xbmc.translatePath(os.path.join('special://home/addons/plugin.program.echowizard',''))
COMMUNITY_VERSION  =  os.path.join(USERDATA,'echo_community_ota.txt')
my_addon = xbmcaddon.Addon()
dp = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()
AddonTitle="[COLOR yellowgreen]ECHO[/COLOR] [COLOR white]Wizard[/COLOR]"
GoogleOne = "http://www.google.com"
GoogleTwo = "http://www.google.co.uk"
check = plugintools.get_setting("checkupdates")
addonupdate = plugintools.get_setting("updaterepos")
autoclean = plugintools.get_setting("acstartup")
size_check = plugintools.get_setting("startupsize")
CLEAR_CACHE_SIZE = plugintools.get_setting("cachemb")
CLEAR_PACKAGES_SIZE = plugintools.get_setting("packagesmb")
CLEAR_THUMBS_SIZE = plugintools.get_setting("thumbsmb")
BASEURL = base64.b64decode(b"aHR0cDovL2VjaG9jb2Rlci5jb20v")
nointernet = 0

#Update Information
ECHO_VERSION  =  os.path.join(USERDATA,'echo_build.txt')
HOME         =  xbmc.translatePath('special://home/')
TMP_TRAKT     =  xbmc.translatePath(os.path.join(HOME,'tmp_trakt'))
TRAKT_MARKER =  xbmc.translatePath(os.path.join(TMP_TRAKT,'marker.xml'))
backup_zip = xbmc.translatePath(os.path.join(TMP_TRAKT,'Restore_RD_Trakt_Settings.zip'))

try:
    response = Common.OPEN_URL_NORMAL(GoogleOne)
except:
    try:
        response = Common.OPEN_URL_NORMAL(GoogleTwo)
    except:
        nointernet = 1
        pass