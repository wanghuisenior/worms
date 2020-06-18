#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @FileName: menu.py
 @Author: 王辉/Administrator
 @Email: wanghui@zih718.com
 @Date: 2020/6/8 11:40
 @Description:
"""
##############
## main.pyw ##
##############
from PyQt5.QtWidgets import QDialog, QSystemTrayIcon, QMenu, QAction, QApplication
from PyQt5.QtGui import QIcon
import sys


class main(QDialog):
	def __init__(self):
		super().__init__()
		self.trayIcon = QSystemTrayIcon(self)  # <===创建通知栏托盘图标
		self.trayIconMenu = QMenu(self)  # 创建菜单
		self.loadMenu()
		self.initUI()

	# self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
	# self.tray.activated.connect(self.TuoPanEvent) #设置托盘点击事件处理函数
	def loadMenu(self):
		menuItems = [{"text": "启动", "icon": "icons/set.png", "event": self.show, "hot": "D"},
					 {"text": "退出", "icon": "icons/switch.png", "event": self.close, "hot": "Q"}]  # 菜单列表
		# 遍历绑定 显示的文字、图标、热键和点击事件
		# 热键可能是无效的 我这里只是为了显示效果而已
		for i in menuItems:
			tmp = QAction(QIcon(i["icon"]), i["text"], self, triggered=i["event"])
			tmp.setShortcut(self.tr(i["hot"]))
			self.trayIconMenu.addAction(tmp)

	def initUI(self):
		self.trayIcon.setIcon(QIcon("icons/alert.png"))  # <===设置托盘图标
		self.trayIcon.setContextMenu(self.trayIconMenu)  # <===创建右键连接菜单
		self.trayIcon.show()  # <====显示托盘
		# self.trayIcon.setToolTip('aa')
		self.setWindowIcon(QIcon("icons/alert.png"))  # <===设置窗体图标
		self.setGeometry(900, 300, 180, 300)  # <===设置窗体打开位置与宽高
		self.setWindowTitle('订单列表')

	# self.show()  # <====显示窗体

	# self.hide()#<====隐藏窗体
	# 默认不显示窗体

	def close(self):
		sys.exit(0)

	# 重写窗体关闭事件,让其点击关闭时隐藏
	def closeEvent(self, event):
		if self.trayIcon.isVisible():
			self.hide()
			event.ignore()
		else:
			event.accept()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = main()
	sys.exit(app.exec_())
