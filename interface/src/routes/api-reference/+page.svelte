<script>
    import Endpoint from "../../lib/Endpoint.svelte";
</script>

<main class="bg-slate-800 text-white text-sm sm:text-xl h-auto">
    <div class="flex">
        <div class="sm:mx-auto w-full sm:w-3/4 pb-10">
            <div class="p-20 pb-10 text-3xl text-center">
                API Reference
            </div>
            <div class="my-4">
                This web interface runs on port <code class="px-1 bg-slate-900 rounded-sm">:3000</code>, however the system also provides a RESTful API on port <code class="px-1 bg-slate-900 rounded-sm">:8000</code>. Anything done in this web interface is based on this API.<br>
                The API accepts and returns <u>only</u> <code class="px-1 bg-slate-900 rounded-sm">JSON</code> encoded objects with no need for authentication. There are diferent ways to use it, one is with <code class="px-1 bg-slate-900 rounded-sm">Python</code>:
                <div class="bg-slate-900 my-3 rounded-md py-5 px-4">            
                    <pre><code>import requests
url = 'http://&lt;ip&gt;:8000/&lt;Endpoint&gt;'
headers = &lbrace;
    "Content-type": "application/json"
&rbrace;

res = requests.get(url, headers=headers)
print(res.text)</code></pre>
                </div>
                In each of the endpoints bellow it's provided the expected returns and a sample code to use it. <br>
                All code can be seen on the <a href="https://github.com/goncaloperalta/Projeto-Industrial" class="font-bold">GitHub</a> repository.
            </div>
                <hr class="my-2">
<!--                        STATUS                        -->
                <h2 class="italic font-bold">STATUS</h2>
                <Endpoint verb="GET" endpoint="/api" message="Returns a message if the API is up and running."
                            jsonReturn='&lbrace;
    "message": "API running."
&rbrace;'
                            code='import requests

url = "http://localhost:8000/api"
headers = &lbrace;
    "Content-type": "application/json"
&rbrace;
res = requests.get(url, headers=headers)
print(res.text)'/>
                <Endpoint verb="GET" endpoint="/get-status" message="Returns a message with the current state which can be on of the following:"
                            jsonReturn='&lbrace;
    // Ready to start a test
    "message": "Ready"
    // Already running a test
    "message": "Running a test"
    // Aborting the running test
    "message": "Aborting the test"
&rbrace;'
                            code='import requests

url = "http://localhost:8000/get-status"
headers = &lbrace;
    "Content-type": "application/json"
&rbrace;
res = requests.get(url, headers=headers)
print(res.text)'/>
                <Endpoint verb="GET" endpoint="/get-current-parameters" message="If a test is running, returns an object with the parameters being used:"
                            jsonReturn='&lbrace;    // If a test is running
    "pressTime": 0
    "pressTime": 1
    "pressTime": 0     
&rbrace;           
&lbrace;    // If no test is running
    "message": "Not running a test"  
&rbrace;'
                            code='import requests

url = "http://localhost:8000/get-current-parameters"
headers = &lbrace;
    "Content-type": "application/json"
&rbrace;
res = requests.get(url, headers=headers)
print(res.text)'/>
                <Endpoint verb="GET" endpoint="/get-logs" message="Returns a file with the logs of the last test done. Can be accessed by just opening on the browser."
                            jsonReturn=''
                            code=''/>



<!--                        RUN A TEST                        -->
                <h2 class="italic font-bold">RUN A TEST</h2>
                <Endpoint verb="POST" endpoint="/start" message="Starts a button test, with the given parameters or profile chosen. If a valid profile is given the other parameters are ignored. A request with no body starts the test with parameter nTimes equal to one an the others set to zero. Returns one of the following messages: "
                            jsonReturn='&lbrace;
    // Status code 200 OK
    "message": "Test started."
    // Status code 304 Not Modified
    "message": "A Test is already running."
    // Status code 404 Not Found
    "message": "Profile not found"
    // Status code 422 Unprocessable Entity
    "detail": [
        ...
    ]
&rbrace;'
                            code='import requests
url = "http://localhost:8000/start"
headers = &lbrace;
    "Content-type": "application/json"
&rbrace;
body = &lbrace;
    "pName": "Example"
    // Or define the parameters
    // "pressTime": 0
    // "nTimes": 1
    // "interval": 0
&rbrace;

res = requests.post(url, headers=headers, json=body)
print(res.text)'/>
                <Endpoint verb="GET" endpoint="/abort-test" message="If a test is running aborts it. The test will only abort after finishing the current actuation "
                            jsonReturn='&lbrace;
    "message": "No test to abort"
    "message": "Test Aborted"
&rbrace;'
                            code='import requests

url = "http://localhost:8000/abort-test"
headers = &lbrace;
    "Content-type": "application/json"
&rbrace;
res = requests.get(url, headers=headers)
print(res.text)'/>



