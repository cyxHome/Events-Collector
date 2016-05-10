
# Need to specify ithaca for better searching
def decodeAddressToCoordinatesIthaca( address ):
        return decodeAddressToCoordinates( address + ", Ithaca")

# Taken from: 
# http://stackoverflow.com/questions/15285691/googlemaps-api-address-to-coordinates-latitude-longitude
def decodeAddressToCoordinates( address ):
        print "address: %s" % address
        import urllib
        import urllib2
        import StringIO
        import json
        urlParams = {
                'address': address,
                'sensor': 'false',
        }  
        url = 'http://maps.google.com/maps/api/geocode/json?' + urllib.urlencode( urlParams )
        response = urllib2.urlopen( url )
        responseBody = response.read()

        body = StringIO.StringIO( responseBody )
        result = json.load( body )
        if 'status' not in result or result['status'] != 'OK':
                return None
        else:
                return {
                        'lat': result['results'][0]['geometry']['location']['lat'],
                        'lng': result['results'][0]['geometry']['location']['lng']
                }  

if __name__ == '__main__':
        print decodeAddressToCoordinates("Herbert F. Johnson Museum of Art, 114 Central Ave, Ithaca, NY 14853, USA")