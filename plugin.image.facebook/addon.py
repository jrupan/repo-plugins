import os, sys, urllib

class AddonHelper:
	def __init__(self,pluginid):
		self._pluginID = pluginid
		self._xbmc = None
		self._xbmcgui = None
		self._xbmcplugin = None
		self._xbmcaddon = None
		self.__settings__ = None
		self.__language__ = None
		self._params = None
		self._urllib2 = None
		self._time = None
		self._re = None
		
	def xbmc(self):
		if self._xbmc: return self._xbmc
		import xbmc #@UnresolvedImport
		self._xbmc = xbmc
		return xbmc
		
	def xbmcgui(self):
		if self._xbmcgui: return self._xbmcgui
		import xbmcgui #@UnresolvedImport
		self._xbmcgui = xbmcgui
		return xbmcgui
		
	def xbmcplugin(self):
		if self._xbmcplugin: return self._xbmcplugin
		import xbmcplugin #@UnresolvedImport
		self._xbmcplugin = xbmcplugin
		return xbmcplugin
		
	def xbmcaddon(self):
		if self._xbmcaddon: return self._xbmcaddon
		import xbmcaddon #@UnresolvedImport
		self._xbmcaddon = xbmcaddon
		return xbmcaddon
		
	def urllib2(self):
		if self._urllib2: return self._urllib2
		import urllib2
		self._urllib2 = urllib2
		return urllib2
		
	def setSetting(self,settingname,setting):
		self.settings().setSetting(settingname,setting)
		
	def getSetting(self,setting):
		return self.settings().getSetting(setting)
		
	def getSettingInt(self,setting):
		return int(self.getSetting(setting))
		
	def getSettingBool(self,setting):
		return self.getSetting(setting) == 'true'
		
	def settings(self):
		if self.__settings__: return self.__settings__
		self.__settings__ = self.xbmcaddon().Addon(id=self._pluginID)
		return self.__settings__
		
	def lang(self,strid):
		if self.__language__: return self.__language__(strid)
		self.__language__ = self.settings().getLocalizedString
		return self.__language__(strid)
		
	def dataPath(self,tail=''):
		return os.path.join(self.settings().getAddonInfo('profile'),tail)
		
	def addonPath(self,tail=''):
		return os.path.join(self.settings().getAddonInfo('path'),tail)
		
	def _getParams(self):
		params=sys.argv[2]
		param={}
		if len(params) < 2:
			self._params = param
			return
		cleanedparams=params.replace('?','')
		if params.endswith('/'): params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]	
		self._params = param
		print param
		
	def getParamString(self,key,default=None,no_unquote=False):
		if self._params == None: self._getParams()
		try:
			if no_unquote:
				return self._params.get(key,default)
			else:
				return urllib.unquote_plus(self._params[key])
		except:
			return default

	def getParamInt(self,key,default=None):
		if self._params == None: self._getParams()
		try:
			return int(self._params[key])
		except:
			return default
			
	def addLink(self,name,url,thumbnail,total=0,contextMenu=None):
		liz=self.xbmcgui().ListItem(name, iconImage="DefaultImage.png", thumbnailImage=thumbnail)
		liz.setInfo(type="image", infoLabels={ "Title": name } )
		if contextMenu: liz.addContextMenuItems(contextMenu)
		return self.xbmcplugin().addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False,totalItems=total)

	def addDir(self,_name,_thumbnail='',_total=0,contextMenu=None,**kwargs):
		u=sys.argv[0]+"?"+urllib.urlencode(kwargs)
		liz=self.xbmcgui().ListItem(_name,'',iconImage="DefaultFolder.png", thumbnailImage=_thumbnail)
		liz.setInfo(type="image", infoLabels={"Title": _name} )
		if contextMenu: liz.addContextMenuItems(contextMenu)
		return self.xbmcplugin().addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=_total)
		
	def endOfDirectory(self,succeeded=True,updateListing=False,cacheToDisc=True):
		self.xbmcplugin().endOfDirectory(int(sys.argv[1]),succeeded=succeeded,updateListing=updateListing,cacheToDisc=cacheToDisc)
		
	def getFile(self,url,target_file):
		request = self.urllib2().urlopen(url)
		f = open(target_file,"wb")    
		f.write(request.read())
		f.close()
		return target_file
	
	def time(self):
		if self._time: return self._time
		import time
		self._time = time
		return time
		
	def re(self):
		if self._re: return self._re
		import re
		self._re = re
		return re