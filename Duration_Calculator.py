from time import mktime
from time import strptime
from googlemaps import *
from collections import OrderedDict

api_key = "AIzaSyCGSXtXXfWP1noF-09za5MTg61msfVg750"
gmaps = Client(key=api_key)

loc = raw_input("Enter the location: ")
B_work = "Warning Tongue Ln, Branton, Doncaster DN4 6TB"
R_work = "Sidhil Business Park Industrial Estate, Halifax HX2 9TN"

rep_date = "16 16 3"  # Year,WeekNo,WeekDay

data_dict = OrderedDict()
data_dict["1_B_to_work"] = ["07 00", loc, B_work]
data_dict["2_B_back_home"] = ["17 40", B_work, loc]
data_dict["3_R_to_work"] = ["06 20", loc, R_work]
data_dict["4_R_back_home"] = ["16 05", R_work, loc]


def getSeconds(departure, rep_date):
    """Get number of seconds since Epoch and input date/time"""
    return mktime(strptime("%s %s" % (departure, rep_date), "%H %M %y %W %w"))


def getDuration(gmaps, origin, dest, depart_time, rep_date):
    """Return duration between two locations, given departure times and destinations"""
    time_since_epoch = getSeconds(depart_time, rep_date)
    api_query = gmaps.distance_matrix(origin,
                                      dest,
                                      departure_time=time_since_epoch,
                                      mode='driving',
                                      traffic_model='pessimistic')
    duration = api_query['rows'][0]['elements'][0]['duration_in_traffic']['text']
    return duration


def printInformation(duration, origin, dest, B_work, R_work):
    if dest == B_work:
        print "Duration for Becky to get to work:\t%s" % duration
    elif dest == R_work:
        print "Duration for Rick to get to work:\t%s" % duration
    elif origin == B_work:
        print "Duration for Becky to get back home:\t%s" % duration
    elif origin == R_work:
        print "Duration for Rick to get back home:\t%s" % duration
    else:
        pass


"""Main Process"""
for key in data_dict:
    depart_time = data_dict[key][0]
    origin = data_dict[key][1]
    dest = data_dict[key][2]
    current_duration = getDuration(gmaps, origin, dest, depart_time, rep_date)
    printInformation(current_duration, origin, dest, B_work, R_work)

raw_input("\npress enter to close...")
