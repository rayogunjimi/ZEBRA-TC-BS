import csv
import os
import sys
from datetime import datetime

# expected format: IdpNum,CustomerNum,SecondaryCustomerNum,StoreNum,SbuNum,ItemCode,ItemDescription,TicketableFlag,OrderableFlag,InclusionFlag,SapItemCode,UpcNum,OrderCategory,CaseCount,Wholesale,Retail,DiscountAmt

#os.system("cd /sdcard0")

#Original %d/%m/%Y %H:%M:%S
print("It is " , datetime.now().strftime("D%dM%mY%Y_H%HM%MS%S") , ".\n")
print("Working driectory is ", os.getcwd() , ".\n")
print("List of files in working directory is ", os.listdir() , ".\n")

product_dict = {}

print("Finding file...")

with open('product_list_v2.csv', mode='r') as in_file:
	print("File found.")
	product_list = csv.reader(in_file)
	next(product_list)
	print("Building List...")
	for rows in product_list:
		#key: pos 11 --> UPC
		#data: pos 6 --> ItemDescription
		#data: pos n/a --> quantity
		product_dict[str(rows[11])]=[rows[6],0]
	print("List built.")



print("Scan or enter quantity.")
print("Type 'q' to quit.")
print("Ready for scan...")

key_mem = -1

for code in sys.stdin:
	code=code.rstrip()
	if code == 'q':
		break
	elif not code.isnumeric():
		print("Omitted: code must be numeric.")
	elif len(code) < 12 and key_mem != -1:
		product_dict[key_mem] = [temp[0],temp[1]+int(code)-1]
		key_mem = -1
	elif len(code) < 12 and key_mem == -1:
		print("Omitted: previous input was not a valid UPC.")
	elif product_dict.get(code) is not None:
		temp = product_dict[code]
		print(temp[0] + " scanned.")
		print("UPC is " + code + ".")
		product_dict[code] = [temp[0],temp[1]+1]
		key_mem = int(code)
	else:
		print("Omitted: unknown product.")
		key_mem = -1
	print("Ready for next scan...")
	
print("Done scanning.")

print("Making file.")
with open("order_"+datetime.now().strftime("D%dM%mY%Y_H%HM%MS%S")+".csv", mode='w+') as out_file:
	sys.stdout = out_file
	print("brand, item_number, item_description, cases_per_week, number_found")
	for key in product_dict:
		temp = product_dict[key]
		if temp[3] != 0:
			print(temp[0] + "," + key + "," + temp[1] + "," + temp[2] + "," + str(temp[3]) )
	sys.stdout = sys.__stdout__
	print("File made.")















