import requests
import json

question = 'What is the funniest movie ever made?'


def putQuestionInJson():
  with open('data.json') as f:
    for item in data['messages']:
      print(item['content'])
      item['content'] = question
  json.dump(data, f)


def getData():
  with open('data.json', 'r') as f:
    data = json.load(f)
    print(data)
  return data


def getHeaders():
  with open('headers.json', 'r') as f:
    headers = json.load(f)
    print("in headers: ", headers)
  return headers


def makeOpenAIRequest():
  url = 'https://api.openai.com/v1/chat/completions'

  headers = getHeaders()
  print(headers)
  data = getData()
  print(data)

  response = requests.post(url, headers=headers, json=data)
  #response = response.json()
  if response.status_code == 200:
    print("Response : ")
    print(response.json())
    response = response.json()
    print("The type of your response is: ", type(response))
    #with open('responseJsonDictionary.json') as f:
      #for item in data['messages']:
        #print(response['content'])
      #f.write(response)
    #response = response.toString()
    #jsonResponse = json.loads(response)
    content = response['choices'][0]['message']['content']
    print("Content is: ", content)
  else:
    print("Error! ")
    print(response.status_code)


#  with open('response.json') as f:
#    #response = response.replace(', "\"")
#    json.dump(response, f)
#    response = json.load(f)
#    print(response)
#  #response = response.json()
#    for item in response:
#      print(item['content'])

makeOpenAIRequest()