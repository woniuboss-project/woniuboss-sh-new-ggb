# -*- coding: utf-8 -*-#
#-------------------------------------------------------------------------------
# Name:         utility
# Description:  
# Author:       Administrator
# Date:         2020/2/10
#-------------------------------------------------------------------------------

# 将类似于文件读写及其它工具类方法都在此存放
# 对类中的方法增加装饰器@classmethod,则该方法可以被类直接访问
# 该模块中的方法应该不依赖于具体的应用，也不应该依赖于具体的库
# 该模块中主要的方法是：


import xlrd
class Utility:

	# 从某个路径读取文本文件内容
	@classmethod
	def get_txt(cls,path):
		with open(path,encoding='utf8') as file:
			return file.readlines()

	# 将包含换行的列表转化为不包含换行的列表
	@classmethod
	def trans_str(cls,path):
		contents = cls.get_txt(path)
		li = []
		for content in contents:
			if not content.startswith('#'):
				li.append(content.strip())
		return li

	# 将文本读取的内容进行转化处理,由于测试数据的每一项有具体涵义，所以转化为[(),(),()]
	@classmethod
	def trans_txt_tuple(cls,path):
		li = []
		contents = cls.get_txt(path)
		for content in contents:
			if not content.startswith("#"):
				temp = content.strip().split(',')
				tup = tuple(temp)
				li.append(tup)
		return li

	# 读取json文件中的内容
	# json是用于存储和数据传递的格式之一.txt是无格式的，处理起来比较麻烦
	# excel，xml，json（key:value）
	@classmethod
	def get_json(cls,path):
		import json
		with open(path) as file:
			contents = json.load(file)
		return contents

	# 传入两个值，判断这两个值是否相同.断言相等
	@classmethod
	def assert_equals(cls,expect,actual):
		if expect == actual:
			return True
		else:
			return False

	# 获取数据库连接
	# 依赖于配置文件的规则
	@classmethod
	def getConn(cls,base_conf_path):
		import pymysql
		db_info = cls.get_json(base_conf_path)
		# 依赖于json数据格式
		return pymysql.connect(db_info['HOSTNAME'], db_info['DBUSER'], db_info['DBPASSWORD'], db_info['DBNAME'], charset='utf8')

	# 查询一条记录
	@classmethod
	def query_one(cls, base_conf_path,sql):
		# 获取数据库连接对象
		conn = cls.getConn(base_conf_path)
		cursor = conn.cursor()
		cursor.execute(sql)
		result = cursor.fetchone()
		cursor.close()
		conn.close()
		# 返回一维元组
		return result

	# 查询多条记录
	@classmethod
	def query_all(cls,base_conf_path, sql):
		# 获取数据库连接对象
		conn = cls.getConn(base_conf_path)
		cursor = conn.cursor()
		cursor.execute(sql)
		result = cursor.fetchall()
		cursor.close()
		conn.close()
		# 返回二维元组
		return result

	@classmethod
	def db_query_dict(cls, db_path, sql):
		db_info = cls.get_json(db_path)
		import pymysql
		conn = pymysql.connect(db_info['HOSTNAME'], db_info['DBUSER'], db_info['DBPASSWORD'], db_info['DBNAME'],
							   charset='utf8')
		from pymysql.cursors import SSDictCursor
		cur = conn.cursor(cursor=SSDictCursor)
		cur.execute(sql)
		result = cur.fetchall()
		cur.close()
		conn.close()
		return result

	# 更新记录
	@classmethod
	def update_data(cls,base_conf_path, sql):
		flag = False
		try:
			conn = cls.getConn(base_conf_path)
			cursor = conn.cursor()
			cursor.execute(sql)
			# 将数据真正提交到数据库中
			conn.commit()
			flag = True
		finally:
			cursor.close()
			conn.close()
			# 不管更新操作是否成功，都会返回真或假的结果
			return flag

	# 从excel中读取内容，读取结果为[{},{},{}]
	# 传递的参数是字典，包含的键是固定值
	@classmethod
	def get_excel_to_dict(cls,xls_file_info):
		# 将excel文件读取到内存中
		workbook = xlrd.open_workbook(xls_file_info['DATAPATH'])
		# 可以根据sheet页的下标或者名称读取sheet页中的内容.下标从0开始
		contents = workbook.sheet_by_name(xls_file_info['SHEETNAME'])
		# contents = workbook.sheet_by_index(0)
		# 读取的目标是[{},{},{}]
		# 定义列表用于存储当前sheet页中的测试信息（测试数据+预期结果）
		test_info = []

		# 按行读取每一条测试信息
		for i in range(xls_file_info['STARTROW'],xls_file_info['ENDROW']):
			# 读取单元格中的内容
			data = contents.cell(i,xls_file_info['DATACOL']).value
			# 读取期望结果列
			expect = contents.cell(i,xls_file_info['EXPECTCOL']).value
			# 获取的是列表
			temp = data.split('\n')
			d = {}
			for t in temp:
				# 给字典添加内容：dict[key] = value
				d[t.split('=')[0]] = t.split('=')[1]
			d['expect'] = expect
			test_info.append(d)
		# 将结果返回
		return test_info


	# 从excel中读取内容，读取结果为[(),(),()]
	@classmethod
	def get_excel_to_tuple(cls,xls_file_info):
		result = cls.get_excel_to_dict(xls_file_info)
		li = []
		for di in result:
			# 通过tuple(dict.vlues())将值集转化为元组
			tup = tuple(di.values())
			li.append(tup)
		return li
	@classmethod
	def get_number(cls,str,split_flag):

		b = str.split(split_flag)[1]
		import re
		number_list = re.findall(r'\d+', b)
		number=number_list[-1]
		return number



if __name__ == '__main__':

	# test_info = Utility.get_json('..\\config\\testdata.conf')
	# Utility.get_excel_to_tuple(test_info[0])
	# n=Utility.get_number('显示第 1 到第 5 条记录，总共 15 条记录','总共')
	# print(n)
	# sql='select count(*)as total from customer'
	# a=Utility().db_query_dict('..\\config\\base.conf',sql)[0]['total']
	# print(type(a))
	test_config_info = Utility.get_json('..\\config\\testdata.conf')
	# train_info = Utility.get_excel_to_tuple(test_config_info[1])
	# train_worker = Utility.get_excel_to_tuple(test_config_info[2])
	# train_status = Utility.get_excel_to_tuple(test_config_info[3])
	# train_source = Utility.get_excel_to_tuple(test_config_info[4])
	# train_time = Utility.get_excel_to_tuple(test_config_info[5])

	# print(train_time)

	train_whole = Utility.get_excel_to_tuple(test_config_info[7])
	print(train_whole)