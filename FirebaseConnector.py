from firebase import firebase
import random
import EventsCollector
import Preprocess
import KeywordsClassifier

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
	month = 5
	nameSet = []
	for day in range(16, 17):
		url = 'https://events.cornell.edu/calendar/day/2016/%s/%s' % (str(month), str(day)) 
		date = 20160000 + month*100 + day 
		retrievedData = EventsCollector.retieveEventsAtDate(date, url)
		

		for i in range(len(retrievedData)):
			tmp = retrievedData[i]
			if tmp['title'] in nameSet:
				continue
			nameSet.append(tmp['title'])
			event_data = {}
			event_data['authorName'] = robot_data['username']
			event_data['authorProfileImg'] =  robot_data['usrProfileImage']
			event_data['startingTime'] = tmp['time'][0]
			event_data['endingTime'] = tmp['time'][1]
			event_data['imageOfEvent'] = [str([tmp['image']][0])]
			event_data['introOfEvent'] = tmp['description']
			event_data['latOfEvent'] = tmp['lat']
			event_data['lngOfEvent'] = tmp['lng']
			event_data['locationOfEvent'] = tmp['location']
			event_data['nameOfEvent'] = tmp['title']
			event_data['numberOfViewed'] = 0

			import datetime
			now = datetime.datetime.now()
			post_time = now.date().year * 10000 + now.date().month * 100 + now.date().day
			post_time = post_time * 10000 + now.time().hour * 100 + now.time().minute
			event_data['postTime'] = post_time
			event_data['restriction'] = ""
			event_data['secondaryTag'] = tmp['secondaryTag']

			text = tmp['title'] + "\n" + tmp['location'] + "\n" + tmp['description']
			event_data['primaryTag'] = KeywordsClassifier.classify(text)
			
			post_event = firebase.post('/events', event_data)
			print 'posted:', event_data
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


def removeAllPostEvents(firebase_url):
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

