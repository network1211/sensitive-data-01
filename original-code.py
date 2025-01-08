from flask import Flask, jsonify, request
import webutil  # Assuming this is an internal utility library
import db       # Assuming this handles database operations
import account  # Assuming this manages account-related operations
import log      # Assuming this handles logging

app = Flask(__name__)

@app.route('/api/login', methods=['POST'])
def login():
    """
    Logs the user in with email + password.
    On success, returns the user object,
    on error, returns 400 and JSON with an error field.
    """
    input = request.json or {}
    email = input.get('email')
    password = input.get('password')

    if not email or not password:
        return webutil.warn_reply("Missing input")

    u = db.get_user_by_email(email)
    if not u or not account.check_password(u.password, password):
        return webutil.warn_reply("Invalid login credentials")
    else:
        account.build_session(u, is_permanent=input.get('remember', True))

        log.info(
            "LOGIN OK agent={}".format(webutil.get_agent())
        )
        return jsonify(u), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
