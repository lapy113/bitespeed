# bitespeed

endpoint - > https://bitespeed-api.onrender.com/identify

Sample payload json/application

{
    "phoneNumber": "3",
    "email":"2@g.com"
}

One customer can have multiple **`Contact`** rows in the database against them. All of the rows are linked together with the oldest one being treated as "primary” and the rest as “secondary” . 

`**Contact`** rows are linked if they have either of **`email`** or **********`phone`** as common.

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
Upon ordering with common phone/email, those two accounts can be linked and user will not get commision.

Request
```
{
	"email": "mcfly@hillvalley.edu",
	"phoneNumber": "123456"
}
```

Response
```

{
	"contact":{
		"primaryContatctId": 1,
		"emails": ["lorraine@hillvalley.edu","mcfly@hillvalley.edu"]
		"phoneNumbers": ["123456"]
		"secondaryContactIds": [23]
	}
}
```

### But what happens if there are no existing **contacts** against an incoming request?

The service will simply create a new `**Contact**` row with `linkPrecedence=”primary"` treating it as a new customer and return it with an empty array for `secondaryContactIds`

### When is a secondary contact created?

If an incoming request has either of `phoneNumber` or `email` common to an existing contact but contains new information, the service will create a “secondary” **************`Contact`** row.
