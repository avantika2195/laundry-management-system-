# Import MySql Connector
import mysql.connector
# making MySQL connection object
mycon = mysql.connector.connect(
host='localhost', user='root',
password='1234@avantika', database='sboutique')
# making MySQL cursor object
mycur = mycon.cursor()

# To provide blank spaces in the output
def space(): 
	for i in range(1):
		print()

# To check if a customer of a given ID exists or not
def check():
	# query to select all customer IDs from the table
	qry = 'select cust_id from customer;'
	mycur.execute(qry)
	
	''' a list where each element in the list is a tuple
	fetched from each record in table
	Each tuple contains a single element as only customer IDs are fetched
	from cust_id column of each record '''
	
	d = mycur.fetchall()
	
	# to create a list of all customer IDs in the table
	list_of_ids = []
	for ids in d:
		# a list of all customer IDs in table
		list_of_ids.append(ids[0])
	return list_of_ids

# To create a new account for the customer
def cust_ac():
	ask = 'Y'
	list_of_ids = check()
	while ask in 'yY':
		custid = int(input('Enter your customer id... '))
		# to check if a customer already exists with this ID
		if custid in list_of_ids:
			print('This Customer Id already exists....\
Try creating a new one')
		else:
		# Tuple to contain details of the customer
			c_det = ()
			cnam = input('First Name : ')
			clnam = input('Last Name : ')
			cphno = input('Phone Number : ')
			cadrs = input('Your Address : ')
			c_det = (custid, cnam, clnam, cphno, cadrs)
			
			''' Values inserted in the table and default NULL value are 
				provided for booked product at the time of creation 
				of customer account '''

			qry = 'insert into customer values(%s,%s,%s,%s,%s,NULL);'
			
			# value of the fields to be entered with the query
			val = c_det
			
			mycur.execute(qry, val)
			mycon.commit()
			print('Customer details entered')
			ask = input('Do you want to continue (Y/N) ')
			if ask not in ('Yy'):
				space()
				break

# To select all booked products of a given customer from the table
def get_bkd_pro(cust_id):
	qry = 'select bkd_pro from customer where cust_id=%s;'
	mycur.execute(qry, (cust_id,))
	bp = mycur.fetchone()
	bkd_pro = bp[0]
	return bkd_pro


