#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Необходимые классы для создания страниц с текстом
"""

import os.path

from core.tree import WikiPage, createPage
from pages.text.TextPanel import TextPanel
import core.exceptions


class TextWikiPage (WikiPage):
	"""
	Класс HTML-страниц
	"""
	def __init__(self, path, title, parent, readonly = False):
		WikiPage.__init__ (self, path, title, parent, readonly)
	

	@staticmethod
	def getType ():
		return u"text"


class TextPageFactory (object):
	@staticmethod
	def getPageType():
		return TextWikiPage

	@staticmethod
	def getTypeString ():
		return TextPageFactory.getPageType().getType()

	# Название страницы, показываемое пользователю
	title = _(u"Text Page")

	def __init__ (self):
		pass


	@staticmethod
	def create (parent, title, tags):
		"""
		Создать страницу. Вызывать этот метод вместо конструктора
		"""
		return createPage (TextPageFactory.getPageType(), parent, title, tags)



	@staticmethod
	def getPageView (page, parent):
		"""
		Вернуть контрол, котоырй будет отображать и редактировать страницу
		"""
		return TextPanel (page, parent)


	@staticmethod
	def getPrefPanels (parent):
		return []

