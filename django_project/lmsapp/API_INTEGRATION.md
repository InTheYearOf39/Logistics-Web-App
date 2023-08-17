# INTEGRATING INTO LASTMILE.PUDONET API

## Expected response codes and payloads

### `sample input data`
```
{
  "sendersName": "Mugai John",
  "sendersEmail": "mgaijohn@gmail.com",
  "sendersAddress": "Nairobi",
  "sendersContact": "0789734536",
  "recipientName": "Sandra Kintu",
  "recipientEmail": "sandyk@gmail.com",
  "recipientAddress": "Kiwatule",
  "recipientContact": "0798765654",
  "recipientIdentification": "CF7654323456789UODD",
  "packageName": "Hand Bags",
  "packageDescription": "African Craft Bags",
  "packageNumber": "MC546A890"
}  
```


#### Expected success response    
```
Status: 200 OK   
    
{
  "response": {
    "success": true,
    "data": {
      "recipientName": "Sandra Kintu",
      "recipientEmail": "sandyk@gmail.com",
      "recipientAddress": "Kiwatule",
      "recipientContact": "0798765654",
      "recipientIdentification": "CF7654323456789UODD",
      "packageName": "Hand Bags",
      "packageDescription": "African Craft Bags",
      "packageNumber": "MC646A890",
      "sendersName": "Mugai John",
      "sendersEmail": "mgaijohn@gmail.com",
      "sendersAddress": "Nairobi",
      "sendersContact": "0789734536"
    }
  }
}
```



#### missing required field e.g `packageNumber`    
    

```
Status: 400 Bad Request    
    
{
  "error": "packageNumber is required"
}
```



####  duplication  
    

```
Status: 400 Bad Request
    
{
  "error": "Package number already exists"
}
```




























