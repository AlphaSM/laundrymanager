from flask import Flask, render_template, request
from datetime import datetime, timedelta
import pywhatkit as pwk
import requests


app = Flask(__name__)
name = ""
nest_group_id = 'C8vvBCM3RS6Bvz6W6m0zJG'


#a bot sends a message to a number
def callmebot_send_whatsapp_to_user(phone, message):
  API_KEY = '1434660'
  # Construct the URL with your parameters
  phone = "+27"+phone[1:]
  message = message.replace(" ", "+")
  url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text={message}&apikey={API_KEY}"

  # Send the GET request
  response = requests.get(url)

  # Check the response
  if response.status_code == 200:
      print("Message sent successfully!")
  else:
      print("Failed to send message. Status code:", response.status_code)
#opens up whatsapp web to send a message 
def send_whatsapp_to_groupchat(Message):
  try:
    # Replace 'group_id' with your actual group ID and adjust the time as needed
    pwk.sendwhatmsg_to_group_instantly("Hs699K7Y9d5JIhw4yAvOrb", Message)
    print("Message Sent Successfully!")
  except Exception as e:
    print("Error in sending the message:", e)
def send_whatsapp_to_user(phone, Message, hour, minute):
  try:
    phone = "+27"+phone
    pwk.sendwhatmsg(phone, Message, hour, minute)
    print("Message Sent Successfully!")
  except Exception as e:
    print("Error in sending the message:", e)

#list of cellphone numbers 
phone_numbers = ["0659740686", "0798613358", "112-223-3344"]
#list of all the countries
country_codes = [
    "93", "355", "213", "1-684", "376", "244", "1-264", "672", "1-268", "54", "374", "297", "61", "43", "994", "1-242", "973", "880", "1-246", 
    "375", "32", "501", "229", "1-441", "975", "591", "387", "267", "55", "246", "1-284", "673", "359", "226", "257", "855", "237", "1", "238", 
    "1-345", "236", "235", "56", "86", "61", "61", "57", "269", "682", "506", "385", "53", "599", "357", "420", "243", "45", "253", "1-767", 
    "1-809, 1-829, 1-849", "670", "593", "20", "503", "240", "291", "372", "251", "500", "298", "679", "358", "33", "689", "241", "220", "995", 
    "49", "233", "350", "30", "299", "1-473", "1-671", "502", "44-1481", "224", "245", "592", "509", "504", "852", "36", "354", "91", "62", 
    "98", "964", "353", "44-1624", "972", "39", "225", "1-876", "81", "44-1534", "962", "7", "254", "686", "383", "965", "996", "856", "371", 
    "961", "266", "231", "218", "423", "370", "352", "853", "389", "261", "265", "60", "960", "223", "356", "692", "222", "230", "262", "52", 
    "691", "373", "377", "976", "382", "1-664", "212", "258", "95", "264", "674", "977", "31", "599", "687", "64", "505", "227", "234", "683", 
    "850", "1-670", "47", "968", "92", "680", "970", "507", "675", "595", "51", "63", "870", "48", "351", "1-787, 1-939", "974", "242", "262", 
    "40", "7", "250", "590", "290", "1-869", "1-758", "590", "508", "1-784", "685", "378", "239", "966", "221", "381", "248", "232", "65", 
    "599", "421", "386", "677", "252", "27", "82", "211", "34", "94", "249", "597", "47", "268", "46", "41", "963", "886", "992", "255", "66", 
    "228", "690", "676", "1-868", "216", "90", "993", "1-649", "688", "1-340", "256", "380", "971", "44", "1", "598", "998", "678", "379", 
    "58", "84", "681", "212", "967", "260", "263"
]
#build a numnber 
def phone_number(phone, country_select):
  phone = "+"+country_select+phone[1:]
  return phone


@app.route('/', methods = ['POST', 'GET'])
def index():
  if request.method == 'POST':
    #getting form data 
    name = request.form.get('name')
    phone = request.form.get('phone')
    country_select = request.form.get('machine_type')
    machine_status = request.form.get('machine_status')
    machine_type = request.form.get('machine_type')
    #getting time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    #for message sending
    current_hour = now.hour
    current_minute = now.minute
    #getting 45 mins in the future 
    time_difference = timedelta(minutes=45)
    future_time = now + time_difference
    future_time = future_time.strftime("%H:%M:%S")


    #notify group that X is using this machine and should be done by Y time
    if machine_status == "using": 
      message = f"{name} is using {machine_type} from {current_time} and should be done by {future_time}"
      phone = phone_number(phone, country_select)
      print(phone)
      callmebot_send_whatsapp_to_user(phone, message)
      #send_whatsapp_to_groupchat(message)
      print(message)
      return "Form submitted successfully!"
    
    #which machine is busy
    if machine_status == "busy":
      message = f"{name} has reported {machine_type} is busy at {current_time}"
      send_whatsapp_to_groupchat(message)
      print(message)
      return "Form submitted successfully! Your message: '{message}' has been sent"
    
    #which machine is done
    if machine_status == "done":
      message = f"{name} has reported {machine_type} is done at {current_time}"
      send_whatsapp_to_groupchat(message)
      print(message)
      return "Form submitted successfully! Your message: '{message}' has been sent"
    
    #which machine is broken
    if machine_status == "broken":
      message = f"{name} has reported {machine_type} is broken at {current_time}"
      send_whatsapp_to_groupchat(message)
      print(message)
      return "Form submitted successfully! Your message: '{message}' has been sent"
    
    #notify group that X is using this machine and should be done by Y time
    if machine_status == "fixed": 
      message = f"{name} has reported {machine_type} is fixed at {current_time}"
      send_whatsapp_to_groupchat(message)
      print(message)
      return "Form submitted successfully! Your message: '{message}' has been sent"

    # Process the data as needed
    #print(f"Name: {name}, Phone: {phone}, Machine Status: {machine_status}, Machine Type: {machine_type}")
    #return "Form submitted successfully!"
  return render_template('index.html')

    
    
    

   

if __name__ == "__main__":
  app.run(debug = True)