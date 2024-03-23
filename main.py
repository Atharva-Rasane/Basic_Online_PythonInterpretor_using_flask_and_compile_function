from flask import Flask, render_template, request, jsonify
import sys
from io import StringIO

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

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


# main driver function
if __name__ == '__main__':
    app.run()