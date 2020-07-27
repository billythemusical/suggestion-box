from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)
html_top = """
<html>
    <head>
        <meta http-equiv='Content-Type' content='text/html; charset=UTF-8'>
    </head>
    <body>
"""
html_bottom = """
    </body>
</html>
"""
# print(os.getcwd()+'/sms.txt')
# exit(0)
sms_file_path = os.getcwd()+'/sms.txt'
html_file_path = os.getcwd()+'/suggestions.html'

@app.route("/sms", methods=['GET', 'POST'])
def handle_sms():
    #Save the message
    new_msg = request.values.get('Body', None)
    if new_msg != None:
        with open(sms_file_path, 'a') as write_file:
            write_file.write('\n' + str(new_msg))
        # if it's their first message
        # check the database of numbers and respond
        resp = MessagingResponse()
        resp.message("Thanks for the suggestion. We'll send word on a meeting soon.")

    # Save the new message with all the others into a new html file to be displayed at a seconrdary site
    with open(sms_file_path, 'r') as read_sms_file:
        msgs_html = html_top
        for line in read_sms_file:
            msgs_html += "<div>%s</div>" % line.replace("\n", "")
        msgs_html += html_bottom
        with open(html_file_path, 'w') as output_file:
            output_file.write(msgs_html)

    if new_msg:
        return str(resp)
    else:
        return str(msgs_html)

if __name__ == "__main__":
    app.run(debug=True)
