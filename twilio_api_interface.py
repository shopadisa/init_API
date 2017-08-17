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

#abstract method that when the url is called, this file will extract the information given by the shopify site
#returns it in a dictionary format
def json_to_dictionary(json_string):
	json_string_temp = json_string[9:-1] #removing the prefix '{"order":' and suffix '}' from the string.
	dictionary = json.loads(json_string_temp)
	return dictionary

def get_line_items_dictionary(json_string):
	temp_string = json_string.split('line_items":[',1)[1]
	temp_string = temp_string.split('"shipping_lines"',1)[0][0:-2]
	line_items_dictionary = json.loads(temp_string)
	return line_items_dictionary
#abstract method that takes the dictionary and makes requests to our database based the item. 
#Returns artisans phone number	
def get_artisan_phone_number(dictionary):
	pass

#abstract method that calls the shopify api that returns the details on the purchased item
#returns json file
def get_shopify_order_details(id):
	# base_url = "http://%s:%s@shopadisa.myshopify.com/admin/orders/%s.json"  % ('050e6e4e42481d41214b5949f37d2da1', '8b9a5636bcbe3898cc4433ec31fb38f1', id)
	base_url = "https://shopadisa.myshopify.com/admin/orders/%s.json"  % id
	response = requests.get(base_url, auth=(shopify_API_key, shopify_API_pass))
	return response.content

#abstract method that updates the sale info in our database with String status (aka purchased, delivered, etc)
#returns nothing
def update_database(dictionary, status):
	pass

#method that uses extracted information to message the artisan with the tracking number for confirmation
#NOTE: ADD TIMESTAMP
def send_artisan_confirmation(line_items_dictionary, dictionary, artisan_phone_number):
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
		


#main function that executes all the backend
#first calls the shopify API with the id number that is passed through the url
#upon the return of the JSON file containing the item info, that is converted to a dictionary
#and then used to reference our database to get the artisan phone number and update the sale status.
#Then the artisan is sent a text message based on the retrieved phone number.
@app.route("/<id>", methods=["GET", "POST"])
def main(id):
		
	json_string = get_shopify_order_details(id)
	dick = json_to_dictionary(json_string)
	smoalerr_dick = get_line_items_dictionary(json_string)
	#update_database(dictionary)
	#artisan_phone_number = get_artisan_phone_number(dictionary)
	send_artisan_confirmation(smoalerr_dick, dick,'+12064994335')
	return("The deed is done.")



if __name__ =="__main__":
	app.run(debug=True)






