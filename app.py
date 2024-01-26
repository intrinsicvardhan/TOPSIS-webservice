from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import os
import subprocess

app = Flask(__name__)

# Flask-Mail setup
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = ''  # replace with your Gmail email
app.config['MAIL_PASSWORD'] = ''  # replace with your Gmail password
app.config['MAIL_DEFAULT_SENDER'] = '' 

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate_topsis():
    try:
        # Extract data from the form
        weights = request.form['weights']
        impacts = request.form['impacts']
        email = request.form['email']

        # Save the file temporarily
        file = request.files['file']
        input_file_path = os.path.join('temp', 'temp.csv')
        output_file_path = os.path.join('temp', 'output.csv')
        file.save(input_file_path)

        # Call the TOPSIS script
        script_path = os.path.join(os.path.dirname(__file__), 'topsis.py')
        command = f'python {script_path} {input_file_path} {weights} {impacts} {output_file_path}'
        result = subprocess.check_output(command, shell=True, text=True)

        # Send email
        with app.open_resource(output_file_path) as output_file:
            msg = Message('TOPSIS Results', recipients=[email])
            msg.body = 'Here are the TOPSIS result:\n\n'+result
            msg.attach(output_file_path,'text/csv',output_file.read())
            mail.send(msg)

        return jsonify(message='TOPSIS calculation completed. Results sent to your email.')
    except Exception as e:
        print('Error:', str(e))
        return jsonify(message='Error: {e}')

if __name__ == '__main__':
    app.run(debug=True)
