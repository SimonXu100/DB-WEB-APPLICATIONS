import CSVCatalog
import json
test = {}
test[0] = 'a'
test[1] = 'b'
del test[0]
for i in test.items():
    print(i)