import urllib.request
import json

API_KEY = "API_KEY_HERE"

def ask_health_question(question):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    data = json.dumps({
        "contents": [{"parts": [{"text": question}]}]
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode('utf-8'))
    return result['candidates'][0]['content']['parts'][0]['text']

print("Bangla Response:")
print(ask_health_question("আমার মাথাব্যাথা, কী করব?"))

print("\nEnglish Response:")
print(ask_health_question("I have fever, what should I do?"))