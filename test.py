#To run programm from terminal type "python test.py x y" where 'x' is the product id and 'y' is the product quantity

import requests
import sys
import json

#Set test data to variable testData from Data.json file 
testData = open('Data.json')
testData = json.load(testData)

#Set email and password values to variables 
loginEmail = testData['email']
loginPassword = testData['password']

#Define login payload structure
loginPayload = {"email": loginEmail, "password": loginPassword}

#Call login request and set response to variable
loginResnonse = requests.post("https://webqa.mercdev.com/api/v1/user/login", data = loginPayload)

#Check if authorization is successful
if loginResnonse.status_code == 200 :
     print('1. Authorization is successful')
else :
     print('1. Authorization error, check your credentials')

#Set autorization token from login response to variable
authToken = json.loads(loginResnonse.text)['authToken']

#Define autorization header
authHeader = {"authorization": authToken}

#Call product get request and set response to variable
productResponse  = requests.get("https://webqa.mercdev.com/api/v1/product/", headers = authHeader)

#Check if product list has been recieved
productResponseExpectedText = '"price":100,"iamgeUrl":"/uploads/images/16a474d19f.png"},{"id":"2","description":'
if productResponse.status_code == 200 and productResponseExpectedText in productResponse.text :
     print('2. Product list successfully recieved')
else :
     print('2. Product list hasnt been recieved')

#Set payment card credentials to variables
cardNumber = testData['cardNumber']
cardName = testData['cardName']
cardDate = testData['cardDate']
cardCvc = testData['cardCvc']

#Set product Id and product quantity to variables
productId = sys.argv[1]
productQty = int(sys.argv[2])

#Define payment payload structure
paymentPayload = {
    "card": {
        "number": cardNumber,
        "date": cardDate,
        "name": cardName,
        "cvv": cardCvc
    },
    "products": [{
            "id": productId,
            "quantity": productQty
        }
    ]
}

#Call payment post request and set response to variable
paymentResponse = requests.post('https://webqa.mercdev.com/api/v1/order/createAndPay', headers = authHeader, json = paymentPayload)
#if paymentResponse.status_code == 200 : print('payment ok')

#Check amount calculation
paymentResponseBody = paymentResponse.json()
orderProductPrice = paymentResponseBody['transaction']['order']['products'][0]['product']['price']
orderProductQty = paymentResponseBody['transaction']['order']['products'][0]['quantity']
orderTotalQty = paymentResponseBody['transaction']['order']['totalQuantity']
orderExpectedAmount = orderProductPrice*orderProductQty
orderActualAmount = paymentResponseBody['transaction']['order']['totalSum']

if orderTotalQty >= 3 : 
     orderExpectedAmount = orderExpectedAmount*0.9

if orderExpectedAmount == orderActualAmount :
     print("3. Payment successful. Expected order amount matches actual order amount")
else :
     print("3. Error. Order expected amount doesn't match actual amount")
     print("Expected amount: ", orderExpectedAmount)
     print("Actual amount: ", orderActualAmount)