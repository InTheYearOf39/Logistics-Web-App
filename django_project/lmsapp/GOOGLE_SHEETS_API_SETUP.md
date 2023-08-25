# `SET UP GUIDE FOR GOOGLE-SHEETS & CLIENT-INTEGRATION`    

### Set up Instructions    

##### To set up google sheets:
- Log in to your google account and enable API's for:    
-- Google Sheets     
-- Google Drive    
    
- After enabling Google drive, You'll need to create service credentials.    
    Go to actions, then manage keys, to create credentials.    
    they should look like this:        

```
{
    "type": "service_account",
    "project_id": "klsx-tbdf-857634",
    "private_key_id": "1d29a01203QLecd278f3800f0c466N4HtGYkyLNxtGn5Ol1",
    "private_key": "-----BEGIN PRIVATE KEY-----\nZdg57nUHn8tbxgUb5ISswiWMqadb9jVPLmIADV\noOyTy0Q1DaYr5kdsub0su9vSX...\n-----END PRIVATE KEY-----\n",
    "client_email": "gsheets-api-read-write@klsx-tbdf-857634.iam.gserviceaccount.com",
    "client_id": "155291071757147230670",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/gsheets-api-read-write%40klsx-tbdf-857634.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
  }
  ```
- Download this file and save it as cred.json: Place it in the root directory of the last.mile.pudonet project   
- After setting up an email associated to the account should have been generated, record this email as it is what will be sent to clients. The client should add this email to the people with access on their spread sheet.    
-- It should look something like this: `gsheets-api-read-write@klsx-tbdf-857634.iam.gserviceaccount.com`.   This is the same as the client_email in the json credentials downloaded earlier.   
    
    `That's all you'll need for the set up --- next will be the client-integration pre-requisites ---`    
        




## To Integrate with client    
When the client shares their google sheet, we should be able to map the fields they have provided inorder to get this  data from them.    



`capture and map all fields from the clients sheet`
    
The json mapped object should look like this 'this assumes these are the possible fields we could map for this client'

```
    
        {
        "package_number": "Order ID", 
        "created_on": "Order Date",  
        "recipientName": "Name of\nReceiver", 
        "recipientAddress": "Delivery address", 
        "city": "City", 
        "recipientTelephone": "Phone", 
        "packageName": "Item1",
        "quantity": "QTY(pieces)"
    }
```
    
- When the mapped object has been identified it should be fitted to match the key in the object below: And the entire object pasted in the django Admin to match the client. Or They could be mapped using a form.   
```
    sample_mapping = {
        "fields": {
        "package_number": "Order ID", 
        "created_on": "Order Date",  
        "recipientName": "Name of\nReceiver", 
        "recipientAddress": "Deliery address", 
        "city": "City", 
        "recipientTelephone": "Phone", 
        "packageName": "Item1",
        "quantity": "QTY(pieces)"
    },
    "custom_fields": ["city","quantity"],
    "settings": {
        "created_on_formats": ["%d/%b/%Y", "%Y-%m-%d"],
        "non_empty_indicator_field": ["recipientName", "packageName", "recipientTelephone"],
        "all_fields_mandatory": ["created_on", "package_number", "packageName", "recipientTelephone"]
    },
    "defaults": {
        "deliveryType": "premium",
        "packageDescription": "", 
        "recipientEmail": "",
        "sendersContact": "",
            }
    }

    all_fields = ["created_on", "package_number", "packageName", "sendersName"
                    , "packageDescription", "sendersName", "sendersEmail", "sendersAddress", "sendersContact"
                    , "sender_latitude", "sender_longitude"
                    , "recipientName", "recipientEmail", "recipientTelephone"
                    , "recipientAddress", "recipientIdentification", "recipient_latitude"
                    , "recipient_longitude", "genderType"
                    , "deliveryFee", "deliveryType"]
```    

`Nothing else should be touched in the object above, If a new field is added to the models, it should be added inside the all_fields array.`    

`NOTE:` The custom fields, can be adjusted depending on a client, the settings object should not be touched, and neither should the defaults.    

The client will then have to provide the link to their google sheet. This will be added together with the mapping object at the point of creating a UserGoogleSheet instance to associate with the user on our system. 
    -- The link should look something like this:  `https://docs.google.com/spreadsheets/d/1Ub5Iadb950LGSJpRXUIBvSswiWMq_K-tTy0Q1DaYr5_S/edit?usp=sharing`    
    
    

