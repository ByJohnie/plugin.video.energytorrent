# -*- coding: utf-8 -*-
#Библиотеки, които използват python и Kodi в тази приставка
import re
import sys
import os
import urllib
import urllib2
import xbmc, xbmcplugin,xbmcgui,xbmcaddon
import base64
import cookielib

#Място за дефиниране на константи, които ще се използват няколкократно из отделните модули
__addon_id__= 'plugin.video.energytorrent'
__Addon = xbmcaddon.Addon(__addon_id__)
__settings__ = xbmcaddon.Addon(id=__addon_id__)
__icon__ =  xbmc.translatePath(__Addon.getAddonInfo('path') + "/resources/icon.png")
username = xbmcaddon.Addon().getSetting('settings_username')
password = xbmcaddon.Addon().getSetting('settings_password')
viewmode = xbmcaddon.Addon().getSetting('list')
MUA = 'Mozilla/5.0 (Linux; Android 5.0.2; bg-bg; SAMSUNG GT-I9195 Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Version/1.0 Chrome/18.0.1025.308 Mobile Safari/535.19' #За симулиране на заявка от мобилно устройство
UA = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0' #За симулиране на заявка от  компютърен браузър
baseurl = base64.b64decode("aHR0cDovL2VuZXJneS10b3JyZW50LmNvbS8=")

#инициализация
if not username or not password or not __settings__:
        xbmcaddon.Addon().openSettings()     


params = {'username': username,
          'password': password
}
login = baseurl + 'takelogin.php'
req = urllib2.Request(login, urllib.urlencode(params))
req.add_header('User-Agent', UA)
req.add_header('Referer', baseurl)
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
f = opener.open(req)
data = f.read()
#print data
#Меню с директории в приставката
def set_viewmode():
        if viewmode == '0':
         xbmc.executebuiltin('Container.SetViewMode(504)')
        if viewmode == '1':
         xbmc.executebuiltin('Container.SetViewMode(500)')
        if viewmode == '2':
         xbmc.executebuiltin('Container.SetViewMode(503)')
        if viewmode == '3':
         xbmc.executebuiltin('Container.SetViewMode(515)')
        if viewmode == '4':
         xbmc.executebuiltin('Container.SetViewMode(501)')
         
def CATEGORIES():
        addDir('Търсене',baseurl+'browse.php?search=',3,'','DefaultFolder.png')
        addDir('Сериали',baseurl+'browse.php?cat=6&page=0',1,'','DefaultFolder.png')
        addDir('Анимация',baseurl+'browse.php?cat=7&page=0',1,'','DefaultFolder.png')
        addDir('Анимация БГ Аудио',baseurl+'browse.php?cat=11&page=0',1,'','DefaultFolder.png')
        movurl = baseurl + 'browse.php'
        req = urllib2.Request(movurl)
        req.add_header('User-Agent', UA)
        req.add_header('Referer', baseurl)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        f = opener.open(req)
        data = f.read().decode('cp1251').encode('utf-8')
        f.close()
        match = re.compile('<a class="catlink" href="(.+?)">(Филми.+?)<').findall(data)
        for link, name in match:
                thumbnail = 'DefaultFolder.png'
                movieurl = baseurl + link + '&page=0'
                addDir(name,movieurl,1,'',thumbnail)    


#Разлистване видеата на първата подадена страница
def INDEXPAGES(url):
        print 'tova e kategoriq' + url
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        req.add_header('Referer', baseurl)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        f = opener.open(req)
        data = f.read().decode('cp1251').encode('utf-8')
        f.close()
        br = 0
        match = re.compile('showpic.+?,.(.+?)..".+?href="(details.+?)&amp;hit=1"><b>(.+?)</b>.*\n<br /><i>(.+?)<.*\n.*\n.*\n.*\n.*\n.*">(.+?)<br />(.+?)</td>\n.*\n*\n.*0>(.+?)</font></a></b>').findall(data)
        for img,link,title,dobaven,razmer,gb,seeders in match:
          thumbnail = baseurl + 'images/torrents/details/' + img
          #print thumbnail
          desc = 'Добавен на:' + dobaven + ' Размер:' + razmer + gb + ' Сийдъри:' + seeders
          url1 = baseurl + link
          #print url
          addDir(title,url1,2,desc,thumbnail)
          br = br + 1
        if br >= 14:
          getpage=re.compile('(.+?)&page=(.+?)').findall(url)
          for newurl,page in getpage:
                  newpage = int(page)+1
                  print newurl
                  print newpage
                  print page
                  nexturl = newurl+ '&page=' + str(newpage)
                  print nexturl
                  addDir('следваща страница>>'+str(newpage),nexturl,1,'','DefaultFolder.png')

