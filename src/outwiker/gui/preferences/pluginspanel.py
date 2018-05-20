# -*- coding: utf-8 -*-

import os
import wx
import wx.adv
import logging
import json
import html
import shutil

import outwiker
import outwiker.core.packageversion as pv
from outwiker.core.application import Application
from outwiker.gui.guiconfig import PluginsConfig
from outwiker.gui.longprocessrunner import LongProcessRunner
from outwiker.gui.testeddialog import TestedDialog
from outwiker.core.system import getImagesDir
from outwiker.core.system import getHTMLTemplatesDir
from outwiker.core.system import getPluginsDirList
from outwiker.core.system import getCurrentDir, getOS
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel
from outwiker.core.commands import MessageBox, setStatusText
from outwiker.core.pluginupdater import UpdatePlugin
from outwiker.utilites.versionlist import VersionList
from outwiker.utilites.textfile import readTextFile

logger = logging.getLogger('pluginspanel')

class PluginsPanel (BasePrefPanel):
    """
    Панель со списком установленных плагинов
    """
    def __init__(self, parent):
        super(PluginsPanel, self).__init__(parent)
        self._application = Application
        self.__htmlMinWidth = 150

        self.__createGui()
        self.__controller = PluginsController(self, self._application)
        self.SetupScrolling()

        self._application.onLinkClick += self.__onLinkClick


    def __createGui(self):
        self.pluginsList = wx.CheckListBox(self, -1, style=wx.LB_SORT)
        self.pluginsList.SetMinSize((50, 20))

        imagesDir = getImagesDir()

        # Add a plugin
        self.addGroupBtn = wx.BitmapButton(
            self,
            bitmap=wx.Bitmap(os.path.join(imagesDir, "add.png"))
        )
        self.addGroupBtn.SetToolTip(_(u"Add new plugin"))
        self.addGroupBtn.Bind(wx.EVT_BUTTON, handler=self.__addPlugins)

        # remove the plugin
        self.delGroupBtn = wx.BitmapButton(
            self,
            bitmap=wx.Bitmap(os.path.join(imagesDir, "delete.png"))
        )
        self.delGroupBtn.SetToolTip(_(u"Delete the plugin"))
        self.delGroupBtn.Bind(wx.EVT_BUTTON, handler=self.__delPlugins)

        self.__downloadLink = wx.adv.HyperlinkCtrl(
            self,
            -1,
            _(u"Download more plugins"),
            _(u"http://jenyay.net/Outwiker/PluginsEn"))

        # Панель, которая потом заменится на HTML-рендер
        self.__blankPanel = wx.Panel(self)
        self.__blankPanel.SetMinSize((self.__htmlMinWidth, -1))

        self.__pluginsInfo = None

        self.__layout()

    @property
    def pluginsInfo(self):
        if self.__pluginsInfo is None:
            # Удалим пустую панель, а вместо нее добавим HTML-рендер
            self.pluginsSizer.Detach(self.__blankPanel)
            self.__blankPanel.Destroy()

            self.__pluginsInfo = getOS().getHtmlRender(self)
            self.__pluginsInfo.SetMinSize((self.__htmlMinWidth, -1))

            self.pluginsSizer.Insert(1, self.__pluginsInfo, flag=wx.EXPAND)
            self.Layout()

        return self.__pluginsInfo

    def __layout(self):
        self.mainSizer = wx.FlexGridSizer(cols=1)
        self.mainSizer.AddGrowableRow(0)
        self.mainSizer.AddGrowableCol(0)

        self.pluginsSizer = wx.FlexGridSizer(cols=2)
        self.pluginsSizer.AddGrowableRow(0)
        self.pluginsSizer.AddGrowableCol(0)
        self.pluginsSizer.AddGrowableCol(1)
        self.pluginsSizer.Add(self.pluginsList, flag=wx.EXPAND)
        self.pluginsSizer.Add(self.__blankPanel, flag=wx.EXPAND)

        self.buttonSizer = wx.FlexGridSizer(cols=2)
        self.buttonSizer.Add(self.addGroupBtn)
        self.buttonSizer.Add(self.delGroupBtn)

        self.mainSizer.Add(self.pluginsSizer,
                           flag=wx.ALL | wx.EXPAND,
                           border=2)
        self.mainSizer.Add(self.buttonSizer,
                           flag=wx.ALL | wx.ALIGN_LEFT,
                           border=2)
        self.mainSizer.Add(self.__downloadLink,
                           flag=wx.ALL | wx.ALIGN_LEFT,
                           border=2)

        self.SetSizer(self.mainSizer)

    def LoadState(self):
        self.__controller.loadState()

    def Save(self):
        self.__controller.save()

    def __addPlugins(self, event):
        setStatusText(_(u"Check for new versions..."))

        progressRunner = LongProcessRunner(
            self.__controller._threadFunc,
            self._application.mainWindow,
            dialogTitle=u"Install Plugins",
            dialogText=_(u"Check available Plugins..."))

        progressRunner.run(silenceMode=True)

        self.__controller._threadFunc()

    def __delPlugins(self, event):
        selection_item = self.pluginsList.GetSelection()
        if selection_item is not None:
            plugin_name = self.pluginsList.GetString(selection_item)
            self.__controller.uninstall_plugin(plugin_name)

    def __onLinkClick(self, page, params):
        '''
        onLinkClick event handler. If params.link contain 'update:<PluginName>' when update <PluginName>
        otherwise do nothing

        :param page:
            not use in this handler
        :param params:
            LinkClickParams instance
        :return:
            None
        '''
        logger.debug(u'__onLinkClick: {}'.format(params.__dict__))

        import re
        m = re.search(r'plugin_install:(\w+)', params.link)

        if m:
            plugin_name = m.group(1)
            logger.info(u'Install plugin "{}"'.format(plugin_name))
            self.__controller.install_plugin(plugin_name)

    def __exit__(self, exc_type, exc_value, traceback):
        self._application.onLinkClick -= self.__onLinkClick

