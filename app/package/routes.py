from flask import render_template, request
from package import package, db
from package.forms import LoginForm
from package.models.models import Relationship

from google.cloud import translate
from twilio.rest import Client

# Instantiates a client
translate_client = translate.Client()

account_sid = 'AC45cfdd30d2d97c83313d5234b0a545fd'
auth_token = '0a724904ae5059e6ab4d03fba376638e'
client = Client(account_sid, auth_token)


@package.route('/', methods=["GET", "POST"])
@package.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()


    if request.method == 'POST':
        
        if form.validate_on_submit():

            relationship = Relationship(
                    phone_number1=form.phone_number1.data,
                    phone_number2=form.phone_number2.data
                    )

            db.session.add(relationship)
            db.session.commit()

            return render_template('success.html', number=relationship.twilio_number, title='Success')
        else:
            return render_template('login.html', title='Sign In', form=form)

    return render_template('login.html', title='Sign In', form=form)



@package.route("/sms", methods=['GET', 'POST'])
def sms_reply():

    incoming_number = request.values.get('From')
    twilio = request.values.get('To')
    text = request.values.get('Body')

    relationship = Relationship.query \
        .filter(Relationship.twilio_number == twilio) \
        .first()

    person1_number = relationship.phone_number1
    person2_number = relationship.phone_number2

    if (incoming_number == person1_number):

      if relationship.person2_preset:
        target = relationship.person2_preset
       
      else:
        target = 'en'

      result = translate_client.detect_language(text)
      print (str(result['language']))
      relationship.change_presetOne(result['language'])
      outgoing_number = person2_number

    else:

      if relationship.person1_preset:
        target = relationship.person1_preset
        
      else: 
       target = 'en'

      result = translate_client.detect_language(text)
      print (str(result['language']))
      relationship.change_presetTwo(result['language'])
      outgoing_number = person1_number

    translation = translate_client.translate(text, target_language=target)

    bodyvalue = translation['translatedText']

    message = client.messages \
                .create(
                     body=bodyvalue,
                     from_=twilio,
                     to=outgoing_number
                 )

    return str(message)



