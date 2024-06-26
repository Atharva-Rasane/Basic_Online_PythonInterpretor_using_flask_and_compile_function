# Basic_Online_PythonInterpretor_using_flask_and_compile_function

# How To Run
- Clone Repo
- Install Flask
- Run main.py

# Explanation
Creating your own online Python interpreter is not as difficult as it may seem at first, we will make a basic online python interpreter in this project. For this project, we will use Flask for the backend and HTML for the frontend.

Frontend:
The frontend will be quite simple. Our HTML page will only contain the following components: a text area for input code, a read-only text area for output, and a button to run the code. Create an index.html file in the template folder and add the following code in the body of the html page:

```
<div class="container">
    <h1>Python Online Interpreter</h1>
    <textarea class="code-input" id="code" placeholder="Enter your Python code here..."  onkeydown="handleTab(event)"></textarea>
    <textarea class="code-output" id="output" readonly></textarea>
    <button class="btn-run" onclick="runCode()">Run</button>
</div>
```

The CSS will be as follows, which can be kept in a separate CSS file or added using style tags:

```
<style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f0f0f0;
        margin: 0;
        padding: 0;
    }
    .container {
        width: 80%;
        margin: 20px auto;
        background-color: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    h1 {
        text-align: center;
    }
    .code-input,
    .code-output {
        width: 100%;
        height: 200px;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 10px;
        box-sizing: border-box;
        margin-bottom: 10px;
        font-family: monospace;
    }
    .btn-run {
        display: block;
        width: 100%;
        padding: 10px;
        margin-top: 10px;
        border: none;
        background-color: #007bff;
        color: #fff;
        cursor: pointer;
        border-radius: 5px;
        transition: background-color 0.3s ease;
    }
    .btn-run:hover {
        background-color: #0056b3;
    }
</style>
```

It's important to note that Python depends on indentation for functions, but pressing the tab in the text area will just exit us out of the text area. Thus, we need to handle the tab press, which we will do with the following function. We will keep it in the script tags for now, but it can be placed in a separate file:

function handleTab(event) {
        if (event.keyCode === 9) {
            event.preventDefault();
            var textarea = event.target;
            var start = textarea.selectionStart;
            var end = textarea.selectionEnd;
            textarea.value = textarea.value.substring(0, start) + '\t' + textarea.value.substring(end);
            textarea.selectionStart = textarea.selectionEnd = start + 1;
        }
    }
The above function inserts a '\t' character when the tab is pressed. Finally, we will write a function that will be responsible for taking the input code and outputting the executed output:

```
async function runCode() {
        var code = document.getElementById("code").value;
        var outputArea = document.getElementById("output");

        try {
            const response = await fetch('/compile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ code: code })
            });

            if (!response.ok) {
                throw new Error("Some Error Occured");
            }

            const data = await response.text();
            outputArea.value = data;
        } catch (error) {
            outputArea.value = "Error: " + error.message;
        }
    }
```

Here, we read the code and fetch the result via a post request to "/compile".

Backend:
For the backend, we will simply set up a simple Flask app:

```
from flask import Flask, render_template, request, jsonify
import sys
from io import StringIO

app = Flask(__name__)
```

We will set up two functions: one for the "/" route and the other to handle the "/compile" post request route. For the first, we will simply serve the HTML file from our templates folder:

```
@app.route('/')
def home():
    return render_template('index.html')
```

The second function, compile_code(), will be a bit more tricky. First, we will store the code from the request sent to us in a variable called code. We need to redirect the standard output to a variable instead of the console; otherwise, when we call the exec() function, the output will be printed on the console and will clutter it over time. Next, we simply compile the code using the compile() function and execute it using the exec() function. At the end, we store the output in the standard output into a variable called output and return it. Finally, we put all of this code inside a try-except block, and on exception, we send a 400 error.

```
@app.route('/compile', methods=['POST'])
def compile_code():
    try:
        code = request.json['code']

        # Redirect stdout
        stdout_redirect = sys.stdout
        sys.stdout = StringIO()

        # Compile and execute code
        compiled_code = compile(code, '<string>', 'exec')
        exec(compiled_code)

        # Get output from redirected stdout
        output = sys.stdout.getvalue()

        # Reset stdout
        sys.stdout = stdout_redirect

        return output
    except Exception as e:
        return str(e), 400
```

Finally we run the flask app.

```
if __name__ == '__main__':
    app.run()
```

