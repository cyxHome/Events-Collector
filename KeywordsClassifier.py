tags_list = ["Professional Events", "Social Events", "Performance Events",
             "Political Events", "Seminars", "Athletics"]

keywords_list = [["professional", "scholarship", "internship"], 
				 ["social", "lunch", "dinner", "club", "sponsored", "coffee", "camp"], 
				 ["performance", "music", "exhibition", "museum", "art", "theatre", "fashion", "show"], 
				 ["politic", "policy", "mtg"], 
				 ["seminar", "research", "colloquium", "lecture"], 
				 ["sport", "yoga", "ball"]]

# fed the title, location and description of the events to the classifier
# it returns the primary tag of the event.
def classify(text):
	import re
	for i in range(6):
		for j in range(len(keywords_list[i])):
			if re.match("(^.*\s+"+keywords_list[i][j]+"[^a-z]+.*$)|(^\s*"+keywords_list[i][j]+"[^a-z]*$)|(^.*\s+"+keywords_list[i][j]+"[^a-z]*$)|(^\s*"+keywords_list[i][j]+"[^a-z]+.*$)", text.lower()) is not None:
				return tags_list[i]
	return tags_list[4]
