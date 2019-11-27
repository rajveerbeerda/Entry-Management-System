# Entry-Management-System

### Assumptions:
Enter valid hostname and address as: Sanjay S., C-Block.
 
Network Issue: As Twilio free version doesn’t send messages to unverified numbers, this message will come up, to get your number verified send me an email. If the SMS can’t be sent due to this reason the network issue message is displayed. This message doesn’t affect the functionality of the app in any way. Also, I came across this, there are many regulations hampering the SMS functionality in India.
https://support.twilio.com/hc/en-us/articles/223134167-Limitations-sending-SMS-messages-to-Indian-mobile-devices

There are two files Host and Visitor that contain details of host and visitor respectively.

Approach:
As soon as a visitor clicks on the check-in button, he is asked to enter his own details along with the host’s name and address(which are used to authenticate the visitor). 

The timestamp is captured and an email and SMS is sent to the host, the details are taken from host.csv file and the details of the visitor are stored in the visitor.csv and status is set to 1 denoting the visitor is still in the building.

When the visitor wants to check-out, a list of visitors in the building is shown, he chooses his own name and then the SMS and email are sent to him, with the timestamp and his status is changed to 0 to denote he left the building.

Visitor.csv is the visitor log for the system.

The web-app is scripted entirely in Python, with Flask for Frontend.


## Heroku App Link:
http://entry-management-innovaccer.herokuapp.com/


