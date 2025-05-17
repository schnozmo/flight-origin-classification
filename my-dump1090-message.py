#!/usr/bin/python -u

import sys, math, subprocess, re, os, json, time
import datetime as dt

def get_aircraft(h):
	if h in fast_aircraft:
		return fast_aircraft[h]
	
	dir = "/usr/share/dump1090-fa/html/db/"
	n = 6
	while n > 0:
		f = dir + h[0:n] + ".json"
		if os.access(f, os.R_OK):
			fh = open(f, 'r')
			j = dict(json.load(fh))
			fh.close()
			if h[n:] in j.keys() and 't' in j[h[n:]].keys():
				return str(j[h[n:]]['t'])
		n -= 1
	return ""

fast_aircraft = {}
def load_aircraft():
	if os.path.exists("/home/pi/flightaware/hexid.airframe.txt"):
		d = {}
		tmp_fh = open("/home/pi/flightaware/hexid.airframe.txt", 'r')
		for l in tmp_fh:
			ln = l.rstrip("\n\r").split("|", 1)
			if len(ln) == 2:
				d[ln[0]] = ln[1]
		tmp_fh.close()
		return d
	else:
		return {}

def send_notification(settings):
	if 'message' not in settings.keys():
		print("no 'message' key in settings, can't push notification")

	form_str = '&'.join([k + '=' + settings[k] for k in settings.keys()])

	print("Sending notification for", settings['message'])
	cmd = "wget --post-data '" + form_str + "' https://api.pushover.net/1/messages.json"
	print("wget command: " + cmd)
	p = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
	p.stdout.read()
	if os.path.exists("messages.json"):
		os.unlink("messages.json")

