<script>
    import Endpoint from "../../lib/Endpoint.svelte";
</script>

<main class="bg-slate-800 text-white text-sm sm:text-xl h-auto">
    <div class="flex">
        <div class="mx-auto w-3/4 pb-10">
            <div class="p-20 pb-10 text-3xl text-center">
                API Reference
            </div>
            <div class="my-4">
                This web interface runs on port <code class="px-1 bg-slate-900 rounded-sm">:5173</code>, however the system also provides a RESTful API on port <code class="px-1 bg-slate-900 rounded-sm">:8000</code>. Anything done in this web interface is based on this API.<br>
                The API accepts and returns <u>only</u> <code class="px-1 bg-slate-900 rounded-sm">JSON</code> encoded objects with no need for authentication. There are diferent ways to use it, one is with <code class="px-1 bg-slate-900 rounded-sm">Python</code>:
                <div class="bg-slate-900 my-3 rounded-md py-5 px-4">            
                    <pre><code>import requests
url = 'http://&lt;ip&gt;:8000/&lt;Endpoint&gt;'
headers = &lbrace;
    "Content-type": "application/json"
&rbrace;

res = requests.get(url, headers=headers)
print(res.text)     </code></pre>
                </div>
                In each of the endpoints bellow it's provided the expected return and a sample code to trigger it.
            </div>
                <hr class="my-2">
                <h2 class="italic font-bold">STATUS</h2>
                <Endpoint verb="GET" endpoint="/api" message="Returns a message if the API is up and running."
                            jsonReturn='&lbrace;
    "message": "API running."
&rbrace;'
                            code='import requests

url = "http://192.168.43.97:8000:8000/api"
headers = &lbrace;
    "Content-type": "application/json"
&rbrace;
res = requests.get(url, headers=headers)
print(res.text)'/>
                <Endpoint verb="GET" endpoint="/state" message="Returns a message with the current state which can be on of the following:"
                            jsonReturn='&lbrace;
    "message": "READY"              // Ready to start a test
    "message": "RUNNING A TEST"     // Already running a test
&rbrace;'
                            code='import requests

url = "http://192.168.43.97:8000:8000/status"
headers = &lbrace;
    "Content-type": "application/json"
&rbrace;
res = requests.get(url, headers=headers)
print(res.text)'/>

                <h2 class="italic font-bold">RUN A TEST</h2>
                <Endpoint verb="POST" endpoint="/start" message="Starts a button test, with the given parameters or profile chosen. If a valid profile is given the other parameters are ignored. A request with no body starts the test with all parameters set to zero. Returns one of the following messages: "
                            jsonReturn='&lbrace;
    "message": "Test started."              // Status code 200 OK
    "message": "A Test is already running." // Status code 304 Not Modified
    "message": "Profile not found"          // Status code 404 Not Found
    "detail": [                             // Status code 422 Unprocessable Entity
        ...
    ]
&rbrace;'
                            code='import requests

url = "http://192.168.43.97:8000:8000/status"
headers = &lbrace;
    "Content-type": "application/json"
&rbrace;
res = requests.get(url, headers=headers)
print(res.text)'/>

                <h2 class="italic font-bold">TESTS DATA</h2>
                <Endpoint verb="GET" endpoint="/get-tests" message="Returns all tests done, from oldest to newest, with format: "
                            jsonReturn='&lbrace;
    "tests": &lbrace;
        "test": [
            &lbrace;
                "id": 5,
                "button": "INFO",
                "success": 1,
                "force_val": "[[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]",
                "time_val": "[[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]",
                "date": "2024-12-30",
                "time": "11:45:43"
            &rbrace;,
            ...
        ]
    &rbrace;
&rbrace;'
                            code='import requests

url = "http://192.168.43.97:8000:8000/get-tests"
headers = &lbrace;
    "Content-type": "application/json"
&rbrace;
res = requests.get(url, headers=headers)
print(res.text)'/>
                <Endpoint verb="GET" endpoint="/get-last-test" message="Returns only the last test done: "
                            jsonReturn='&lbrace;
    "button": 7,
    "success": "INFO",
    "force_val": 1,
    "time_val": "[[1, 2, 3, 4, 5]]",
    "date": "[[1, 2, 3, 4, 5]]",
    "time": "2024-12-30"
&rbrace;'
                            code='import requests

url = "http://192.168.43.97:8000:8000/get-last-test"
headers = &lbrace;
    "Content-type": "application/json"
&rbrace;
res = requests.get(url, headers=headers)
print(res.text)'/>
                <Endpoint verb="GET" endpoint="/get-success" message="Returns the success of all tests done: "
                            jsonReturn='[
    1,
    1,
    0,
    ...
]'
                            code='import requests

url = "http://192.168.43.97:8000:8000/get-success"
headers = &lbrace;
    "Content-type": "application/json"
&rbrace;
res = requests.get(url, headers=headers)
print(res.text)'/>

                <h2 class="italic font-bold">PROFILES</h2>
                <Endpoint verb="GET" endpoint="/get-profiles" message="Returns all profiles: "
                            jsonReturn='&lbrace;
    "profiles": &lbrace;
        "profile": [
            &lbrace;
                "id": 1,
                "pName": "Custom",
                "pressTime": 0,
                "nTimes": 0,
                "interval": 0
            &rbrace;,
            ...
        ]
    &rbrace;
&rbrace;'
                            code='import requests

url = "http://192.168.43.97:8000:8000/get-profiles"
headers = &lbrace;
    "Content-type": "application/json"
&rbrace;
res = requests.get(url, headers=headers)
print(res.text)'/>
                <Endpoint verb="POST" endpoint="/add-profile" message="Add a new profile with given parameters and name. Returns one of the messages: "
                            jsonReturn='&lbrace;
    "message": "Profile added to database."                 // Status code 201 Created
    "message": "A profile with that name already exists."   // Status code 400 Bad Request
&rbrace;'
                            code='import requests

url = "http://192.168.43.97:8000:8000/add-profile"
headers = &lbrace;
    "Content-type": "application/json"
&rbrace;
res = requests.get(url, headers=headers)
print(res.text)'/>

                <Endpoint verb="DELETE" endpoint="/delete-profile" message="Deletes a profile given it's name. Returns on of the messages: "
                            jsonReturn='&lbrace;
    "message": "Profile deleted from database."     // Status code 200 OK
    "message": "Profile name not found."            // Status code 404 Not Found
&rbrace;'
                            code='import requests

url = "http://192.168.43.97:8000:8000/delete-profile"
headers = &lbrace;
    "Content-type": "application/json"
&rbrace;
res = requests.get(url, headers=headers)
print(res.text)'/>
        </div>
    </div>
</main>