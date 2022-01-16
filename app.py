# importing needed libraries
import pyotp
import qrcode
from flask import *
from flask_bootstrap import Bootstrap

# configuring flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "APP_SECRET_KEY"
# my_secret = pyotp.random_base32()
my_secret = 'OMAS2M6FKQUTN62P3D5VTUAKNYK5BFQH'
my_hex_secret = pyotp.random_hex()
print(my_secret)
print(my_hex_secret)
Bootstrap(app)


# homepage route
@app.route("/")
def index():
    return "<h1>Hello World!</h1>"

# login page route
@app.route("/login/")
def login():
    return render_template("login.html")

# application access route
@app.route("/login/application_access")
def login_application_access():
    return render_template("application_access.html")

# failed access route
@app.route("/login/failed_access")
def login_failed_access():
    return render_template("failed_access.html")


# 2FA page route
@app.route("/login/2fa/")
def login_2fa():
    # generating random secret key for authentication
    '''img = qrcode.make(my_secret)
    type(img)  # qrcode.image.pil.PilImage
    img.save("some_file.png") '''
    uri = pyotp.totp.TOTP(my_secret).provisioning_uri('suchintya.paul@gmail.com',issuer_name="SecureApp")
    qrcode_uri = "https://www.google.com/chart?chs=200x200&chld=M|0&cht=qr&chl={}".format(uri)
    print(qrcode_uri)
    return render_template("login_2fa.html", secret=my_secret, qr_code = qrcode_uri)

# login form route
@app.route("/login/", methods=["POST"])
def login_form():

    # demo creds
    creds = {"username": "test", "password": "password"}

    # getting form data
    username = request.form.get("username")
    password = request.form.get("password")

    # authenticating submitted creds with demo creds
    if username == creds["username"] and password == creds["password"]:
        # inform users if creds are valid
        flash("The credentials provided are valid", "success")
        return redirect(url_for("login_2fa"))
    else:
        # inform users if creds are invalid
        flash("You have supplied invalid login credentials!", "danger")
        return redirect(url_for("login"))


@app.route("/login/2fa/", methods=["POST"])
def login_2fa_form():
    # getting secret key used by user
    secret = request.form.get("secret")
    # getting OTP provided by user
    otp = int(request.form.get("otp"))

    # verifying submitted OTP with PyOTP
    if pyotp.TOTP(secret).verify(otp):
        # inform users if OTP is valid
        flash("The TOTP 2FA token is valid", "success")
        return redirect(url_for("login_application_access"))
    else:
        # inform users if OTP is invalid
        flash("You have supplied an invalid 2FA token!", "danger")
        return redirect(url_for("login_failed_access"))

# get a new base32 code

@app.route('/api/v1/newBase32Code', methods=['GET'])
def api_newbase32code():
    #returns "A new base32 coded string "
    base32code = pyotp.random_base32()
    print(type(base32code))
    return base32code


# get a new base32 QR code for an email id

@app.route('/api/v1/newBase32CodeForEmail', methods=['POST'])
def api_newbase32codeforemail():
    #returns "A new base32 coded string which will be associated with every external user passed through the request param"
    input_json = request.get_json(force=True) 
    email_id_for_code = input_json['email']
    base32code = pyotp.random_base32()
    uri = pyotp.totp.TOTP(base32code).provisioning_uri(email_id_for_code,issuer_name="MRO")
    qrcode_uri = "https://www.google.com/chart?chs=200x200&chld=M|0&cht=qr&chl={}".format(uri)
    print(qrcode_uri)
    return qrcode_uri


@app.route('/api/v1/validateToken', methods=['POST'])
def api_validate_token():
    input_json = request.get_json(force=True) 
    base32codepassed = input_json['code']
    tokenpassed = input_json['token']
    # verifying submitted OTP with PyOTP
    if pyotp.TOTP(base32codepassed).verify(tokenpassed):
        # inform users if OTP is valid
        print("The TOTP 2FA token is valid", "success")
        return "Valid"
    else:
        # inform users if OTP is invalid
        print("You have supplied an invalid 2FA token!", "danger")
        return "InValid"
   
    
    return base32codepassed + '....' + tokenpassed
    



# running flask server
if __name__ == "__main__":
    app.run(debug=True)