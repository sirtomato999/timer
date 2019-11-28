import pygame, time, pygame.font, conf_read, sys, random

print "initalizing pygame..."
pygame.init()

print "loading times..."
session_obj = []

for i in xrange(10):
	session_obj.append(open("times_%i.txt" % i))

session_lists = []

#strip newlines
for i in xrange(10):
	session_lists.append(session_obj[i].readlines())
	for x in xrange(len(session_lists[i])):
		session_lists[i][x] = float(session_lists[i][x].strip("\n"))

for i in session_obj: #close readables
	i.close()




print "loading functions..."

### functions

def convert_to_minutes(seconds):
	"""Converts seconds to the regular time format (e.g. 14:34.33)"""
	minutes = int(seconds/60)
	seconds = seconds % 60
	if minutes == 0:
		return "%.2f" % seconds
	elif len(str(seconds).split('.')[0]) == 2:
		return str(minutes) + ":%.2f" % seconds
	elif len(str(seconds).split('.')[0]) == 1:
		return str(minutes) + ":0%.2f" % seconds

def hex_to_rgb(hex_code):
	return [int(hex_code[0:2], 16), int(hex_code[2:4], 16) \
		, int(hex_code[4:6], 16)]

def olympic_average(count):
	"""count: int of items to average"""
	countlist = session_lists[current_session][-count:-1]
	worst = 0
	best = 0
	for i in countlist:
		if i > worst:
			worst = i
		elif i < best:
			best = i
	mid = []
	for i in countlist:
		if i == worst:
			continue
		if i == best:
			continue
		mid.append(i)
	try: return [sum(mid) / len(mid), best, worst]
	except ZeroDivisionError: return [0,0,0]

def save():
	print "saving..."
	session_obj = []
	for i in xrange(10):
		session_obj.append(open("times_%i.txt" % i, 'w'))
	for i in xrange(10):
		for x in session_lists[i]:
			session_obj[i].write(str(x) + "\n")

def generate_scramble(length):
        scramble_items  = ["R", "R'", "L", "L'", "U", "U'", "D", "D'", "B", "B'", "F", "F'"]
        scramble = []
        for i in xrange(length):
                scramble.append(random.choice(scramble_items))
        return " ".join(scramble)

print "reading config..."
try:
	config = open("config.conf")
	config_things = conf_read.read_config(config)
	config.close()

	bg_rgb          = hex_to_rgb(config_things[1])
	fg_rgb          = hex_to_rgb(config_things[2])
	scramble_length = int(config_things[3])

except IOError:
	print("config nonexsistent or has invalid syntax. exiting.")
	sys.exit()

### variables
display         = pygame.display.set_mode([600,250])
clock           = pygame.time.Clock()
timer           = False
time            = 0
current_session = 1
time_font       = pygame.font.SysFont("Monospace", 120)
time_font_blit  = time_font.render("0.00", True, (50,50,50))
avg_font        = pygame.font.SysFont("Monospace", 30)
avg2_font       = pygame.font.SysFont("Monospace", 30)
scramble_font   = pygame.font.SysFont("Monospace", 24)
title_font      = pygame.font.SysFont("Monospace", 28)
scramble        = generate_scramble(scramble_length)
reserved_keys   = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0, pygame.K_r, pygame.K_d]

try:
	time_avg    = sum(session_lists[current_session]) / len(session_lists[current_session])
except: 
	time_avg    = 0
				
while True:
	pygame.draw.rect(display, bg_rgb, [0,0,600,250], 0) #clears screen

	for event in pygame.event.get(): #event loop
		if event.type == pygame.QUIT:
			save()
			pygame.quit()
		if event.type == pygame.KEYUP:
			if (not event.key in reserved_keys) and (time == 0):
                                timer = True
                        
		if event.type == pygame.KEYDOWN:
			if   event.key == pygame.K_0: current_session = 0   # change session binds
			elif event.key == pygame.K_1: current_session = 1
			elif event.key == pygame.K_2: current_session = 2
			elif event.key == pygame.K_3: current_session = 3
			elif event.key == pygame.K_4: current_session = 4
			elif event.key == pygame.K_5: current_session = 5
			elif event.key == pygame.K_6: current_session = 6
			elif event.key == pygame.K_7: current_session = 7
			elif event.key == pygame.K_8: current_session = 8
			elif event.key == pygame.K_9: current_session = 9
			elif event.key == pygame.K_r: 
				session_lists[current_session] = [0]
				time = 0
				print("session reset")
			elif event.key == pygame.K_d:
				try:
					session_lists[current_session].pop()
					print("deleted last time")
				except:
                                        print("session already empty")
			else:
				if not timer:
					time = 0.00
				if timer:
					timer = False
					session_lists[current_session].append(time)
					print("new time %.2f on session %i" % (time, current_session))
					
					scramble = generate_scramble(scramble_length) # generates new scramble after the end of each solve


	if timer: #adds time to timer if it is running
		time = time + 0.01
	time_font_blit = time_font.render(convert_to_minutes(time),True, fg_rgb)
	if not timer:
        	title_font_blit = title_font.render(config_things[0][current_session].strip(),True, fg_rgb)
		avg_font_blit = avg_font.render("ao5: " + convert_to_minutes(olympic_average(5)[0]), True, fg_rgb)
		avg2_font_blit = avg2_font.render("ao12: " + convert_to_minutes(olympic_average(12)[0]), True, fg_rgb)
		scramble_font_blit = scramble_font.render(scramble, True, fg_rgb)
		

		time_font_rect = time_font_blit.get_rect()   #
                title_font_rect = title_font_blit.get_rect() #
		avg_font_rect  = avg_font_blit.get_rect()    # get rects for placement of other text
		avg2_font_rect  = avg2_font_blit.get_rect()  #

                if not session_lists[current_session] == '':
                        display.blit(title_font_blit, [0, time_font_rect.height-3])
                        display.blit(avg_font_blit, [0, time_font_rect.height-3+title_font_rect.height-3])
		        display.blit(avg2_font_blit, [0, avg_font_rect.height-3+time_font_rect.height-3+title_font_rect.height-3])
		        display.blit(scramble_font_blit, [0, avg_font_rect.height-3+time_font_rect.height-3+title_font_rect.height-3+avg2_font_rect.height-3])
                else:
                        display.blit(avg_font_blit, [0, time_font_rect.height-3])
                        display.blit(avg2_font_blit,[0, time_font_rect.height-3+avg_font_rect.height-3])
                        display.blit(scramble_font_blit, [0, time_font_rect.height-3+avg_font_rect.height-3])
 

		try:
			time_avg = sum(session_lists[current_session]) / len(session_lists[current_session])
		except ZeroDivisionError: 
			time_avg = 0

	display.blit(time_font_blit, [0,0])	
	pygame.display.flip()
	clock.tick(100) #max fps 100 because it updates the time once per frame