def calculate_initial_compass_bearing(pointA, pointB):
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLat = math.radians(pointB[0] - pointA[0])
    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    R = 6373.0 # radius of earth in radians
    a = math.sin(diffLat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(diffLong / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return compass_bearing, distance

def newFlight(r, h):
	flights[h] = {}
	flights[h]['complete'] = True
	flights[h]['msgs'] = 1
	flights[h]['first_time'] = int(r['clock'])
	flights[h]['last_time'] = int(r['clock'])
	flights[h]['ac_type'] = get_aircraft(h)

	if 'ident' in r.keys():
		flights[h]['ident'] = r['ident']
	else:
		flights[h]['ident'] = ""
		flights[h]['complete'] = False

	if 'alt' in r.keys():
		flights[h]['alt'] = int(r['alt'])
	else:
		flights[h]['alt'] = -1
		flights[h]['complete'] = False

	if 'speed' in r.keys():
		flights[h]['speed'] = float(r['speed'])
	else:
		flights[h]['speed'] = -1.
		flights[h]['complete'] = False

	if 'track' in r.keys():
		flights[h]['track'] = float(r['track'])
	else:
		flights[h]['track'] = 361.
		flights[h]['complete'] = False

	if 'lat' in r.keys():
		flights[h]['last_lat'] = float(r['lat'])
		flights[h]['last_lon'] = float(r['lon'])
		b, d = calculate_initial_compass_bearing((my_lat, my_lon), 
                                                         (flights[h]['last_lat'], flights[h]['last_lon']))
		flights[h]['bearing'] = b
		flights[h]['distance'] = d
	else:
		flights[h]['complete'] = False
		flights[h]['last_lat'] = 200
		flights[h]['last_lon'] = 200
		flights[h]['bearing'] = 361
		flights[h]['distance'] = 1000

def updateFlight(r, h):
	flights[h]['msgs'] += 1
	flights[h]['last_time'] = int(r['clock'])
	if 'ident' in r.keys() and flights[h]['ident'] != "" and flights[h]['ident'] != r['ident']:
		print("IDENT MISMATCH - (curr vs flights) - #"+ r['ident'] + "# vs #" + flights[h]['ident'] + "#")
		flights[h]['ident'] = r['ident']
	elif 'ident' in r.keys() and flights[h]['ident'] == "":
		flights[h]['ident'] = r['ident']

	alt_chg = 0
	if 'alt' in r.keys():
		alt_chg = int(r['alt']) - flights[h]['alt']
		flights[h]['alt'] = int(r['alt'])

	speed_chg = 0
	if 'speed' in r.keys():
		speed_chg = float(r['speed']) - flights[h]['speed']
		flights[h]['speed'] = float(r['speed'])

	track_chg = 0
	if 'track' in r.keys():
		track_chg = float(r['track']) - flights[h]['track']
		if track_chg < -180:
			track_chg += 360
		flights[h]['track'] = float(r['track'])
	
	if 'lat' in r.keys():
		flights[h]['last_lat'] = float(r['lat'])
		flights[h]['last_lon'] = float(r['lon'])
		b, d = calculate_initial_compass_bearing((my_lat, my_lon), 
                                                         (flights[h]['last_lat'], flights[h]['last_lon']))
		flights[h]['bearing'] = b
		flights[h]['distance'] = d

	if flights[h]['alt'] == -1 or flights[h]['speed'] == -1 or flights[h]['track'] == 361 or flights[h]['distance'] == 1000 or flights[h]['ident'] == "" or flights[h]['last_lat'] == 200 or flights[h]['last_lon'] == 200:
		flights[h]['complete'] = False
	else:
		flights[h]['complete'] = True

	if flights[hexid]['complete']:
		all_fh.write("%s|%s|%s|%s|%f|%f|%f|%f|%f|%d|%d|%d|%d|%f|%f|%f|%f\n" % (dt.datetime.now().strftime("%Y%m%d.%H%M%S"), hexid,
                                                             flights[hexid]['ident'], flights[h]['ac_type'],
                                                             flights[hexid]['distance'], flights[hexid]['alt'],
                                                             flights[hexid]['track'], flights[hexid]['speed'], flights[hexid]['bearing'],
                         		                             wind_dir, wind_sust, wind_gust, alt_chg, speed_chg, track_chg, flights[h]['last_lat'], flights[h]['last_lon']))
		all_fh.flush()

def isComingHere(h):
	if flights[h]['bearing'] == 361 or flights[h]['track'] == 361:
		return False
	elif flights[h]['distance'] > 3 or flights[h]['alt'] > 14000:
		return False
	print(flights[h]['distance'], flights[h]['alt'], flights[h]['ident'], flights[h]['ac_type'])
	rev_bearing = (flights[h]['bearing'] + 180) % 360
	if abs(rev_bearing - flights[h]['track']) < 180:
		return True
	else:
		return False

def isComingHereLow(h):
	if isComingHere(h) and flights[h]['alt'] <= 8000:
		return True
	else:
		return False

def isNear(h):
	if flights[h]['distance'] > 6 or flights[h]['alt'] > 16000:
		return False
	else:
		return True

def cleanFlights():
	for k in flights.keys():
		if last_clock - flights[k]['last_time'] > 900:
			flights.pop(k, "blah")

# <code>KEWR 200151Z 33011KT 10SM OVC250 00/M16 A3060 RMK AO2 SLP362 T00001156</code><br/>
def get_wind(metar_file):
	if os.access(metar_file, os.F_OK):
		fh = open(metar_file, 'r')
		for line in fh:
			match = re.search("([A-Z][A-Z][A-Z][A-Z]) \d\d(\d\d\d\d)Z", line)
			if match != None:
				fh.close()
				code = match.group(1)
				metar_time = match.group(2)
				match = re.search(" (\d\d\d)(\d\d)KT ", line)
				if match != None:
					return code, metar_time, int(match.group(1)), int(match.group(2)), int(match.group(2))
				match = re.search(" (\d\d\d)(\d\d)G(\d\d)KT ", line)
				if match != None:
					return code, metar_time, int(match.group(1)), int(match.group(2)), int(match.group(3))
				else:
					return code, metar_time, 0, 0, 0

def is_running():
	f = "/home/pi/flightaware/pid.my-dump"
	if os.access(f, os.F_OK):
		fh = open(f, 'r')
		pid = int(fh.readline().rstrip('\r\n'))
		fh.close()
		if os.access("/proc/" + str(pid), os.F_OK):
			return pid
	return 0

def start_1090_proc():
	cmd = "/usr/lib/piaware/helpers/faup1090 --net-bo-ipaddr localhost --net-bo-port 30005 --stdout --lat 40.368 --lon -74.192"
	subp_obj = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
	return subp_obj.stdout

subp_obj_1090 = None

pid = is_running()
if pid > 0:
	print("Running as " + str(pid))
	sys.exit()

# claim running
pid_fh = open("/home/pi/flightaware/pid.my-dump", 'w')
pid = os.getpid()
pid_fh.write("%d\n" % pid)
pid_fh.close()

# read metar
try:
	airport, metar_time, wind_dir, wind_sust, wind_gust = get_wind('/home/pi/flightaware/kewr_metar.txt')
except:
	print("Problem with metar file:")
	print(open('/home/pi/flightaware/kewr_metar.txt', 'r').read())
	airport="-1"
	metar_time="-1"
	wind_dir=-1
	wind_sust=-1
	wind_gust=-2

# key = hexid, subkeys = msgs, ident, last_time, last_lat, last_lon, track, bearing, distance, alt
flights = {}

# key = hexid, value = distance
near = {}
recent_near = []
recent_first = []
last_clock = 0
my_lat = 40.368
my_lon = -74.192
last_coming_here = ""
nrecs = 0
widebodies = ['A388', 'B748', 'B744', 'B742', 'B741', 'B772', 'B773', 'B77L', 'B77W', 
              'B788', 'B789', 'B78X', 'A346', 'A330', 'A343', 'A345', 'A333', 'A332', 'A359', 'A35K'
              'B764', 'B763', 'A306', 'B753', 'MD11']

fast_aircraft = load_aircraft()
print("loaded " + str(len(fast_aircraft.keys())) + " frequent aircraft and their types")

log_file = "/home/pi/flightaware/pid." + str(pid) + "." + dt.datetime.now().strftime("%Y%m%d.%H%M%S") + ".log"
log_fh = open(log_file, 'w')

app_file = "/home/pi/flightaware/pid." + str(pid) + "." + dt.datetime.now().strftime("%Y%m%d.%H%M%S") + ".approach.csv"
app_fh = open(app_file, 'w')

all_file = "/home/pi/flightaware/pid." + str(pid) + "." + dt.datetime.now().strftime("%Y%m%d.%H%M%S") + ".allflights-wchg.csv"
all_fh = open(all_file, 'w')

#for line in sys.stdin:
#for line in iter(p.stdout.readline, ""):
#for line_tuple in get_new_1090_line(fh_1090):
while True:
	if subp_obj_1090 is None:
		subp_obj_1090 = start_1090_proc()
		print("First start of 1090")
	next_line = subp_obj_1090.readline()
	while not next_line:
		print("1090 is EOF, sleeping, then restarting")
		time.sleep(1)
		subp_obj_1090 = start_1090_proc()
		next_line = subp_obj_1090.readline()

	ln = next_line.rstrip('\r\n').split('\t')
	curr_rec = {}

	i = 0
	while i < len(ln):
		if ln[i] == 'position':
			pos_match = re.search("{([\d\.\-]+) ([\d\.\-]+) ", ln[i+1])
			if pos_match != None:
				curr_rec['lat'] = pos_match.group(1)
				curr_rec['lon'] = pos_match.group(2)

		curr_rec[ln[i]] = ln[i+1].strip().split(' ')[0]
		i+=2

	if 'clock' in curr_rec.keys():
		last_clock = int(curr_rec['clock'])
	if 'hexid' not in curr_rec.keys():
		continue
	if 'ident' in curr_rec.keys():
		curr_rec['ident'] = re.sub('[{}]', '', curr_rec['ident'])

	hexid = curr_rec['hexid']
	if hexid in flights.keys():
		updateFlight(curr_rec, hexid)
		#print "update - ", flights[hexid]

	else:
		newFlight(curr_rec, hexid)
		#print "new    - ", flights[hexid]

	#if isVeryNear(hexid) == 1 and last_coming_here != hexid:
	if isNear(hexid):
		if hexid in near.keys() and hexid not in recent_near:
			if flights[hexid]['distance'] > near[hexid]:
				#log_fh.write("%s|%s|%s|%s|%f|%f|%f|%f|%d|%d|%d\n" % (dt.datetime.now().strftime("%Y%m%d.%H%M%S"), hexid, 
                #                                                            flights[hexid]['ident'], get_aircraft(hexid),
                #                                                            near[hexid], flights[hexid]['alt'], 
                #                                                            flights[hexid]['track'], flights[hexid]['speed'],
				#					    wind_dir, wind_sust, wind_gust))
				#log_fh.flush()
				del near[hexid]
				recent_near.insert(0, hexid)
				if len(recent_near) > 4:
					recent_near.pop()
			else:
				near[hexid] = flights[hexid]['distance']
		else:
			near[hexid] = flights[hexid]['distance']

		
		if hexid not in recent_first:
			app_fh.write("%s,%s,%s,%s,%s,%f,%f,%f,%f,%.1f,%.1f,%d,%d,%d\n" % (dt.datetime.now().strftime("%Y%m%d.%H%M%S"), hexid, 
                                                                        flights[hexid]['ident'], flights[hexid]['ident'][:3], flights[h]['ac_type'],
                                                                        flights[hexid]['last_lat'], flights[hexid]['last_lon'],
                                                                        flights[hexid]['alt'], flights[hexid]['distance'],
                                                                        flights[hexid]['track'], flights[hexid]['speed'],
									wind_dir, wind_sust, wind_gust))
			app_fh.flush()
			recent_first.insert(0, hexid)
			if len(recent_first) > 10:
				recent_first.pop()

	if isComingHereLow(hexid) and last_coming_here != hexid and (flights[hexid]['ac_type'] in widebodies or flights[hexid]['ac_type'] == ""):
		# push notification
		message = "Flight = " + flights[hexid]['ident'] + " (" + flights[hexid]['ac_type'] + ") at altitude " + str(flights[hexid]['alt'])
		notif_settings = {'token': 'actkmpvdi83xifcpbr5vgmt4uhw9ih', 
                                          'user': 'u9bvt1c6947hwsjo24gtiyn54yx74j',
                                          'sound': 'none',
                                          'message': message}
		if 'ident' in flights[hexid].keys() and flights[hexid]['ident'] != '':
			notif_settings['url'] = "https://flightaware.com/live/flight/" + flights[hexid]['ident']
			notif_settings['url_title'] = 'Flightaware details'
		send_notification(notif_settings)

		print("\n" + hexid + " is coming this way!!!!\n    " + str(flights[hexid]))
		
		last_coming_here = hexid
	nrecs += 1
	if nrecs % 50 == 0:
		sys.stdout.flush()
		if nrecs % 500 == 0:
			print("flights before cleaning: " + str(len(flights.keys())))
			cleanFlights()
			print("flights after cleaning:  " + str(len(flights.keys())))
			print("flights in near:         " + str(len(near.keys())))
			print("flights in recent near:  " + str(recent_near))
				
			# read metar
			airport, metar_time, wind_dir, wind_sust, wind_gust = get_wind('/home/pi/flightaware/kewr_metar.txt')

print("Read all lines???")
