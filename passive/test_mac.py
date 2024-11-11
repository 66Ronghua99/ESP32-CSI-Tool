mac_map = {}
def process(res):
    all_data = res.split(',')
    if all_data[2] not in mac_map.keys():
        mac_map[all_data[2]] = 0
    mac_map[all_data[2]] += 1
        
    

with open("data/emptyroom.csv", "r") as f:
    for line in f:
        line = line.replace('\x00', '').strip()
        if len(line) == 0:
            continue
        if "CSI_DATA" in line:
            process(line)

mac_map = dict(sorted(mac_map.items(), key = lambda item: item[1], reverse=True))
print(list(mac_map.items())[:20])
    