def sign_in():
	try:
		ask = int(input('Enter customer ID to sign in : '))
		# Using check function to check whether this account exists or not
		list_of_ids = check()
		if ask in list_of_ids:
			while True:
				print(''' Do you want to :																 
						1) View Bookings
						2) Book a product
						3) Update Self Details
						4) Cancel booked products 
							enter 'back' to exit ''')
				# Take choice of the customer
				ccc = input('enter choice - ')
				if ccc == '1':
					# Get booked product function is used where cutomer ID
					# is passed as an argument

					s = get_bkd_pro(ask)
					# To check if the column has any value
					if s is None or s == ' ':
						print('you have not booked products yet')
					else:
						''' If more than one products are booked,
						their IDs are stored as a single value
						separated by '_' so we have to split the
						string to print each product ID.'''
						
						# d is a list containing product IDs
						d = s.split('_')
						
						print('Booked products')
						for bkditems in d:
							print(bkditems)

				if ccc == '2':

					# check if the product to be booked exists or not
					qry = 'select pro_id from products;'
					mycur.execute(qry)
					pro_list = mycur.fetchall()
					''' contains a list where each element is a tuple fetched
					from each record, the tuple contains values in the
					column named pro_nam from products table.'''

					# empty list to store product IDs
					list_of_products = []
					for i in pro_list:
						list_of_products.append(i[0])

					# Take ID and quantity of product to be booked
					pro_id = input('Enter the product id to book products : ')
					# To add booked product in the column,we first
					# need to check if it already contains a value in it
					if pro_id in list_of_products:
						# Customer ID is given as value along with
						# query to fetch booked product for the given ID
						qry = 'select bkd_pro from customer where cust_id=%s;'
						mycur.execute(qry, (ask,))
						pr = mycur.fetchone()
						# prl is value fetched from table
						prl = pr[0] 
						# When the column is empty the new product is to stored
						if prl is None or prl == ' ':
							qry = 'update customer set bkd_pro=%s where cust_id=%s;'				
							val = (pro_id+'_', ask)
							mycur.execute(qry, val)
							mycon.commit()
							print('Your Product is booked !!')
							
					''' If there already exists a value in bkd_pro column,
						new value must be concatenated with the existing
						one and again stored in the table'''
					
						else:
							prl1 = prl+pro_id
							qry2 = 'update customer set bkd_pro=%s where cust_id=%s;'
							# val2 is the new value containing all booked products
							# to be stored in the column
							val2 = (prl1+'_', ask)
							mycur.execute(qry2, val2)
							mycon.commit()
							print('Your Product is booked !!')
					else:
						print('This product does not exists.\
Please write the correct product id!')

				if ccc == '3':

					qry = 'select cust_id,c_nam,c_lnam,c_phno,c_adrs\
						from customer where cust_id =%s'
					mycur.execute(qry, (ask,))
					# clist contains list of all values fetched
					# in the form of a tuple for this customer ID
					clist = mycur.fetchone()
					# list of fields to be updated
					flds = ['Name', 'Last Name', 'Ph.No', 'Address']
					dic = {}
					print("Your existing record is :")
					# The fetched details are stored in the form of key
					# value pair in a dictionary
					for i in range(4):
						dic[flds[i]] = clist[i+1]
						print(i+1, ' ', flds[i], ' : ', clist[i+1])

					for i in range(len(clist)):
						updtc = int(input('enter choice to update '))
						upval = input('enter'+flds[updtc-1]+' ')
					# Change the value corresponding to the required field
						dic[flds[updtc-1]] = upval
						yn = input(
							'Do you want to update other details? y or n ')
						if yn in 'Nn':
							break
					qry = 'update customer set c_nam=%s,c_lnam=%s,c_phno=%s,\
					c_adrs=%s where cust_id=%s;'

					updtl = tuple(dic.values())+(ask,)
					# The value to be passed along with the query is a tuple
					# containing updated details of the given customer ID
					val = (updtl)
					mycur.execute(qry, val)
					mycon.commit()
					print('Your details are are updated ')

				if ccc == '4':

					try:
						# To get the existing bookings
						# Booked products in the table
						bkd_pro = get_bkd_pro(ask)
						print('Your Booking(s) : \n ', bkd_pro)
						if bkd_pro is None or bkd_pro == ' ':
							print('you have no bookings to cancel')
						else:
							cw = input("To cancel all products; enter A \nOR \
enter the product code to cancel : ")
							if cw in 'Aa':
								qry = 'update customer set bkd_pro=NULL\
								where cust_id=%s'

								mycur.execute(qry, (ask,))
								mycon.commit()
								print('All bookings deleted')
							elif cw in bkd_pro:
								# If more than one products entered,
								# split them on the basis of '_'
								# x is a list containing all booked products
								x = (bkd_pro[0:-1]).split('_')
								
								# Delete the required product ID
								x.remove(cw)
								updt_pro = ''
								# Again concatenate each product ID
								# in the list to store in the table
								for item in x:
									updt_pro = updt_pro+item+'_'
								qry = 'update customer set bkd_pro=%s where cust_id=%s'
								val = (updt_pro, ask)
								mycur.execute(qry, val)
								mycon.commit()
								print('Booking Cancelled !')
					except Exception:
						print('Some problem in updating details.Try again')
				if ccc.lower() == 'back':
					print("Successfully logged out")
					space()
					break
		else:
			print('This Account does not exist. ')
	except Exception:
		print('Some error occurred. Try Again')


# To fetch values from all columns of 
# product table to get product details
def view_pro():
	qry = 'select * from products;'
	mycur.execute(qry)
	d = mycur.fetchall()
	# contains list of all records
	dic = {}
	# Each record fetched is separated into a key value pair
	# and stored in the dictionary where product ID is the key
	for i in d:
		dic[i[0]] = i[1:]
	print('_'*80)
# Printing the dictionary in the form of a table
	print("{:<17} {:<22} {:<23} {:<19}".format(
		'Product id', 'Product name', 'Price', 'Stock'))
	print('_'*80)
	for k, v in dic.items():
		a, b, c = v
		print("{:<17} {:<22} {:<23} {:<19}".format(k, a, b, c))
	print('_'*80)


# To add a new product in Products table
def addpro():
	# Display list of products
	view_pro() 
	n = int(input('Enter no of items to insert '))
	for j in range(n):
		# Initialize tuple to store
		# product details.
		t = ()
		pronum = input("Product No. ")
		proid = input('Product ID : ')
		pprice = int(input('Price : '))
		pstk = int(input('Stock : '))
		t = (pronum, proid, pprice, pstk)
		# Using MySql query
		qry = 'insert into products values(%s,%s,%s,%s);'
		val = t
		mycur.execute(qry, val)
		mycon.commit()
		print("Product Added")