class PluginsController (object):
    """
    Контроллер, отвечающий за работу панели со списком плагинов
    """
    def __init__(self, pluginspanel, app):
        self.__owner = pluginspanel
        self._application = app
        # update dialog instance
        self._dialog = None

        # Т.к. под виндой к элементам CheckListBox нельзя
        # прикреплять пользовательские данные,
        # придется их хранить отдельно.
        # Ключ - имя плагина, оно же текст строки
        # Значение - экземпляр плагина
        self.__pluginsItems = {}
        self.__deletedPlugins = {}
        self._installerPlugins = {}

        self.__owner.Bind(wx.EVT_LISTBOX,
                          self.__onSelectItem,
                          self.__owner.pluginsList)


        self.vl = VersionList()
        self._htmlTemplatePath = os.path.join(getHTMLTemplatesDir(),'plugin_install.html')

    def __onSelectItem(self, event):
        htmlContent = u""
        if event.IsSelection():
            plugin = self.__pluginsItems[event.GetString()]
            assert plugin is not None

            htmlContent = self.__createPluginInfo(plugin)

        self.__owner.pluginsInfo.SetPage(htmlContent, getCurrentDir())

    def __createPluginInfo(self, plugin):
        assert plugin is not None

        infoTemplate = u"""<html>
<head>
    <meta http-equiv='content-type' content='text/html; charset=utf-8'/>
</head>

<body>
{name}<br>
{version}<br>
{url}<br>
{description}<br>
</body>
</html>"""

        plugin_name = u"""<h3>{name}</h3>""".format(name=plugin.name)

        plugin_version = u"""<b>{version_header}:</b> {version}""".format(
            version_header=_(u"Version"),
            version=plugin.version)

        plugin_description = u"""<b>{description_head}:</b> {description}""".format(
            description_head=_(u"Description"),
            description=plugin.description.replace("\n", "<br>"))

        if plugin.url is not None:
            plugin_url = u"""<br><b>{site_head}</b>: <a href="{url}">{url}</a><br>""".format(
                site_head=_("Site"),
                url=plugin.url)
        else:
            plugin_url = u""

        result = infoTemplate.format(
            name=plugin_name,
            version=plugin_version,
            description=plugin_description,
            url=plugin_url)

        return result

    def loadState(self):
        self.__pluginsItems.clear()
        self.__owner.pluginsList.Clear()
        self.__appendEnabledPlugins()
        self.__appendDisabledPlugins()
        self.__appendInvalidPlugins()

    def __appendEnabledPlugins(self):
        """
        Добавить загруженные плагины в список
        """
        for plugin in Application.plugins:
            index = self.__owner.pluginsList.Append(plugin.name)

            assert plugin.name not in self.__pluginsItems
            self.__pluginsItems[plugin.name] = plugin

            self.__owner.pluginsList.Check(index, True)

    def __appendDisabledPlugins(self):
        """
        Добавить отключенные плагины в список
        """
        for plugin in Application.plugins.disabledPlugins.values():
            index = self.__owner.pluginsList.Append(plugin.name)

            assert plugin.name not in self.__pluginsItems
            self.__pluginsItems[plugin.name] = plugin

            self.__owner.pluginsList.Check(index, False)

    def __appendInvalidPlugins(self):
        for plugin in Application.plugins.invalidPlugins:
            index = self.__owner.pluginsList.Append(plugin.name)

            self.__pluginsItems[plugin.name] = plugin
            self.__owner.pluginsList.Check(index, False)

    def save(self):
        config = PluginsConfig(Application.config)
        config.disabledPlugins.value = self.__getDisabledPlugins()
        Application.plugins.updateDisableList()

    def __getDisabledPlugins(self):
        disabledList = []

        for itemindex in range(self.__owner.pluginsList.GetCount()):
            if not self.__owner.pluginsList.IsChecked(itemindex):
                disabledList.append(self.__pluginsItems[self.__owner.pluginsList.GetString(itemindex)].name)

        return disabledList

    def _threadFunc(self, silenceMode=False):
        """
        Thread function for silence updates checking.
        Get info data from the  updates Urls

        :param:
            updateUrls - dict which key is plugin name or other ID,
                value is update url
            silenceMode - True or False

        :raise:
            EVT_UPDATE_VERSIONS event
        """

        # get update URLs from plugins.json and remove installed.
        pluginsUrls = {x: y for x, y
                             in self._getUrlsForInstaller().items()
                             if x not in self._application.plugins.loadedPlugins}
        installerInfoDict = self.vl.loadAppInfo(pluginsUrls)

        if not silenceMode:
            self._showUpdates(installerInfoDict)


    def _getUrlsForInstaller(self):

        self._pluginsRepoPath = os.path.join(getHTMLTemplatesDir(), u'plugins.json')

        # read data/plugins.json
        self._installerPlugins = json.loads(
            readTextFile(self._pluginsRepoPath))

        updateUrls = {x['name']: x['url']
                      for x in self._installerPlugins.values()}
        return updateUrls

    def _showUpdates(self, installerInfoDict):
        '''
        Show dialog with update information.
        '''
        #setStatusText(u"")

        HTMLContent = self.createHTMLContent(installerInfoDict)

        with UpdateDialog(self._application.mainWindow) as updateDialog:
            self._dialog = updateDialog
            updateDialog.setContent(HTMLContent, getHTMLTemplatesDir())
            updateDialog.ShowModal()

    def createHTMLContent(self, installerInfoDict):
        template = readTextFile(self._htmlTemplatePath)

        logger.info(getImagesDir())

        templateData = {
            u'installerInfoDict': installerInfoDict,
            u'str_outwiker_current_version': _(u'Installed OutWiker version'),
            u'str_outwiker_latest_stable_version': _(u'Latest stable OutWiker version'),
            u'str_outwiker_latest_unstable_version': _(u'Latest unstable OutWiker version'),
            u'str_version_history': _(u'Version history'),
            u'str_more_info': _(u'More info'),
            u'str_update': _(u'Update'),
            u'str_install': _(u'Install'),
            u'str_uninstall': _(u'Uninstall'),
            u'data_path': getImagesDir(),
            u'escape': html.escape,
        }

        contentGenerator = ContentGenerator(template)
        HTMLContent = contentGenerator.render(templateData)
        return HTMLContent

    def install_plugin(self, name):
        """
        Install plugin by name.

        :return: True if plugin was installed, otherwise False
        """

        getAppInfo = self.vl.getAppInfoFromUrl
        getDownlodUrl = self.vl.getDownlodUrl

        plugin_info = self._installerPlugins.get(name, None)
        if plugin_info:

            appInfo = getAppInfo(plugin_info["url"])
            if not appInfo or not appInfo.versionsList:
                MessageBox(_(u"The plugin description can't be downloaded. Please install plugin manually"),
                           u"UpdateNotifier")
                return False

            api_required_version = appInfo.requirements.api_version
            if pv.checkVersionAny(outwiker.core.__version__,
                                  api_required_version) != 0:
                MessageBox(_(u"The plugin required newer version of OutWiker. Please update OutWiker"),
                           u"UpdateNotifier")
                return False

            # get link to latest version
            url = getDownlodUrl(appInfo)
            if not url:
                MessageBox(_(u"The download link was not found in plugin description. Please install plugin manually"),
                           u"UpdateNotifier")
                return False

            # getPluginsDirList[0] - папка рядом с запускаемым файлом, затем идут другие папки,
            # если они есть
            pluginPath = self.__deletedPlugins.get(
                name,
                os.path.join(getPluginsDirList()[-1], name.lower()))

            logger.info(
                'install_plugin: {url} {path}'.format(
                    url=url, path=pluginPath))

            rez = UpdatePlugin().update(url, pluginPath)

            if rez:
                self._application.plugins.load([os.path.dirname(pluginPath)])
                self._updateDialog()
                self.loadState()
            else:
                MessageBox(
                    _(u"Plugin was NOT Installed. Please update plugin manually"),
                    u"UpdateNotifier")
            return rez

    def _updateDialog(self):
        """
        Update content on the current opened update dialog.
        """
        if self._dialog and self._dialog.IsModal():
            self._dialog.EndModal(wx.ID_OK)
            self._threadFunc()

    def uninstall_plugin(self, name):
        """
        remove plugin from application._plugins and delete plugin folder from disk
        :param name:
        :return:
            True if plugin was uninstalled successful, otherwise False
        """
        def del_msg(function, path, excinfo):
            "Error handler for shutil.rmtree"
            MessageBox(_("Plugin's folder can't be deleted. Please delete the following path: \n {}").format(path))

        rez = True

        plugin = self._application.plugins.loadedPlugins.get(name, None)
        if not plugin:
            return

        plugin_path = plugin.pluginPath

        logger.info(
            'uninstall_plugin: {name} {path}'.format(
                name=name, path=plugin_path))

        # remove plugin from applications._plugins
        rez = rez and self._application.plugins.remove(name)

        logger.info('uninstall_plugin: remove plugin {}'.format(rez))

        # remove plugin folder or remove symbolic link to it.
        if rez:
            if os.path.islink(plugin_path):
                os.unlink(plugin_path)
            else:
                shutil.rmtree(plugin_path,
                              onerror=lambda f, path, i:
                              MessageBox(
                                  _("Plugin's folder can't be deleted. Please delete the following path: \n {}"
                                    ).format(path)))

            # Python can't unimport file, so save the deleted plugin
            # If user re-installs it we just install it in same directory
            self.__deletedPlugins[name] = plugin_path

            self.loadState()
        return rez

