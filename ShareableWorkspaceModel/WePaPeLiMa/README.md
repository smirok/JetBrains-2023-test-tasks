# Description

* OpenAPI definition is available on `http://localhost:8080/swagger-ui/index.html` after starting application

## API

1) Get the available versions \
   Request: `GET /lists` \
   Response: `{ "versions": [1,2,3,4] }`
2) Get the list elements \
   Request: `GET /list/{id}` \
   Response: `[2,3,4,6,0]`
3) Add a new element to the end of the last list (because by [the definition of partially persistent structures](https://en.wikipedia.org/wiki/Persistent_data_structure#:~:text=A%20data%20structure%20is%20partially,be%20both%20accessed%20and%20modified.) only the newest version can be modified) \
   Request: `POST /list` \
   Request body: `{ "newElement": 22 }` \
   Response: `{ "listVersion": 5 }`
4) Remove an element by value \
   Request: `DELETE /list` \
   Request body: `{ "oldElement": 10 }` \
   Response: `{ "listVersion": 7 }`
5) Update an element’s value \
   Request: `PUT /list` \
   Request body: `{ "oldValue": 10, "newValue": 12 }` \
   Response: `{ "listVersion": 8 }`
