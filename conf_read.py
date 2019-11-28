def read_config(obj):
    """obj: file object of config file"""
    lines = obj.readlines()
    names = ['','','','','','','','','','']
    for line in lines:
        line_secs = line.split(":")
	try:
        	names[int(line_secs[0])] = line_secs[1]
	except:
		if line_secs[0] == "fg_color":
			fg = line_secs[1]
		elif line_secs[0] == "bg_color":
			bg = line_secs[1]
                elif line_secs[0] == "scramble_length":
                        scramble_length = line_secs[1]
    return [names, bg, fg, scramble_length]
