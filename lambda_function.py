"""
This sample demonstrates an implementation of the Lex Code Hook Interface
in order to serve a sample bot which manages orders for flowers.
Bot, Intent, and Slot models which are compatible with this sample can be found in the Lex Console
as part of the 'OrderFlowers' template.

For instructions on how to set up and test this bot, as well as additional samples,
visit the Lex Getting Started documentation http://docs.aws.amazon.com/lex/latest/dg/getting-started.html.
"""
import math
import dateutil.parser
import datetime
import time
import os
import logging
import pymysql

db=pymysql.connect(host="gpa.cxu0mytwya5e.us-east-1.rds.amazonaws.com",
                                user="gpa",
                                passwd="*******",                     #Password of your sql database
                                db="gpadb")
cursor=db.cursor()


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


""" --- Helpers to build responses which match the structure of the necessary dialog actions --- """


def get_slots(intent_request):
    return intent_request['currentIntent']['slots']


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message, response_card=None):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message,
            'responseCard': response_card
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


""" --- Helper Functions --- """


def parse_int(n):
    try:
        return int(n)
    except ValueError:
        return float('nan')


def build_validation_result(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot,
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }


def response_card(title, subtitle, url, options):
    buttons = []
    for key,value in options.items():
        button1 = {"text": key, "value": value}
        buttons.append(button1)

    return {
        'contentType': 'application/vnd.amazonaws.card.generic',
        'version': 1,
        'genericAttachments': [{
            'title': title,
            'subTitle': subtitle,
            'imageUrl': url,
            'buttons': buttons
        }]
    }
	
	

def isvalid_date(date):
    try:
        dateutil.parser.parse(date)
        return True
    except ValueError:
        return False


'''def validate_order_flowers(flower_type, date, pickup_time):
    flower_types = ['lilies', 'roses', 'tulips']
    if flower_type is not None and flower_type.lower() not in flower_types:
        return build_validation_result(False,
                                       'FlowerType',
                                       'We do not have {}, would you like a different type of flower?  '
                                       'Our most popular flowers are roses'.format(flower_type))

    if date is not None:
        if not isvalid_date(date):
            return build_validation_result(False, 'PickupDate', 'I did not understand that, what date would you like to pick the flowers up?')
        elif datetime.datetime.strptime(date, '%Y-%m-%d').date() <= datetime.date.today():
            return build_validation_result(False, 'PickupDate', 'You can pick up the flowers from tomorrow onwards.  What day would you like to pick them up?')

    if pickup_time is not None:
        if len(pickup_time) != 5:
            # Not a valid time; use a prompt defined on the build-time model.
            return build_validation_result(False, 'PickupTime', None)

        hour, minute = pickup_time.split(':')
        hour = parse_int(hour)
        minute = parse_int(minute)
        if math.isnan(hour) or math.isnan(minute):
            # Not a valid time; use a prompt defined on the build-time model.
            return build_validation_result(False, 'PickupTime', None)

        if hour < 10 or hour > 16:
            # Outside of business hours
            return build_validation_result(False, 'PickupTime', 'Our business hours are from ten a m. to five p m. Can you specify a time during this range?')

    return build_validation_result(True, None, None)
'''

""" --- Functions that control the bot's behavior --- """


