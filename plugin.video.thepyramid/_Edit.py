import xbmcaddon, base64

Decode = base64.decodestring
MainBase = (Decode('aHR0cDovL3RvbWJyYWlkZXJidWlsZHMuY28udWsvYWRkb24vaG9tZS50eHQ='))
addon = xbmcaddon.Addon('plugin.video.thepyramid')