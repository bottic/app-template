import requests



resp = requests.get('http://127.0.0.1:8000/example/whoami?token=pHejaIPJGodgFzUAKVKgVWhwmURKcyfVHIpCaLGbAkZNOrHxKNSLscWjWQQKxCzD&scopes=&user_id=161')
print(resp.json())