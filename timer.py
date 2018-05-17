# TO DO LIST: add config file w/ session titles

import pygame, time, pygame.font, conf_read

print "Initalizing pygame..."
pygame.init()

print "Loading times..."
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

print "Reading config..."
try:
	config = open("config.conf")
	session_names = conf_read.read_config(config)
	config.close()
except IOError:
	print("config nonexsistent or has invalid syntax. Ignoring")


print "Loading GUI and essential variables..."
### variables
display         = pygame.display.set_mode([250,100])
clock           = pygame.time.Clock()
timer           = False
time            = 0
current_session = 0
time_font       = pygame.font.SysFont("Monospace", 60)
time_font_blit  = time_font.render("0.00", True, (50,50,50))
avg_font        = pygame.font.SysFont("Monospace", 18)
avg2_font       = pygame.font.SysFont("Monospace", 18)
title_font      = pygame.font.SysFont("Monospace", 24)
try:
	time_avg    = sum(session_lists[current_session]) / len(session_lists[current_session])
except: 
	time_avg    = 0

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
				
while True:
	pygame.draw.rect(display, [200,200,200], [0,0,250,100], 0) #clears screen

	for event in pygame.event.get(): #event loop
		if event.type == pygame.QUIT:
			save()
			pygame.quit()
		if event.type == pygame.KEYUP:
			if time == 0: timer = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_0: current_session = 0
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
			elif event.key == pygame.K_d: session_lists[current_session].pop()
			else:
				if not timer:
					time = 0.00
				if timer:
					timer = False
					session_lists[current_session].append(time)


	if timer: #adds time to timer if it is running
		time = time + 0.01
		time_font_blit = time_font.render(convert_to_minutes(time),True, (50,50,50))
	elif not timer:
		avg_font_blit = avg_font.render("ao5: " + convert_to_minutes(olympic_average(5)[0]), True, (50,50,50))
		avg2_font_blit = avg2_font.render("ao12: " + convert_to_minutes(olympic_average(12)[0]), True, (50,50,50))

		time_font_rect = time_font_blit.get_rect() #
		avg_font_rect  = avg_font_blit.get_rect()  # get rects for placement of other text

		display.blit(avg_font_blit, [0, time_font_rect.height-10])
		display.blit(avg2_font_blit, [0, avg_font_rect.height-3+time_font_rect.height-10])
		try:
			time_avg = sum(session_lists[current_session]) / len(session_lists[current_session])
		except ZeroDivisionError: 
			time_avg = 0

	display.blit(time_font_blit, [0,0])	
	pygame.display.flip()
	clock.tick(100) #max fps 100 because it updates the time once per frame