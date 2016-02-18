from firebase import firebase
import random
import EventsCollector


firebase_url = 'https://event-finder-test.firebaseio.com'

robot_data = {}
robot_data['age'] = 100
robot_data['gender'] = 'female'
robot_data['interest'] = ['None'],
robot_data['myAttendanceNumber'] = 0
robot_data['myPostsNumber'] = 0
robot_data['nickname'] = 'robot'
robot_data['password'] = 'robot'
robot_data['username'] = 'python crawler'
robot_data['usrProfileImage'] = ''
robot_data['whatsup'] = 'nothing up'

data_mask = 10000
lat_lower_bound = 42.442454
lat_upper_bound = 42.455479
lng_lower_bound = -76.487715
lng_upper_bound = -76.462526
mock_data = {}
mock_data['data_mask'] = data_mask
mock_data['lat_lower_bound'] = lat_lower_bound
mock_data['lat_upper_bound'] = lat_upper_bound
mock_data['lng_lower_bound'] = lng_lower_bound
mock_data['lng_upper_bound'] = lng_upper_bound
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

	for i in range(len(retrievedData)):
		tmp = retrievedData[i]
		event_data = {}
		event_data['authorName'] = robot_data['username']
		event_data['authorProfileImg'] = robot_data['usrProfileImage']
		event_data['endingTime'] = 201602011510 + random.randint(1, 29) * mock_data['data_mask']
		event_data['imageOfEvent'] = [str([tmp['image']][0])]
		event_data['introOfEvent'] = tmp['description']
		event_data['latOfEvent'] = random.uniform(mock_data['lat_lower_bound'], 
			                                      mock_data['lat_upper_bound'])
		event_data['lngOfEvent'] = random.uniform(mock_data['lng_lower_bound'], 
			                                      mock_data['lng_upper_bound'])
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
	# result = firebase.post('/users', {'this': 'is'})

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


def removeAllPostEvents():
	print 'fetching events from the database ... '
	from firebase import firebase
	firebase = firebase.FirebaseApplication(firebase_url, None)
	events = firebase.get('/events', None)

	print "found", len(events), "events"
	print "Do you want to remove them all?"
	num = len(events)
	print "Are you sure you want to delete all " + str(num) + " events?"
	yes_or_no = raw_input("Y/N: ")
	if yes_or_no == "Y":
		for i in range(0, num):
			firebase.delete('/events', events.keys()[i])

	print "DONE"

if __name__ == '__main__':
	print "Welcome to use this crawler to add events to CU Event Finder"
	print "-------------------------------------------------------"
	print "What would you like to do?"
	print "input 1 to add events"
	print "input 2 to delete events"
	print "input 3 to remove all the events"
	print "input 0 to exit"
	num = input("Your choice: ")
	if num == 0:
		quit()
	elif num == 1:
		postEvents(robot_data, firebase_url, tags_list)
	elif num == 2:
		removeRobotPostEvents(firebase_url, robot_data['username'])
	elif num == 3:
		removeAllPostEvents()






