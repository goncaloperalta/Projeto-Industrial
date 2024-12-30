<script>
   
</script>

<main class="dark:bg-slate-700 text-white h-screen text-xl">
    <div>

    </div>
    <div class=" flex ">
        <div class=" mt-32 mb-20 mx-10">
            <strong class=" text-2xl">Table of contents</strong>
        </div>

        <div class="h-screen border border-black"></div>

        <div class="ml-20 mt-14 w-3/4">
            <strong class=" text-3xl ">API Reference</strong>

            <div>
                Our system provides a RESTful API on port <code class="px-1 bg-slate-800 rounded-sm">:8000</code>. <br>
                The API accepts and returns only <code class="px-1 bg-slate-800 rounded-sm">JSON</code> encoded objects with no need for authentication. <br>
                There are diferent ways to use the API, one is with <code class="px-1 bg-slate-800 rounded-sm">Python</code>:
                <div class="bg-slate-800 my-3 rounded-md py-5 px-4">            
<pre><code>import requests
url = 'http://&lt;ip&gt;:8000/&lt;Endpoint&gt;'
headers = &lbrace;
    "content-type": "application/json"
&rbrace;

res = requests.get(url, headers=headers)
print(res.text)
</code></pre>
                                    </div>
            </div>
            
            <hr>

            <div class="bg-slate-500 flex h-12 rounded-sm my-3">
                <div class=" py-2 px-7 bg-green-500 rounded-sm">GET</div>
                <div class=" py-2 px-7"><code class="px-1 bg-gray-700 rounded-sm">/api</code></div>
                <div class="my-auto ml-auto pr-5">&#11167</div>
            </div>
            <div class="px-4">
                Returns a message if the API is up and running.
                <div class="bg-slate-800 my-3 rounded-md py-5 px-4">            
<pre><code>&lbrace;
    "message": "API running."
&rbrace;</code></pre>
                </div>
                Sample <code class="px-1 bg-slate-800 rounded-sm">python</code> code:
                <div class="bg-slate-800 my-3 rounded-md py-5 px-4">
<pre><code>import requests

res = requests.get('http://&lt;ip&gt;:8000:/api')
print(res.text)
</code></pre>
                </div>
            </div>
        </div>
    </div>
</main>