import urllib
from bs4 import *

import Preprocess


free_food_keywords = ['free food', 'free pizza']

def timePreprocess(date, time):
    # Proprocess a string to extract starting and ending time. 
    # e.g. date: 20150103  time: " Sunday, May 29, 2016 at 2:30pm to 4:00pm "
    #      return [201501030230, 201501030400]
    # e.g. data: 20150103  time: " Sunday, May 29, 2016 at to 4:00pm "
    #      return None 

    import re
    # Jim Tebbel, http://regexlib.com/DisplayPatterns.aspx?cattabindex=4&categoryId=5&AspxAutoDetectCookieSupport=1
    # Matches     12:00am | 1:00 PM | 12:59 pm
    # Not matches 0:00 | 0:01 am | 13:00 pm
    pattern = re.compile(" *((1[0-2]|[1-9]):[0-5][0-9] *(a|p|A|P)(m|M)) *")

    result = pattern.findall(time)
    if len(result) != 2:
        return None

    def extractNumber(date, string):
        numbers = re.findall("\d+", string)
        return date*10000 + int(numbers[0]) * 100 + int(numbers[1])

    startingTime = extractNumber(date, result[0][0])
    endingTime = extractNumber(date, result[1][0])
    return [startingTime, endingTime]


def retieveEventsAtDate(date, url):
    # root website

    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")

    briefs = soup.select("div.item.event_item.vevent")

    # retieve all the events detail pages url.
    print 'collecting', len(briefs), 'events from', url
    toVisit = []
    for brief in briefs:
        toVisit.append(brief.find('a').get('href'))

    result = []

    # get information from each events detail pages.
    for item in toVisit:
        tmp = {}
        url = item
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html, "html.parser")
        # the event information is reside here. 
        event = soup.select("div.box_header.vevent")[0]

        # extract title from h1 tag's text
        title = event.h1.span.get_text().strip()

        # extract time from h2 tag's abbr field
        time = ""
        for abbr in event.h2.findAll('abbr'):
            time += abbr.get_text().strip() + " "
        print time
        time = timePreprocess(date, time)
        print time
        if time is None:
            print("can't resolve time, discard this event")
            continue
        display_location = event.h3.a
        real_location = event.h3.small

        if display_location is not None and real_location is not None and len(display_location) > 0 and len(real_location) > 0:
            display_location = display_location.get_text().strip()
            real_location = real_location.get_text().strip()
        else:
            # discard bad formated events 
            print("can't resolve location, discard this event")
            continue

        if "Cornell University" in real_location:
            real_location = real_location.replace("Cornell University", "")
            print "real_location becomes: " + real_location 

        if "Ithaca, NY 14853, USA" not in real_location:
            real_location = display_location + ", Ithaca, NY 14853, USA"

        latlng = Preprocess.decodeAddressToCoordinates(real_location)
        print "latlng: %s" % latlng
        lat = latlng['lat']
        lng = latlng['lng']

        # street = event.h3.small
        # if street is not None:
        #     street = street.get_text().strip()
        # else:
        #     street = "Cornell University"

        description = event.select("div.description")
        if len(description) > 0:
            description = description[0].get_text()
        else:
            # discard bad formated events 
            print("can't resolve description, discard this event")
            continue
        image = soup.select("div.box_image")
        if len(image) > 0:
            image = image[0].a.img['src']
        else:
            # discard bad formated events 
            print("can't resolve image, discard this event")
            continue
        tmp['title'] = title
        tmp['time'] = time
        tmp['location'] = display_location
        tmp['description'] = description
        tmp['image'] = image
        tmp['lat'] = lat
        tmp['lng'] = lng
        tmp['secondaryTag'] = ['Cornell Sponsored']

        for free_food_keyword in free_food_keywords:
            if free_food_keyword in tmp['description'].lower():
                tmp['secondaryTag'].append('Free Food')
                break

        print 'retrieved:', tmp['title']
        result.append(tmp)

    # return all events dicitionary in an array.
    return result

if __name__ == '__main__':
    for i in range(1, 2):
        url = 'https://events.cornell.edu/calendar/day/2016/6/' + str(i)
        date = 20160600 + i
        print url
        print retieveEventsAtDate(date, url)
    # print timePreprocess(20150101, "Sunday, May 29, 2016 at 2:30pm to 4:00pm ")