# To delete a product from the table
def delpro():
	view_pro()
	delt = input("Enter ID of product to be deleted")
	qry = 'delete from products where pro_id=%s;'
	mycur.execute(qry, (delt,))
	mycon.commit()
	print("Product is deleted")

# For Employee Login
def emp_sign_in():
	try:
		ask = input('Enter id to sign in to the account : ')
		# To check if the employee with this ID exists or not.
		qry = 'select emp_id from employee;'
		mycur.execute(qry)
		d = mycur.fetchall()
		lis = []
		for i in d:
			lis.append(i[0])
		if ask not in lis:
			print('Enter the correct id')
		else:
			while True:
				space()
				ccc = input("1. Update delivered records\n
							2. Add a New Product \n
							3. Delete a product \n
							Enter 'Back' to logout: ")
				if ccc == '1':
					cust_id = input('Enter customer id')
					# Check if the customer has bookings or not
					bkd_pro = get_bkd_pro(cust_id)
					if bkd_pro is None or bkd_pro == ' ':
						print('This customer has no bookings ')
					else:
						print('All booking(s): ', bkd_pro)
						pro_id = input('Enter product code to\
remove the delivered product ')
						# The product IDs are stored in the form of a
						# single value separated by '_'.
						if pro_id in bkd_pro:
							x = (bkd_pro[0:-1]).split('_')
							# Returns a list of all booked products,
							# then remove the delivered product from list
							x.remove(pro_id)
							# Concatenate the existing products using '_'
							updt_pro = ''
							for i in x:
								updt_pro = updt_pro+i+'_'
							qry = 'update customer set bkd_pro=%s \
where cust_id=%s;'
							val = (updt_pro, cust_id)
							mycur.execute(qry, val)
							mycon.commit()
							print('Delivered product is removed\
from the database. ')
						else:
							print('enter the correct code')
				elif ccc == '2':
					addpro()
				elif ccc == '3':
					delpro()
				elif ccc.lower() == 'back':
					print("Successfully logged out ")
					break
	except Exception:
		print('Give the correct input')

# To add employee details
def addemp(): 
	qry = "select * from employee;"
	mycur.execute(qry)
	emp_list = mycur.fetchall()
	print("List of Employees ")
	for emp in emp_list:
		print("Emp Id : ", emp[0], " Name : ", emp[1],
			" Last Name : ", emp[2], " Phone No : ", emp[3])
	ne = []
	n = int(input('enter the no. of employees to add '))
	for i in range(1, n+1):
		t = ()
		print('enter employee id ')
		idd = int(input(str(i)+') '))
		print('Name ')
		nam = input(str(i)+') ')
		print('Last name ')
		lnam = input(str(i)+') ')
		print('Contact no. ')
		conno = int(input(str(i)+') '))
		print('Address ')
		adrs = input(str(i)+') ')
		# A tuple containing details of an employee
		t = (idd, nam, lnam, conno, adrs)
		# List containing details of n number
		# of employees to be added
		ne = ne+[t, ]
	qry = 'insert into employee values(%s,%s,%s,%s,%s);'
	# A list containing details of each employee
	# in the form of a tuple is to be passed along with the query
	for i in range(len(ne)):
		val = ne[i]
		mycur.execute(qry, val)
		mycon.commit()
	print('All Employee details added. ')
	space()


# For employer login
def employer(): 
	while True:
		print()
		print('''Enter Your Choice:													 
					1)View Product Details
					2)Add a New Employee
					enter back to exit''')
		ccc = input('Enter _____ ')
		if ccc == '1':
			view_pro()
		if ccc == '2':
			addemp()
		if ccc.lower() == "back":
			break


print('WELCOME !')
# Running a infinite loop
while True:
	print('''Are you a :												 
(A). Customer
(B). Employee
(C). Employer
enter e to exit ''')
	ch = input('Enter - ')
	try:
		if ch in 'aA':
			print(" 1. Create Account\n 2.Sign In into existing account")
			choice = input('enter- ')
			if choice == '1':
				cust_ac()
			elif choice == '2':
				sign_in()
			else:
				print('Enter correct choice')
		if ch in 'bB':
			emp_sign_in()
		if ch in 'cC':
			employer()
		elif ch.lower() == "e":
			print("Thankyou for visiting !")
			break
	except Exception:
		print('Give the right input')
	space()
