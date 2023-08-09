# bitespeed

endpoint - > https://bitespeed-api.onrender.com/identify

Sample payload json/application

{
    "phoneNumber": "3",
    "email":"2@g.com"
}


The API can be used to detect and prevent misuse of Affiliate program by linking multiple accounts
in an e-commerce website, so a person participating in the program cannot use their other account to order 
and get commision on those orders.

If a customer placed an order with 
```
email=lorraine@hillvalley.edu
phoneNumber=123456 
```
and later came back to place another order with 
```
email=mcfly@hillvalley.edu & phoneNumber=123456
```
database will have the following rows:

```
{
	id                   1                   
  phoneNumber          "123456"
  email                "lorraine@hillvalley.edu"
  linkedId             null
  linkPrecedence       "primary"
  createdAt            2023-04-01 00:00:00.374+00              
  updatedAt            2023-04-01 00:00:00.374+00              
  deletedAt            null
},
{
	id                   23                   
  phoneNumber          "123456"
  email                "mcfly@hillvalley.edu"
  linkedId             1
  linkPrecedence       "secondary"
  createdAt            2023-04-20 05:30:00.11+00              
  updatedAt            2023-04-20 05:30:00.11+00              
  deletedAt            null
}
```
