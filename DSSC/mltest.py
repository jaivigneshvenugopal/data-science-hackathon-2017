import urllib.request
import ast
import json

def getMostCommonCancer(gender, ageBand, alch, smoke):
    data =  {

            "Inputs": {

                    "input1":
                    {
                        "ColumnNames": ["Gender", "Band", "Alcohol Consumption", "Smoking"],
                        "Values": [ [ gender, ageBand, alch, smoke ] ]
                    },        },
                "GlobalParameters": {
    }
        }

    body = str.encode(json.dumps(data))

    url = 'https://ussouthcentral.services.azureml.net/workspaces/5b54aba369e143bdb728ccda7d66b150/services/083a962d4a4f437ca7499551306b61b6/execute?api-version=2.0&details=true'
    api_key = 'qwG6yNQw7/q+hoUygBxRzlVpIDnCUFXSr0L4rcfpDMgkCbhkMUNDVVY7h/zmf8IApM2Uj4kYfGBHuDsL9ajXLg==' 
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers) 

    try:
        req = urllib.request.Request(url, body, headers) 
        response = urllib.request.urlopen(req)

        result = response.read()
        results = result.decode("utf-8")
        resultDict = ast.literal_eval(results)
        return resultDict['Results']['output1']['value']['Values'][0][0] 
    except (urllib.HTTPError, error):
        print("The request failed with status code: " + str(error.code))

        print(error.info())

        print(json.loads(error.read()))
