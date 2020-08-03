import re
import os
import sys
import pandas as pd
from openpyxl import load_workbook

def main(root, filename):
	class_str = ''
	data = []
	for category in ['public', 'protected']:
		class_str = os.popen('cat ' + root + '/'+filename +  '| grep "'+category+' .*" | grep -v "//" | grep "(" | grep -v "*" | grep -v "="', 'r').read()
		# 每个方法以大括号结尾
		class_list = class_str.split('{')
		for i in class_list:
			# strip()去掉字符串前后的空格和'\n'
			i = i.strip()
			if i != '':
				# 如果类不是以大括号结尾，则是以'\n'作为分割
				if '\n' in i:
					i = i.split('\n')
					for j in i:
						data.append([filename, j.strip()])
				else:
					data.append([filename, i])


	columns = ['sailor中的类', '接口原型']
	df = pd.DataFrame(columns = columns, data = data)
	if not os.path.exists('data.xlsx'):
		df.to_excel('data.xlsx' ,sheet_name=filename, index=None)
	else:
	# 获取类的接口原型
		excelWriter = pd.ExcelWriter('data.xlsx', engine='openpyxl')
		book = load_workbook(excelWriter.path)
		excelWriter.book = book
		df.to_excel(excel_writer=excelWriter,sheet_name=filename, index=None)
		excelWriter.close()




if __name__ == '__main__':
	# 获取当前路径下的所有.java文件
	for root, dirs, files in os.walk('.'):
		for i in files:
			if len(re.findall('.java', i))>0:
				main(root, i)