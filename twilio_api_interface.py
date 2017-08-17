from twilio.rest import Client
from flask import Flask, redirect, request
from twilio.twiml.messaging_response import MessagingResponse
import json
from requests.auth import HTTPBasicAuth
import requests


app = Flask(__name__)
our_number = "+12069813239"
shopify_API_key = '050e6e4e42481d41214b5949f37d2da1'
shopify_API_pass = '8b9a5636bcbe3898cc4433ec31fb38f1'


def json_to_dictionary(json_string):
	'''
	Convert the json file returned by the shopify orders api to a dictionary
	
	@type json_string: string
	@param json_string: json_string containing order details
	
	@rtype: dict
	@return: dictionary of order details, for example, id: ..., shipping_lines: ..., ...
	'''
	json_string_temp = json_string[9:-1] #removing the prefix '{"order":' and suffix '}' from the string.
	dictionary = json.loads(json_string_temp)
	return dictionary

def get_line_items_dictionary(json_string):
	'''
	Convert the line_item details in json file returned by the shopify orders api to a dictionary
	
	@type json_string: string
	@param json_string: json_string containing order details
	
	@rtype: dict
	@return: dictionary of line item details, for example, name: ..., quantity: ..., ...
	'''
	temp_string = json_string.split('line_items":[',1)[1]
	temp_string = temp_string.split('"shipping_lines"',1)[0][0:-2]
	line_items_dictionary = json.loads(temp_string)
	return line_items_dictionary


def get_artisan_phone_number(product_id):
	'''
	Method that takes the product id and queries Adisa database for the artisan's phone number	
	
	@type product_id: int
	@param product_id: number representing the product in the database
	
	@rtype: str
	@return: Artisan's phone number
	'''
	pass


def get_shopify_order_details(id):
	'''
	Method that calls the shopify orders api and returns a string in json format
	with the details of the purchased item

	@type id: str
	@param id: id of transaction
	
	@rtype: str
	@return: string containing order information in json format
	'''
	base_url = "https://shopadisa.myshopify.com/admin/orders/%s.json"  % id
	response = requests.get(base_url, auth=(shopify_API_key, shopify_API_pass))
	return response.content


def update_database(dictionary, status):
	'''
	Method that updates the sale info in our database with status (aka purchased, delivered, etc)

	@type dictionary: dict
	@param dictionary: dictionary containing order details
	
	@type status: str
	@param status: the status of the order i.e. purchases, delivered, etc.
	'''
	pass


def send_artisan_confirmation(line_items_dictionary, dictionary, artisan_phone_number):
	'''
	Method that uses extracted information to message the artisan with the tracking number for confirmation

	@type line_items_dictionary: dict
	@param line_items_dictionary: dictionary containing line item details
	
	@type dictionary: dict
	@param dictionary: dictionary containing order details

	@type artisan_phone_number: str
	@param status: the phone number of the artisan to be texted
	'''

	#These keys are hard coded from the twilio site, they give us access to our purchased number
	account_sid = "AC5c28e8e1e47b705b518337506b1f4fe0"
	auth_token = "623d65e8232424274dac8ddd63a716d6"
	client = Client(account_sid, auth_token)
	product_name = str(line_items_dictionary['title'])
	product_id= str(dictionary["id"])
	quantity = str(line_items_dictionary['quantity'])
	vendor = str(line_items_dictionary['vendor'])

	client.messages.create(
		to=artisan_phone_number,
	 	from_=our_number,
	 	body= "Hello %s! \nCongratulations, you have a new order with the following details: \n" % vendor +
	 	"\nProduct Name: " + product_name + "\n" +
	 	"Product ID: " + product_id + "\n" +
	 	"Quantity: " + quantity + "\n" +
	 	 "\nPlease deliver the item(s) to your local Adisan store. If you have any questions, " +
	 	  "please call %s.Your payment will be processed shortly. Thank you, Adisa LLC" %  our_number)
		

@app.route("/<id>", methods=["GET", "POST"])
def main(id):
	'''
	Main function that executes all the backend

	@type id: str
	@param id: id of the transaction
	
	'''
	json_string = get_shopify_order_details(id)
	dictionary = json_to_dictionary(json_string)
	line_items_dictionary = get_line_items_dictionary(json_string)
	#update_database(dictionary)
	#artisan_phone_number = get_artisan_phone_number(dictionary)
	send_artisan_confirmation(line_items_dictionary, dictionary,'+16123561005')

if __name__ =="__main__":
	app.run(debug=True)