def claim_management(intent_request):
    """
    Performs dialog management and fulfillment for raising the claim.
    Beyond fulfillment, the implementation of this intent demonstrates the use of the elicitSlot dialog action
    in slot validation and re-prompting.
    """
    
    greeting= get_slots(intent_request)["GreetingSlot"]
    names= get_slots(intent_request)["NameSlot"]
    work= get_slots(intent_request)["ActionTypeSlot"]
    policy= get_slots(intent_request)["PolicyNumberSlot"]
    mobile= get_slots(intent_request)["MobileSlot"]
    test= get_slots(intent_request)["TestSlot"]
    confirm= get_slots(intent_request)["ConfirmationSlot"]
    incident= get_slots(intent_request)["Incident_Severity_Slot"]
    propertydamage= get_slots(intent_request)["PropertyDamageSlot"]
    witness= get_slots(intent_request)["WitnessSlot"]
    witnessno= get_slots(intent_request)["WitnessNo"]
    policereport= get_slots(intent_request)["PoliceReportSlot"]
    claimamount= get_slots(intent_request)["ClaimAmountSlot"]
    vehicleinvolved= get_slots(intent_request)["VehicleInvolvedSlot"]
    incidentdate= get_slots(intent_request)["IncidentDateSlot"]
    incidenttime= get_slots(intent_request)["IncidentTimeSlot"]
    incidentlocation= get_slots(intent_request)["IncidentLocationSlot"]
    months= get_slots(intent_request)["MonthsAsCustomerSlot"]
    raiseto= get_slots(intent_request)["RaiseConfirmSlot"]
    empid= get_slots(intent_request)["EmpIdSlot"]
    fraudno= get_slots(intent_request)["FraudNoSlot"]


    
    source = intent_request['invocationSource']
    
    
    if source == 'DialogCodeHook':
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt for the first violation detected.
        slots = get_slots(intent_request)
        
        if names is None:
            message = {'contentType': 'PlainText', 'content': 'Hi, I am dora and I am here to assist you on queries and services related to policy. What is your name?'}
            return elicit_slot(intent_request['sessionAttributes'],
                              intent_request['currentIntent']['name'],
                              slots,
                              'NameSlot',
                              message)
     
      
        if greeting is None:
            message = {'contentType': 'PlainText', 'content': 'Welcome '+names+'!! How are you today?'}
            return elicit_slot(intent_request['sessionAttributes'],
                              intent_request['currentIntent']['name'],
                              slots,
                              'GreetingSlot',
                              message)
        if work is None:              
            message = {'contentType': 'PlainText', 'content': "Don't Worry, We are here to help you!! How can I assist you? Please visit these links.."}
            res = response_card('Specify Action', 'What you wish to do?','http://www.vasilevconsult.bg/upimages/31-Insurance.jpg', {'Raise a Claim':"Raise", 'Check Status':"Check",'Fraud Detection':'Fraud'})
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               'ActionTypeSlot',
                               message,
                               res
                               )
        if policy is None and work == 'Raise':
            message = {'contentType': 'PlainText', 'content': "To raise the Claim, Kindly Enter your Policy number in the format XX-XX-XXXX? In case you do not remember, type No."}
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               'PolicyNumberSlot',
                               message
                               )
                               
                               
        if  work=='Raise' and confirm is None and policy!="No":
            print(policy)
            cursor.execute("SELECT Insured_Name from Tr_Gargi_Policy where Policy_Number='"+policy+"'")
            rows = cursor.fetchall()
            print(rows)
            if rows!=():
                x=''.join(rows[0])
                message = {'contentType': 'PlainText', 'content':  'Hello '+x+'!! We found you as a registered Policy holder. Kindly Press the button to fill the Claim Application Form'}
                res = response_card('Specify Action', 'Click on your choice?','https://static.careers360.mobi/media/presets/860X430/article_images/2019/1/2/ATMA-Application-Form.jpg', {'Start':'Yes', 'Later':'No'})
                return elicit_slot(intent_request['sessionAttributes'],
                                           intent_request['currentIntent']['name'],
                                           slots,
                                           'ConfirmationSlot',
                                           message,
                                           res
                                           )
            elif rows == ():
                return close(intent_request['sessionAttributes'],
                'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Sorry , You are not a registered Policy Holder. Thanks for using the application.'})
                  
        if work=='Raise' and policy=="No" and mobile is None:
                print("djfdjf")
                message = {'contentType': 'PlainText', 'content': 'Please mention your Mobile number? '}
                return elicit_slot(intent_request['sessionAttributes'],
                             intent_request['currentIntent']['name'],
                                    slots,
                                    'MobileSlot',
                                    message)                       
        if work=='Raise' and mobile is not None and confirm is None:
            cursor.execute("SELECT Insured_Name from Tr_Gargi_Policy where Mobile_No='"+mobile+"'")
            rows = cursor.fetchall()
            
            if rows!=():
                x=''.join(rows[0])
                message = {'contentType': 'PlainText', 'content':  'Hello '+x+'!! We found you as a registered Policy holder. Kindly Press the button to fill the Claim Application Form'}
                res = response_card('Specify Action', 'Click on your choice?','https://static.careers360.mobi/media/presets/860X430/article_images/2019/1/2/ATMA-Application-Form.jpg', {'Start':'Yes', 'Later':'No'})
                return elicit_slot(intent_request['sessionAttributes'],
                                           intent_request['currentIntent']['name'],
                                           slots,
                                           'ConfirmationSlot',
                                           message,
                                           res
                                           )
            elif rows==():
                return close(intent_request['sessionAttributes'],
                'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Sorry , you are not a registered policy holder with given mobile number. Thanks for using the application.'})

        if work=='Raise' and incident is None and confirm=="No":
            return close(intent_request['sessionAttributes'],
                'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Thanks for using the application.Have a Nice Day!!'})

                  
                                       
        if work=='Raise' and incident is None and confirm=="Yes":
            
            message = {'contentType': 'PlainText', 'content': "How Severe the Incident was?"}
            res = response_card('Specify Action', 'Enter your choice?','https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Head_On_Collision.jpg/300px-Head_On_Collision.jpg', {'Major Damage':'Major Damage', 'Minor Damage':'Minor Damage','Total Damage':"Total Damage"})
            return elicit_slot(intent_request['sessionAttributes'],
                              intent_request['currentIntent']['name'],
                              slots,
                              'Incident_Severity_Slot',
                              message,
                              res
                              )
            
                              
        if work=='Raise' and propertydamage is None:
            message = {'contentType': 'PlainText', 'content': "Is there any property damage?"}
            res = response_card('Specify Action', 'Enter your choice?','https://media.gettyimages.com/photos/insurance-claim-form-and-insurance-policy-picture-id183427329',  {'Yes':'Yes', 'No':'No'})
            return elicit_slot(intent_request['sessionAttributes'],
                              intent_request['currentIntent']['name'],
                              slots,
                              'PropertyDamageSlot',
                              message,
                              res
                              )        
        if work=='Raise' and witness is None:
            message = {'contentType': 'PlainText', 'content': "Is there any witness of the Accident?"}
            res = response_card('Specify Action', 'Enter your choice?','https://ctpisolutions.com/wp-content/uploads/2017/02/car-accident-1080x675.jpg', {'Yes':'Yes', 'No':'No'})
            return elicit_slot(intent_request['sessionAttributes'],
                              intent_request['currentIntent']['name'],
                              slots,
                              'WitnessSlot',
                              message,
                              res
                              )      
        if work=='Raise' and witness == "Yes" and witnessno is None:
            message = {'contentType': 'PlainText', 'content': "Enter the number of witness present"}
            return elicit_slot(intent_request['sessionAttributes'],
                                       intent_request['currentIntent']['name'],
                                       slots,
                                       'WitnessNo',
                                       message
                                       )
        if work=='Raise' and witness == "No" and witnessno is None:
            witnessno = 0
            
        
            
        if work=='Raise' and policereport is None:
            message = {'contentType': 'PlainText', 'content': "Have you filled any Police report?"}
            res = response_card('Specify Action', 'Enter your choice?','https://image.shutterstock.com/image-vector/hand-holding-clipboard-completed-form-260nw-493482403.jpg', {'Yes':'Yes', 'No':'No'})
            return elicit_slot(intent_request['sessionAttributes'],
                              intent_request['currentIntent']['name'],
                              slots,
                              'PoliceReportSlot',
                              message,
                              res
                              )       
                               
        if work=='Raise' and vehicleinvolved is None:
                message = {'contentType': 'PlainText', 'content': 'Enter the Number of vehicles involved in the Accident.'}
                return elicit_slot(intent_request['sessionAttributes'],
                             intent_request['currentIntent']['name'],
                                    slots,
                                    'VehicleInvolvedSlot',
                                    message)    
        
        if work=='Raise' and incidentdate is None:
                message = {'contentType': 'PlainText', 'content': 'Enter the date of the incident? '}
                return elicit_slot(intent_request['sessionAttributes'],
                             intent_request['currentIntent']['name'],
                                    slots,
                                    'IncidentDateSlot',
                                    message)
        if work=='Raise' and incidenttime is None:
                message = {'contentType': 'PlainText', 'content': 'Enter the time on which incident take place? '}
                return elicit_slot(intent_request['sessionAttributes'],
                             intent_request['currentIntent']['name'],
                                    slots,
                                    'IncidentTimeSlot',
                                    message)
                                    
        if work=='Raise' and incidentlocation is None:
                message = {'contentType': 'PlainText', 'content': 'Enter the place of Incident. '}
                return elicit_slot(intent_request['sessionAttributes'],
                             intent_request['currentIntent']['name'],
                                    slots,
                                    'IncidentLocationSlot',
                                    message)
        
        if work=='Raise' and months is None:
                message = {'contentType': 'PlainText', 'content': 'Enter the number of months you are associated with us. '}
                return elicit_slot(intent_request['sessionAttributes'],
                             intent_request['currentIntent']['name'],
                                    slots,
                                    'MonthsAsCustomerSlot',
                                    message)
        
        if work=='Raise' and claimamount is None:
                message = {'contentType': 'PlainText', 'content': 'Enter the amount you want to claim in Dollars. '}
                return elicit_slot(intent_request['sessionAttributes'],
                             intent_request['currentIntent']['name'],
                                    slots,
                                    'ClaimAmountSlot',
                                    message)
                                    
                                    
        if work=='Raise' and raiseto is None:
            if policy=="0":
                cursor.execute("Select Policy_Number from Tr_Gargi_Policy where Mobile_No='"+mobile+"'")
                rows = cursor.fetchall()
                policy=''.join(rows[0])
            report='N'
            cursor.execute("Insert into Tr_Gargi_Claim(Policy_Number,Incident_Severity,Property_Damage,Witnesses,Police_Report_Available,Total_Claim_Amount,Number_Of_Vehicles_Involved,Months_As_Customer,Incident_Date,Incident_Hour_of_the_Day,Incident_Location,Fraud_Reported)values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(policy,incident,propertydamage,witnessno,policereport,claimamount,vehicleinvolved,months,incidentdate,incidenttime,incidentlocation,report))
            print("done")
            db.commit()
            return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Do not Panic!! Your Claim Application form has been successfully submitted.Feel Free to check the status of your claim.Thank You for using the Application and believing in us.Regards:Dora' })

                                    
        
      
        if  work == 'Check' and policy is None:
            message = {'contentType': 'PlainText', 'content': "To Check your Claim Status,Kindly Enter your Policy number in the format XX-XX-XXXX? If you do not remember ,type No "}
            #res = response_card('Specify Action', 'Enter your choice?','https://injurymaster.zendesk.com/hc/en-us/article_attachments/202682928/2015-08-06_11-07-28.png', {'Yes':'Yes', 'No':'No'})
            return elicit_slot(intent_request['sessionAttributes'],
                              intent_request['currentIntent']['name'],
                              slots,
                              'PolicyNumberSlot',
                              message
                              )
        
        if work == 'Check' and policy!="No" and policy is not None:
            print(policy)
            cursor.execute("SELECT Total_Claim_Amount from Tr_Gargi_Claim where Policy_Number='"+policy+"'")
            rows = cursor.fetchall()
            print(rows)
            if rows!=():
                x=''.join(str(rows[0]))
                print(x)
                #message = {'contentType': 'PlainText', 'content':  'Your Total Claim is'+x+'.The average waiting time to get your claim approved is 21 days'}
                return close(intent_request['sessionAttributes'],
                'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Our ML Model has predicted an average processing time of 20 days for your Claim of amount $'+x+'. The stated time is our best prediction but is not a guarantee.Thank you for using the application'})
                

            elif rows == ():
                return close(intent_request['sessionAttributes'],
                'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Sorry , There is no claim associated with the given policy number. Thanks for using the application.'})
           





        if work == 'Check' and policy=="No":
            return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': ' Sorry, but we need your policy number to ensure.Regards:Dora' })

        
                
        if  work == 'Fraud' and empid is None:
            message = {'contentType': 'PlainText', 'content': 'Please Enter your Credientials '}
            return elicit_slot(intent_request['sessionAttributes'],
                             intent_request['currentIntent']['name'],
                                    slots,
                                    'EmpIdSlot',
                                    message)

        if work=='Fraud' and empid is not None and fraudno is None:
            cursor.execute("SELECT Adjuster_Name from Tr_Gargi_Emp where id='"+empid+"'")
            rows = cursor.fetchall()
            print(rows)
            if rows!=():
                x=''.join(rows[0])
                print(x)
                message = {'contentType': 'PlainText', 'content': "Hello "+x+ " , Given are the Pending Claim Requests, have a look!!"}
                res = response_card('Specify Action', 'Enter your choice?','https://image.shutterstock.com/image-vector/hand-holding-clipboard-completed-form-260nw-493482403.jpg', {'17-709-4353':'17-709-4353', '72-022-2462':'72-022-2462','65-266-8217':'65-266-8217'})
                return elicit_slot(intent_request['sessionAttributes'],
                              intent_request['currentIntent']['name'],
                              slots,
                              'FraudNoSlot',
                              message,
                              res
                              )
            elif rows == ():
                return close(intent_request['sessionAttributes'],
                'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Sorry , You are not a registered Claim Adjuster. Thanks for using the application.'})
           
        if work=='Fraud' and fraudno is not None:

            cursor.execute("SELECT Fraud_Reported from Tr_Gargi_Claim where Policy_Number='"+fraudno+"'")
            rows = cursor.fetchall()
            print(rows)
            
            for i, in rows:
                r=i
                print(r)
            if r=='N':
                print("yupp")

                x="According to the Prediction, The claim raised by with Policy Number-"+fraudno+" is not fraud. Please Carry on other verification."
            else:
                x="According to the Prediction, The claim raised by with Policy Number-"+fraudno+" is Fraud."

            return close(intent_request['sessionAttributes'],
                    'Fulfilled',
                    {'contentType': 'PlainText',
                    'content': x})
           

                            
        
        #         message = {'contentType': 'PlainText', 'content': 'Enter the date of incident '}
        #         return elicit_slot(intent_request['sessionAttributes'],
        #                      intent_request['currentIntent']['name'],
        #                             slots,
        #                             'IncidentDateSlot',
        #                             message)                             
        # validation_result = validate_order_flowers(flower_type, date, pickup_time)
        # if not validation_result['isValid']:
        #     slots[validation_result['violatedSlot']] = None
        #     return elicit_slot(intent_request['sessionAttributes'],
        #                       intent_request['currentIntent']['name'],
        #                       slots,
        #                       validation_result['violatedSlot'],
        #                       validation_result['message'])

        # Pass the price of the flowers back through session attributes to be used in various prompts defined
        # on the bot model.
        
        
        
        # output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        # if flower_type is not None:
        #     output_session_attributes['Price'] = len(flower_type) * 5  # Elegant pricing model

        # return delegate(output_session_attributes, get_slots(intent_request))

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'hey!Thanks for using the application.'})


""" --- Intents --- """


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """
    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'InsuranceClaimsIntents':
        return claim_management(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
