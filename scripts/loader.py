
from sys import argv
import csv
import cx_Oracle as oracle
from credentials import username,password,server

# Connecting to oracle database
def connect():
	db = oracle.connect("{}/{}@{}".format(username,password,server))
	cursor = db.cursor()
	return db,cursor

def close(cursor,db):
	cursor.close()
	db.close()

def get_columns(cursor):
	sql_desc = "SELECT * FROM {} WHERE 1=0".format(argv[1])
	cursor.execute(sql_desc)
	description = cursor.description
	columns = []
	for c in description:
		columns.append(c[0])
	print columns

# DD-MMM-YYYY
def format_date(date_str):
	cal = [None,'jan','feb','mar','apr','may','jun','jul','aug','sep',
		'oct','nov','dec']
	date_split = date_str.split('-')
	date = [date_split[1], cal[int(date_split[0])], date_split[2]]
	date = '-'.join(date)
	return date

# ENTITIES
def user_data(row):
	return '(\'{}\',\'{}\')'.format(row[0],row[1])

def strategy(row):
	return '({},\'{}\')'.format(row[0],row[1])

def indicator(row):
	return '({},\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'.format(
		row[0],row[1],row[2],row[3],row[4],row[5])

def trade(row):
	return '({},\'{}\',\'{}\',{},{},\'{}\',\'{}\')'.format(
		row[0],row[1],row[2],row[3],row[4],row[5],row[6])

def portfolio_statistics(row):
	return '({},{},{},\'{}\')'.format(row[0],row[1],row[2],row[3])

# RELATIONS
def create_strategy(row):
	return '(\'{}\',{})'.format(row[0],row[1])

def criteria(row):
	return '({},{})'.format(row[0],row[1])

def indicator_reference(row):
	return '({},{},\'{}\',\'{}\',{},{},{})'.format(
		row[0],row[1],row[2],row[3],row[4],row[5],row[6])	

def action(row):
	return '({},{})'.format(row[0],row[1])

def create_portfolio(row):
	return '({},{})'.format(row[0],row[1])

def raw_data_parsing(row):
	return '({},\'{}\',\'{}\')'.format(
		row[0],row[1],format_date(row[2]))



# Reading in csv file contents
def insert_data(data,cursor,db,use):
	with open( data, 'r') as csvfile:
		data_reader = csv.reader(csvfile)
		for row in data_reader:
			sql_insert = "INSERT INTO {} VALUES {}".format(argv[1],use(row))
			print sql_insert
			cursor.execute(sql_insert)
			db.commit()


def determine_table():
	converters ={'user_data':user_data, 'strategy':strategy, 'indicator':indicator, 
		'criteria':criteria, 'indicator_reference':indicator_reference, 'trade':trade,
		'action':action, 'portfolio_statistics':portfolio_statistics,
		'create_portfolio':create_portfolio, 'raw_data_parsing':raw_data_parsing,
		'create_strategy':create_strategy}
	return converters[argv[1]]

if __name__ == '__main__':
	if len(argv) != 3:
		print 'Proper Usage:\n\tpython loader.py <table_name> <csv_file_name>' 
		exit(1)

	db,cursor = connect()

	get_columns(cursor)
	csv_file = str(argv[2])
	use = determine_table()
	insert_data(csv_file,cursor,db,use)

	close(cursor,db)
