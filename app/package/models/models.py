from package import db
from twilio.rest import Client
import requests

class Relationship(db.Model):
    __tablename__ = "relationships"

    id = db.Column(db.Integer, primary_key=True)
    phone_number1 = db.Column(db.String, nullable=False)
    phone_number2 = db.Column(db.String, nullable=False)
    twilio_number = db.Column(db.String, nullable=True)
    person1_preset = db.Column(db.String, nullable=True)
    person2_preset = db.Column(db.String, nullable=True)

    def __init__(self, phone_number1, phone_number2):
        self.phone_number1 = '+1' + phone_number1
        self.phone_number2 = '+1' + phone_number2
        self.buy_number()    

    def buy_number(self):

        account_sid = "AC45cfdd30d2d97c83313d5234b0a545fd"
        auth_token = "0a724904ae5059e6ab4d03fba376638e"
        client = Client(account_sid, auth_token)

        numbers = client.available_phone_numbers("US") \
                        .local \
                        .list()

        # Purchase the phone number

        number = client.incoming_phone_numbers \
                       .create(phone_number=numbers[0].phone_number)

        address = 'https://api.twilio.com' + number.uri

        data = {
            'SmsUrl': 'http://9237c256.ngrok.io/sms',
        }

        #create webhook

        response = requests.post(address, data=data, auth=(account_sid, auth_token))

        self.twilio_number = number.phone_number

    def change_presetOne(self, str):
        self.person1_preset = str
        db.session.commit()

    def change_presetTwo(self, str):
        self.person2_preset = str
        db.session.commit()

    def _get_twilio_client(self):
        account_sid = 'AC45cfdd30d2d97c83313d5234b0a545fd'
        auth_token = '0a724904ae5059e6ab4d03fba376638e'
        return Client(account_sid, auth_token)