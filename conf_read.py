def read_config(obj):
    """obj: file object of config file"""
    lines = obj.readlines()
    names = ['','','','','','','','','','']
    for line in lines:
        line_secs = line.split(":")
        names[int(line_secs[0])-1] = line_secs[1]
    return names