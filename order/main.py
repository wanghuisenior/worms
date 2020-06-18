#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @FileName: main.py
 @Author: 王辉/Administrator
 @Email: wanghui@zih718.com
 @Date: 2020/6/8 17:15
 @Description:
"""
import json
import sys
import random
from time import sleep

import requests
from PyQt5.QtCore import QThread, QTimer, Qt
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QSystemTrayIcon, QMenu, QAction, QApplication, QWidget, qApp, QMessageBox, \
	QLineEdit, QFormLayout, QTableWidget, QAbstractItemView, QPushButton, QHBoxLayout, QHeaderView, QTableWidgetItem
from PyQt5.QtGui import QIcon, QFont


class TrayIcon(QSystemTrayIcon):
	def __init__(self, parent=None):
		super(TrayIcon, self).__init__(parent)
		self.showMenu()
		self.other()

	def showMenu(self):
		"设计托盘的菜单，这里我实现了一个二级菜单"
		self.menu = QMenu()
		self.showAction = QAction(QIcon("icons/set.png"), "启动", self, triggered=self.showM)
		self.quitAction = QAction(QIcon("icons/switch.png"), "退出", self, triggered=self.quit)
		self.menu.addAction(self.showAction)
		self.menu.addAction(self.quitAction)
		self.setContextMenu(self.menu)

	def other(self):
		self.activated.connect(self.iconClied)
		# 把鼠标点击图标的信号和槽连接
		self.messageClicked.connect(self.mClied)
		# 把鼠标点击弹出消息的信号和槽连接
		self.setIcon(QIcon("icons/alert.png"))
		self.icon = self.MessageIcon()

	# 设置图标

	def iconClied(self, reason):
		"鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击"
		# if reason == 2 or reason == 3:
		if reason == 2:
			pw = self.parent()
			if pw.isVisible():
				pw.hide()
			else:
				pw.show()

	def mClied(self):
		self.showMessage("提示", "你点了消息", self.icon)

	def showM(self):
		# self.showMessage("测试", "我是消息", self.icon)
		pw = self.parent()
		pw.show()

	def quit(self):
		"保险起见，为了完整的退出"
		# self.setVisible(False)
		# self.parent().exit()
		# qApp.quit()
		sys.exit()


class window(QWidget):
	def __init__(self, parent=None):
		super(window, self).__init__(parent)
		ti = TrayIcon(self)
		ti.show()
		self.initUI()
		self.session = getSession()

	def closeEvent(self, event):
		# reply = QMessageBox.question(self, '提示', '确认退出吗?',
		# 							 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		#
		# if reply == QMessageBox.Yes:
		# 	event.accept()
		# else:
		# 	event.ignore()
		# 隐藏窗口，同时使关闭事件失效
		self.hide()
		event.ignore()

	def initUI(self):
		self.setWindowIcon(QIcon("icons/alert.png"))  # <===设置窗体图标
		# self.setGeometry(900, 300, 180, 300)  # <===设置窗体打开位置与宽高
		self.setWindowTitle('订单列表')
		############################
		# layout = QFormLayout()
		# self.edita3 = QLineEdit()
		# self.edita4 = QLineEdit()
		# self.edita5 = QLineEdit()
		# layout.addRow("A数值", self.edita3)
		# layout.addRow("B数值", self.edita4)
		# layout.addRow("C数值", self.edita5)
		# self.setLayout(layout)
		self.Mytimer()
		self.resize(800, 550)
		layout = QHBoxLayout()

		self.table = QTableWidget(self)
		self.table.setRowCount(10)
		self.table.setColumnCount(5)
		self.table.setHorizontalHeaderLabels(['预约号', '菜品名称', '数量', '备注', '操作'])  # 设置行表头
		# 自定义列宽
		self.table.setColumnWidth(0, 120)
		self.table.setColumnWidth(1, 250)
		self.table.setColumnWidth(2, 60)
		self.table.setColumnWidth(3, 200)
		self.table.setColumnWidth(4, 140)
		#################################### 设置水平方向表格为自适应的伸缩模式###################################
		# self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 将表格变为禁止编辑
		self.table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置表格整行选中
		# 将行与列的高度设置为所显示的内容的宽度高度匹配
		# QTableWidget.resizeColumnsToContents(self.table)
		# QTableWidget.resizeRowsToContents(self.table)
		# self.table.horizontalHeader().setVisible(False)
		self.table.verticalHeader().setVisible(False)  # 隐藏列表头
		# newItem = QTableWidgetItem('1234')
		# newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
		# newItem.setFont(QFont('Times', 12, QFont.Black))
		# self.table.setItem(0, 0, newItem)
		# newItem = QTableWidgetItem('男法计算的飞机发射点发放大算法放大算法阿道夫阿斯弗阿刁爱的发声 的设计覅')
		# newItem.setFont(QFont('Times', 12, QFont.Black))
		# self.table.setItem(0, 1, newItem)
		# newItem = QTableWidgetItem('160')
		# newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
		# self.table.setItem(0, 2, newItem)
		layout.addWidget(self.table)

		for i in range(self.table.rowCount()):
			self.table.setRowHeight(i, 50)
			self.table.setItem(i, 4, QTableWidgetItem('操作按钮'))
		self.setLayout(layout)

		# self.table_insert()

		# self.table.itemChanged.connect(self.table_update)

		# self.delete_button = QPushButton(self)
		# self.delete_button.move(230, 350)
		# self.delete_button.setFixedWidth(100)
		# self.delete_button.setFixedHeight(32)
		# self.delete_button.clicked.connect(self.table_delete)
		# self.delete_button.setText("Delete")
		#
		# self.setGeometry(200, 200, 570, 400)
		# self.show()
		pass

	def Mytimer(self):
		timer = QTimer(self)
		timer.timeout.connect(self.update)
		timer.start(1000 * 5)  # 每5秒调用一次 update() 函数

	def update(self):
		# self.edita3.setText(str(T_value))
		# self.edita4.setText(str(P_value))
		# global SUM_value
		# SUM_value = T_value + P_value
		# self.edita5.setText(str(SUM_value))
		# print(len(orders))
		res = requestBySession(self.session)
		# print(res)
		orders=[]
		number = res['waitPayOrder']
		if not number:
			orderVoList = res['orderVoList']
			for o in orderVoList:
				if o['orderStatus'] == '已完成':
					orders.append({'orderId': o['orderNumber'][-4:],
								   'time': o['endTime'],
								   'orderItem': o['orderItem'],
								   'remark': o['remark']})
		else:
			print('没有新订单')
		i = 0
		size = 0
		# self.table.clearContents()  # 清空原始数据
		print(orders)
		for d in orders:
			order_number = str(d['orderId'])
			remark = d['remark']
			dishes = d['orderItem']
			size = len(dishes)
			for dish in dishes:
				dish_name = dish['itemName']
				num = dish['number']
				# print(i, order_number, dish_name, num)
				item00 = QTableWidgetItem(order_number)
				item01 = QTableWidgetItem(dish_name)
				item02 = QTableWidgetItem(str(num))
				item03 = QTableWidgetItem(remark)
				item00.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
				item02.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
				item00.setFont(QFont('Times', 12, QFont.Black))
				item01.setFont(QFont('Times', 12, QFont.Black))
				self.table.setItem(i, 0, item00)
				self.table.setItem(i, 1, item01)
				self.table.setItem(i, 2, item02)
				self.table.setItem(i, 3, item03)
				self.table.setSpan(0, 0, 2, 0)
				i += 1
			# print(i - size, 0, size, 1)
			self.table.setSpan(i - size, 0, size, 1)  # 合并单元格


def getSession():
	headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac 05 X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
	}
	session = requests.Session()
	session.post(url="http://www.zitcloud.cn/login",
				 data={'username': '13253538977', 'password': '13253538977'},
				 headers=headers)
	session.get(url='http://www.zitcloud.cn/user/xcx/manage/43', headers=headers)
	return session


def requestBySession(session):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac 05 X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
	}
	res = json.loads(session.get(
		url='http://xcx.zitcloud.cn/api/restaurant/order/orderList?page_size=100&page=0&type=8&restaurantid=179',
		headers=headers
	).text)
	print('请求成功...')
	return res


if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = window()
	w.show()
	# workThread = WorkThread()
	# workThread.start()
	sys.exit(app.exec_())