class UpdateDialog(TestedDialog):
    """Dialog to show new plugins"""

    def __init__(self, parent):
        super(UpdateDialog, self).__init__(
            parent,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.SetSize((750, 500))
        self.SetTitle(_(u"Choose plugins for installation"))
        self._createGui()

    def setContent(self, HTMLContent, basepath):
        self._htmlRender.SetPage(HTMLContent, basepath)

    def _createGui(self):
        self._mainSizer = wx.FlexGridSizer(cols=1)
        self._mainSizer.AddGrowableCol(0)
        self._mainSizer.AddGrowableRow(0)

        self._htmlRender = getOS().getHtmlRender(self)
        self._mainSizer.Add(self._htmlRender,
                            1,
                            wx.EXPAND | wx.ALL,
                            border=2)

        buttonsSizer = self.CreateButtonSizer(wx.OK)
        self._mainSizer.Add(buttonsSizer,
                            1,
                            wx.ALIGN_RIGHT | wx.ALL,
                            border=2)

        self.SetSizer(self._mainSizer)
        self.Layout()


class ContentGenerator(object):
    def __init__(self, templateStr):
        self._templateStr = templateStr

    def render(self, data):
        '''
        data - dictionary for template substitution.
        '''
        from outwiker.libs.jinja2 import Environment

        env = Environment()
        templateObj = env.from_string(self._templateStr)

        return templateObj.render(**data)

