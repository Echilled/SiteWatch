# SiteWatch

An interactive monitoring tool 

## JSON Formatting
The appropriate file format for the JSON file to store URL properties, 'WebHash.json' are as follows,
The JSON file, 'WebHash.json' should also be in the archive folder at all times
The Input JSON File, 'WebHash.json',  for SiteWatch should look something like this: 

```json
{
    "URLs": {
        "https://time.gov": {
            "properties": {
                "hash": "B14ACCD32BFD5C5F02192C4711510895",
                "archival_date": "2022-07-31 00:39:58",
                "number of times URL content change": 33
            }
        },
        "http://randomcolour.com": {
            "properties": {
                "hash": "44C1F541B08858095C829289D04EDEDA",
                "archival_date": "2022-07-31 00:40:03",
                "number of times URL content change": 25
            }
        },
        "https://www.ledr.com/colours/multi.htm": {
            "properties": {
                "hash": "0DEBC77372740436519994B42B14A784",
                "archival_date": "2022-07-31 00:40:04",
                "number of times URL content change": 0
            }
        },
        "https://www.ledr.com/colours/grey.htm": {
            "properties": {
                "hash": "EFDF4B6BFEB675B0DA3039D986FD9537",
                "archival_date": "2022-07-31 00:40:05",
                "number of times URL content change": 0
            }
        }
    }
}
```

## Formatting examples
Ensure that the Input JSON file has URL as the key and the appropriate properties: 'hash', 'archival_date' and 'number of times URL content change'. If any of these keys ("URLs", input URLs and "properties") or properties ("hash", "archival_date",  "number of times URL content change") are missing, then it will return an error and the file will not be processed. 


Please feel free to use the template above to format your own JSON file with the relevant values. 

### Accepted JSON Format:
```json
{
    "URLs": {
        "https://time.gov": {
            "properties": {
                "hash": "",
                "archival_date": "",
                "number of times URL content change": 1
            }
        },
        "http://randomcolour.com": {
            "properties": {
                "hash": "",
                "archival_date": "",
                "number of times URL content change": 1
            }
        },
        "https://www.ledr.com/colours/multi.htm": {
            "properties": {
                "hash": "",
                "archival_date": "",
                "number of times URL content change": 0
            }
        },
        "https://www.ledr.com/colours/grey.htm": {
            "properties": {
                "hash": "",
                "archival_date": "",
                "number of times URL content change": 0
            }
        }
    }
}
````
If you are unsure about the previous properties of the URLs, you can leave them in the format shown above. Ensure that each property, even if it is blank, it still contains the value "". SiteWatch will update the value accordingly after every monitoring cycle. Appropriate JSON file formatting is crucial if you want SiteWatch to work as intended

### Unacceptable JSON Format:
```json
{
    "URLs": {
        "https://time.gov": {
            "properties": {
                "hash": ,
                "archival_date": ""
                "number of times URL content change": 
            }
        },
        "http://randomcolour.com": {
            "properties": {
                "hash": ""
                "archival_date": ""
                "number of times URL content change": 1
            }
        },
        "https://www.ledr.com/colours/multi.htm": {
            "properties": {
                "hash": "",
                "archival_date": "",
                "number of times URL content change": 0
            }
        },
        "https://www.ledr.com/colours/grey.htm": {
            "properties": {
                "hash": "",
                "archival_date": "",
                "number of times URL content change": 0
            }
        }
    }
}
````
As seen above, this is an example of an unacceptable JSON File format, there are missing values for properties of the first URL, no comma after the value of "archival_date". The placement of commas, curly braces, keys and values must be strictly adhered to as shown in the accepted example for SiteWatch to work as intended.# SiteWatch