def SHOW(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        req.add_header('Referer', baseurl)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        f = opener.open(req)
        data = f.read().decode('cp1251').encode('utf-8')
        #print data
        f.close()
        br = 0
        matchl = re.compile('a href="(magnet.+?)"').findall(data)
        for link in matchl:
          link = link.replace('&amp;','&')
          matchi = re.compile("<img border='0' src=.(.+?). />").findall(data)
          for thumbnail in matchi:      
           if 'Резюме' in data:
            descr = ''       
            matchd = re.compile('Резюме.*<b>:(.*)</b>').findall(data)
            for desc in matchd:
             descr = descr + desc      
             addLink(name,link,4,descr,thumbnail)
             br = br + 1
           if 'Резюме:' in data:
            descr = ''       
            matchd2 = re.compile('Резюме:.*">(.*)<').findall(data)
            for desc in matchd2:
             descr = descr + desc       
             addLink(name,link,4,descr,thumbnail)
             br = br + 1
           if 'Сюжет' in data:
            descr = ''       
            matchd2 = re.compile('.: Сюжет :..*">(.*)<').findall(data)
            for desc in matchd2:
             descr = descr + desc       
             addLink(name,link,4,descr,thumbnail)
             br = br + 1
           if 'Действие' in data:       
            matchd2 = re.compile('Действие.*<b>(.*)').findall(data)
            for desc in matchd2:     
             addLink(name,link,4,desc,thumbnail)
             br = br + 1
           if '.: Резюме :.' in data:
            descr = ''       
            matchd2 = re.compile('Резюме.*\n.*\n.*\n.*\n.*>(.*)<').findall(data)
            for desc in matchd2:
             descr = descr + desc       
             addLink(name,link,4,descr,thumbnail)
             br = br + 1
        if br == 0:
         xbmc.executebuiltin(('Notification(%s,%s,%s,%s)' % ('MAGNET', 'Няма магнитен линк върнете се назад', '5000', __icon__)))

def SEARCH(url):
       values = ['Всички','XVID','X264','СЕРИАЛИ','Филми Русия','HDTV']
       question = 'Изберете категория за търсене'
       ask = xbmcgui.Dialog().select(question, values)
       keyb = xbmc.Keyboard('', 'Търсачка')
       keyb.doModal()
       searchText = ''
       sel = ask
       if (keyb.isConfirmed()):
           if values[sel] == 'Всички':
            searchText = urllib.quote_plus(keyb.getText())
            searchText=searchText.replace(' ','+')
            searchurl = url + searchText + '&descrbox=1&page=0'
            searchurl = searchurl.encode('utf-8')
           if values[sel] == 'XVID':
            searchText = urllib.quote_plus(keyb.getText())
            searchText=searchText.replace(' ','+')       
            searchurl = url + searchText + '&cat=4&descrbox=1&page=0'
            searchurl = searchurl.encode('utf-8')
           if values[sel] == 'X264':
            searchText = urllib.quote_plus(keyb.getText())
            searchText=searchText.replace(' ','+')       
            searchurl = url + searchText + '&cat=30&descrbox=1&page=0'
            searchurl = searchurl.encode('utf-8')
           if values[sel] == 'СЕРИАЛИ':
            searchText = urllib.quote_plus(keyb.getText())
            searchText=searchText.replace(' ','+')       
            searchurl = url + searchText + '&cat=6&descrbox=1&page=0'
            searchurl = searchurl.encode('utf-8')
           if values[sel] == 'Филми Русия':
            searchText = urllib.quote_plus(keyb.getText())
            searchText=searchText.replace(' ','+')       
            searchurl = url + searchText + '&cat=28&descrbox=1&page=0'
            searchurl = searchurl.encode('utf-8')
           if values[sel] == 'HDTV':
            searchText = urllib.quote_plus(keyb.getText())
            searchText=searchText.replace(' ','+')       
            searchurl = url + searchText + '&cat=19&descrbox=1&page=0'
            searchurl = searchurl.encode('utf-8')
       print 'SEARCHING:' + searchurl
       INDEXPAGES(searchurl)

#Зареждане на видео
def PLAY(url):
          p = 'plugin://plugin.video.elementum/play?uri=%s' % (url)
          li = xbmcgui.ListItem(iconImage=iconimage, thumbnailImage=iconimage, path=p)
          li.setInfo('video', { 'title': name })
          try:
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
          except:
            xbmc.executebuiltin("Notification('Грешка','Видеото липсва на сървъра!')")



#Модул за добавяне на отделно заглавие и неговите атрибути към съдържанието на показваната в Kodi директория - НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def addLink(name,url,mode,plot,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name, "plot": plot } )
        liz.setProperty("IsPlayable" , "true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok



#Модул за добавяне на отделна директория и нейните атрибути към съдържанието на показваната в Kodi директория - НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def addDir(name,url,mode,plot,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name, "plot": plot } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


#НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param







params=get_params()
url=None
name=None
iconimage=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        name=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass


#Списък на отделните подпрограми/модули в тази приставка - трябва напълно да отговаря на кода отгоре
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
    
elif mode==1:
        print ""+url
        INDEXPAGES(url)

elif mode==2:
        print ""+url
        SHOW(url)

elif mode==3:
        print ""+url
        SEARCH(url)

elif mode==4:
        print ""+url
        PLAY(url)


xbmcplugin.setContent(int(sys.argv[1]), 'movies')
set_viewmode()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
