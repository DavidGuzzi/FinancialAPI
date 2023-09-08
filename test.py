import requests

print('Search by id:')
print(requests.get('http://127.0.0.1:8000/transactions/2').json())
print()

print("Adding an item:")
print(
    requests.post(
        'http://127.0.0.1:8000',
        json={'id' : 4, 'date' : '2023-09-07', 'instrument' : 'commercial_paper', 'amount' : 100000, 'maturity' : 120, 'rate' : 110, 'drawer' : 'Firm 1'},
    ).json()
)
print(requests.get('http://127.0.0.1:8000').json())
print()

print("Updating an item:")
print(requests.put('http://127.0.0.1:8000/transactions/2?rate=77').json())
print(requests.get('http://127.0.0.1:8000').json())
print()

print("Deleting an item:")
print(requests.delete('http://127.0.0.1:8000/transactions/1').json())
print(requests.get('http://127.0.0.1:8000').json())