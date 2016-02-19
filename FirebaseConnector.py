from firebase import firebase
import random
import EventsCollector
import Preprocess

data_mask = 10000
mock_data = {}
mock_data['data_mask'] = data_mask
mock_data['restriction'] = 'None'
mock_data['secondary_tag'] = ['Cornell Sponsored']

tags_list = ["Professional Events", "Social Events", "Performance Events",
             "Political Events", "Seminars", "Athletics"]


def createUser(robot_data, firebase_url):
	from firebase import firebase
	firebase = firebase.FirebaseApplication(firebase_url, None)
	users = firebase.get('/users', None)

	username_has_been_created = False
	if users is not None and len(users) > 0:
		for user in users.values():
			if user['username'] == robot_data['username']:
				username_has_been_created = True
				break

	# create a robot user if has not been created yet. 
	if username_has_been_created == False:
		print "creating robot user:", robot_data['username']
		usr_data = {
			'age': robot_data['age'],
			'gender': robot_data['gender'],
			'interest': robot_data['interest'], 
			'myAttendanceNumber': robot_data['myAttendanceNumber'],
			'myPostsNumber': robot_data['myPostsNumber'],
			'nickname': robot_data['nickname'],
			'password': robot_data['password'],
			'username': robot_data['username'],
			'usrProfileImage': robot_data['usrProfileImage'],
			'whatsup': robot_data['whatsup']
		}
		post_user = firebase.post('/users', usr_data)
		print post_user
	return robot_data


def postEvents(robot_data, firebase_url, tags_list):
	from firebase import firebase
	firebase = firebase.FirebaseApplication(firebase_url, None)

	createUser(robot_data, firebase_url)
	retrievedData = EventsCollector.retieveEvents()

	nameSet = []

	for i in range(len(retrievedData)):
		tmp = retrievedData[i]
		if tmp['title'] in nameSet:
			continue
		nameSet.append(tmp['title'])
		event_data = {}
		event_data['authorName'] = robot_data['username']
		event_data['authorProfileImg'] = robot_data['usrProfileImage']
		event_data['endingTime'] = 201602011510 + random.randint(1, 29) * mock_data['data_mask']
		event_data['imageOfEvent'] = [str([tmp['image']][0])]
		event_data['introOfEvent'] = tmp['description']
		latlng = Preprocess.decodeAddressToCoordinatesIthaca(tmp['location'])
		event_data['latOfEvent'] = latlng['lat']
		event_data['lngOfEvent'] = latlng['lng']
		event_data['locationOfEvent'] = tmp['location']
		event_data['nameOfEvent'] = tmp['title']
		event_data['numberOfViewed'] = 0
		event_data['postTime'] = 201602011310 + random.randint(0, 30) * mock_data['data_mask']
		event_data['primaryTag'] = tags_list[random.randint(0, 5)]
		event_data['restriction'] = mock_data['restriction']
		event_data['secondaryTag'] = mock_data['secondary_tag']
		event_data['startingTime'] = event_data['endingTime'] - mock_data['data_mask']
		
		post_event = firebase.post('/events', event_data)
		print 'posted:', post_event
	print "DONE"
	print "\n"
	print "\n"
	print "\n"

def threaded_function(stop_event):
	from time import sleep
	while (not stop_event.is_set()):
		sleep(3)
		print '.'

def removeRobotPostEvents(firebase_url, robot_name):
	
	import threading
	from firebase import firebase

	print 'fetching events from the database ... '
	stop_event= threading.Event()
	thread = threading.Thread(target = threaded_function, args = [stop_event])
	thread.start()
    
	firebase = firebase.FirebaseApplication(firebase_url, None)
	events = firebase.get('/events', None)
	robot_event_list_key = []

	if events == None:
		stop_event.set()
		print "There is no events in the database."
		print "\n"
		print "\n"
		print "\n"
		return


	for key in events:
		if events[key]['authorName'] == robot_name:
			robot_event_list_key.append(key)

	stop_event.set()

	print "robot had posted", len(robot_event_list_key), "events"
	print "How many events you want to delete today?"
	num = input("Number: ")
	print "Are you sure you want to delete " + str(num) + " events?"
	yes_or_no = raw_input("Y/N: ")
	if yes_or_no == "Y":
		for i in range(min(num, len(robot_event_list_key))):
			firebase.delete('/events', robot_event_list_key[i])
			print 'deleted', i, 'events'

	print "DONE"
	print "\n"
	print "\n"
	print "\n"


def removeAllPostEvents():
	print 'fetching events from the database ... '
	from firebase import firebase
	firebase = firebase.FirebaseApplication(firebase_url, None)
	events = firebase.get('/events', None)

	if events == None:
		print "There is no events in the database."
		print "\n"
		print "\n"
		print "\n"
		return

	print "found", len(events), "events"
	print "Do you want to remove them all?"
	num = len(events)
	print "Are you sure you want to delete all " + str(num) + " events?"
	yes_or_no = raw_input("Y/N: ")
	if yes_or_no == "Y":
		for i in range(num):
			firebase.delete('/events', events.keys()[i])
			print 'deleted', i, 'events'

	print "DONE"
	print "\n"
	print "\n"
	print "\n"

