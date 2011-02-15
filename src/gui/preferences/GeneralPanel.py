# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Sat Oct 23 11:59:26 2010

import wx

import ConfigElements
from core.config import StringOption, BooleanOption, IntegerOption
import core.i18n
from core.application import Application

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade

class GeneralPanel(wx.ScrolledWindow):
	def __init__(self, *args, **kwds):
		# begin wxGlade: GeneralPanel.__init__
		kwds["style"] = wx.TAB_TRAVERSAL
		wx.ScrolledWindow.__init__(self, *args, **kwds)
		self.minimizeCheckBox = wx.CheckBox(self, -1, _("Minimize to tray"))
		self.startIconizedCheckBox = wx.CheckBox(self, -1, _("Start iconized"))
		self.alwaysInTrayCheckBox = wx.CheckBox(self, -1, _("Always show tray icon"))
		self.askBeforeExitCheckBox = wx.CheckBox(self, -1, _("Ask before exit"))
		self.static_line_2 = wx.StaticLine(self, -1)
		self.history_label = wx.StaticText(self, -1, _("Recent files history length (restart required)"))
		self.historySpin = wx.SpinCtrl(self, -1, "5", min=0, max=20, style=wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB|wx.TE_AUTO_URL)
		self.autoopenCheckBox = wx.CheckBox(self, -1, _("Automatically open the recent file"))
		self.static_line_1 = wx.StaticLine(self, -1)
		self.titleFormatLabel = wx.StaticText(self, -1, _("Main window title format"))
		self.titleFormatText = wx.TextCtrl(self, -1, "")
		self.macrosLabel = wx.StaticText(self, -1, _("Macros for title:\n{file} - open wiki file name\n{page} - open page title"))
		self.static_line_3 = wx.StaticLine(self, -1)
		self.langLabel = wx.StaticText(self, -1, _("Language (restart required)"))
		self.langCombo = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_DROPDOWN|wx.CB_READONLY)

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_CHECKBOX, self.onMinimizeToTray, self.minimizeCheckBox)
		# end wxGlade

		self.LoadState()
		self.updateCheckState()


	def __set_properties(self):
		# begin wxGlade: GeneralPanel.__set_properties
		self.SetSize((514, 414))
		self.SetFocus()
		self.SetScrollRate(0, 0)
		self.askBeforeExitCheckBox.SetValue(1)
		self.langCombo.SetMinSize((130, -1))
		# end wxGlade


	def __do_layout(self):
		# begin wxGlade: GeneralPanel.__do_layout
		main_sizer = wx.FlexGridSizer(10, 1, 0, 0)
		grid_sizer_1 = wx.FlexGridSizer(1, 2, 0, 0)
		grid_sizer_2 = wx.FlexGridSizer(1, 2, 0, 0)
		history_size = wx.FlexGridSizer(1, 2, 0, 0)
		main_sizer.Add(self.minimizeCheckBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
		main_sizer.Add(self.startIconizedCheckBox, 0, wx.ALL, 2)
		main_sizer.Add(self.alwaysInTrayCheckBox, 0, wx.ALL, 2)
		main_sizer.Add(self.askBeforeExitCheckBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
		main_sizer.Add(self.static_line_2, 0, wx.EXPAND, 0)
		history_size.Add(self.history_label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
		history_size.Add(self.historySpin, 0, wx.ALL|wx.ALIGN_RIGHT, 2)
		history_size.AddGrowableRow(0)
		history_size.AddGrowableCol(0)
		history_size.AddGrowableCol(1)
		main_sizer.Add(history_size, 1, wx.EXPAND, 0)
		main_sizer.Add(self.autoopenCheckBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
		main_sizer.Add(self.static_line_1, 0, wx.EXPAND, 0)
		grid_sizer_2.Add(self.titleFormatLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
		grid_sizer_2.Add(self.titleFormatText, 0, wx.ALL|wx.EXPAND, 2)
		grid_sizer_2.AddGrowableCol(1)
		main_sizer.Add(grid_sizer_2, 1, wx.EXPAND, 0)
		main_sizer.Add(self.macrosLabel, 0, wx.ALL, 2)
		main_sizer.Add(self.static_line_3, 0, wx.EXPAND, 0)
		grid_sizer_1.Add(self.langLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
		grid_sizer_1.Add(self.langCombo, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 2)
		grid_sizer_1.AddGrowableRow(0)
		grid_sizer_1.AddGrowableCol(0)
		grid_sizer_1.AddGrowableCol(1)
		main_sizer.Add(grid_sizer_1, 1, wx.EXPAND, 0)
		self.SetSizer(main_sizer)
		main_sizer.AddGrowableCol(0)
		# end wxGlade
	

	def LoadState (self):
		"""
		Загрузить состояние страницы из конфига
		"""
		self.__loadGeneralOptions()
		self.__loadRecentOptions()

	
	def __loadRecentOptions (self):
		"""
		Опции, связанные с последними открытыми файлами
		"""
		# Длина истории последних открытых файлов
		self.historyLength = ConfigElements.IntegerElement (Application.config.historyLengthOption, self.historySpin, 0, 30)

		# Открывать последнюю вики при запуске?
		self.autoopen = ConfigElements.BooleanElement (Application.config.autoopenOption, self.autoopenCheckBox)


	def __loadGeneralOptions (self):
		"""
		Опции для сворачивания окна в трей
		"""
		# Сворачивать в трей?
		self.minimizeToTray = ConfigElements.BooleanElement (Application.config.minimizeOption, self.minimizeCheckBox)

		# Всегда показывать иконку в трее
		self.alwaysInTray = ConfigElements.BooleanElement (Application.config.alwaysShowTrayIconOption, self.alwaysInTrayCheckBox)

		# Запускаться свернутым?
		self.startIconized = ConfigElements.BooleanElement (Application.config.startIconizedOption, self.startIconizedCheckBox)

		# Задавать вопрос перед выходом из программы?
		self.askBeforeExit = ConfigElements.BooleanElement (Application.config.askBeforeExitOption, self.askBeforeExitCheckBox)

		# Формат заголовка страницы
		self.titleFormat = ConfigElements.StringElement (Application.config.titleFormatOption, self.titleFormatText)

		self.__loadLanguages()
	

	def __loadLanguages (self):
		languages = core.i18n.getLanguages()
		languages.sort()

		self.langCombo.Clear ()
		self.langCombo.AppendItems (languages)

		currlang = Application.config.languageOption.value

		try:
			currindex = languages.index (currlang)
			self.langCombo.SetSelection (currindex)
		except ValueError:
			try:
				# Индекс для английского языка
				enindex = languages.index (u"en")
				self.langCombo.SetSelection (enindex)
			except ValueError:
				pass


	def Save(self):
		"""
		Сохранить состояние страницы в конфиг
		"""
		self.startIconized.save()
		self.minimizeToTray.save()
		self.askBeforeExit.save()
		self.historyLength.save()
		self.autoopen.save()
		self.__saveLanguage()

		if self.titleFormat.isValueChanged() or self.alwaysInTray.isValueChanged():
			self.alwaysInTray.save()
			self.titleFormat.save()
			Application.onMainWindowConfigChange()
	

	def __saveLanguage (self):
		index = self.langCombo.GetSelection()
		if index == wx.NOT_FOUND:
			return

		lang = self.langCombo.GetString (index)
		Application.config.languageOption.value = lang

	def onMinimizeToTray(self, event): # wxGlade: GeneralPanel.<event_handler>
		self.updateCheckState()
	

	def updateCheckState (self):
		"""
		Обновить стостояния чекбоксов
		"""
		if not self.minimizeCheckBox.IsChecked():
			self.startIconizedCheckBox.SetValue(False)
			self.startIconizedCheckBox.Disable()
		else:
			self.startIconizedCheckBox.Enable()

# end of class GeneralPanel


