tags_list = ["Professional Events", "Social Events", "Performance Events",
             "Political Events", "Seminars", "Athletics"]

# Store events with their description into a file, 
# as the data set to build our classifier. 
if __name__ == '__main__':
	import EventsCollector
	output_file = open('text', 'w')
	title_list = []
	for i in range(1, 16):
		url = 'https://events.cornell.edu/calendar/day/2016/4/' + str(i)
		date = 20160600 + i
		retrievedData = EventsCollector.retieveEventsAtDate(date, url)
		for i in range(len(retrievedData)):
			event = retrievedData[i]
			# avoid redundent training data.
			if event['title'] in title_list:
				continue
			title_list.append(event['title'])
			print "\n"
			print "\n"
			print "\n"
			print event['title']
			print "\n"
			print event['location']
			print "\n"
			print event['description']
			print "\n"
			print "Please classify the class for the following events"
			for i in range(len(tags_list)):
				print "%d\t: %s" % (i, tags_list[i])
			num = input("Your choice: ")
			output_file.write(tags_list[num])
			output_file.write("\n")
			output_file.write(event['title'].encode("utf-8"))
			output_file.write(event['location'].encode("utf-8"))
			output_file.write(event['description'].encode("utf-8"))
			output_file.write("\n")
			output_file.write("\n")
			output_file.write("\n")
			output_file.write("\n")
			output_file.write("\n")

			