<!--                        TESTS DATA                        -->
                <h2 class="italic font-bold">TESTS DATA</h2>
                <Endpoint verb="GET" endpoint="/get-test-data" message="Returns a file a JSON file with the all tests done from newest to oldest. Using a browser you can open the link directly and a download should appear. Data has the format: "
                            jsonReturn='[
    &lbrace;
        "id": 5,
        "button": "WPS",
        "success": 1,
        "error": "No error",
        "presses": 2,
        "parameters": "[0, 2, 1]",
        "force_val": "[[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]",
        "time_val": "[[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]",
        "date": "2024-12-30",
        "time": "11:45:43"
    &rbrace;,
    ...
]'
                            code=''/>
                <Endpoint verb="GET" endpoint="/get-tests" message="Returns all tests done, from newest to oldest, with format: "
                            jsonReturn='&lbrace;
    "tests": &lbrace;
        "test": [
            &lbrace;
                "id": 5,
                "button": "WPS",
                "success": 1,
                "error": "No error",
                "presses": 2,
                "parameters": "[0, 2, 1]",
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

url = "http://localhost:8000/get-tests"
headers = &lbrace;
    "Content-type": "application/json"
&rbrace;
res = requests.get(url, headers=headers)
print(res.text)'/>
                <Endpoint verb="GET" endpoint="/get-last-test" message="Returns only the last test done: "
                            jsonReturn='&lbrace;
    "id": 5,
    "button": "WPS",
    "success": 1,
    "error": "No error",
    "presses": 2,
    "parameters": [0, 2, 1],
    "force_val": "[[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]",
    "time_val": "[[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]",
    "date": "2024-12-30",
    "time": "11:45:43"
&rbrace;'
                            code='import requests

url = "http://localhost:8000/get-last-test"
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

url = "http://localhost:8000/get-success"
headers = &lbrace;
    "Content-type": "application/json"
&rbrace;
res = requests.get(url, headers=headers)
print(res.text)'/>
                <Endpoint verb="POST" endpoint="/get-tests-range" message="Returns a defined range of tests: "
                            jsonReturn='&lbrace;
    "tests": &lbrace;
        "test": [
            &lbrace;
                "id": 5,
                "button": "WPS",
                "success": 1,
                "error": "No error",
                "presses": 2,
                "parameters": "[0, 2, 1]",
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

url = "http://localhost:8000/get-tests-range"
headers = &lbrace;
    "Content-type": "application/json"
&rbrace;
body = &lbrace;
    "size": 2,
    "offset": 3
&rbrace;

res = requests.post(url, headers=headers, json=body)
print(res.text)'/>
                <Endpoint verb="GET" endpoint="/get-count" message="Returns the total number of tests done: "
                            jsonReturn='&lbrace;
    "count": 19
&rbrace;'
                            code='import requests

url = "http://localhost:8000/get-count"
headers = &lbrace;
    "Content-type": "application/json"
&rbrace;
res = requests.get(url, headers=headers)
print(res.text)'/>
                <Endpoint verb="POST" endpoint="/get-by-id" message="Returns the test data with the same id: "
                            jsonReturn='&lbrace;
    "id": 5,
    "button": "WPS",
    "success": 1,
    "error": "No error",
    "presses": 2,
    "parameters": "[0, 2, 1]",
    "force_val": "[[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]",
    "time_val": "[[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]",
    "date": "2024-12-30",
    "time": "11:45:43"
&rbrace;'
                            code='import requests

url = "http://localhost:8000/get-by-id"
headers = &lbrace;
    "Content-type": "application/json"
&rbrace;
body = &lbrace;
    "id": 5
&rbrace;
res = requests.post(url, headers=headers, json=body)
print(res.text)'/>
                <Endpoint verb="DELETE" endpoint="/delete-tests-before-date" message="Deletes all tests before the given date: "
                            jsonReturn='&lbrace;
    "message": "Tests deleted"
&rbrace;'
                            code='import requests

url = "http://localhost:8000/delete-tests-before-date"
headers = &lbrace;
    "Content-type": "application/json"
&rbrace;
body = &lbrace;
    "day": "2024-12-30"
&rbrace;
res = requests.delete(url, headers=headers, json=body)
print(res.text)'/>


<!--                        PROFILES                        -->
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

url = "http://localhost:8000/get-profiles"
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

url = "http://localhost:8000/add-profile"
headers = &lbrace;
    "Content-type": "application/json"
&rbrace;
body = &lbrace;
    "pName": "Test Profile",
    "pressTime": 3,
    "nTimes": 2,
    "interval": 1
&rbrace;

res = requests.post(url, headers=headers, json=body)
print(res.text)'/>

                <Endpoint verb="DELETE" endpoint="/delete-profile" message="Deletes a profile given it's name. Returns on of the messages: "
                            jsonReturn='&lbrace;
    "message": "Profile deleted from database."     // Status code 200 OK
    "message": "Profile name not found."            // Status code 404 Not Found
&rbrace;'
                            code='import requests

url = "http://localhost:8000/delete-profile"
headers = &lbrace;
    "Content-type": "application/json"
&rbrace;
body = &lbrace;
    "pName": "Test Profile"
&rbrace;

res = requests.delete(url, headers=headers, json=body)
print(res.text)'/>
        </div>
    </div>
</main>