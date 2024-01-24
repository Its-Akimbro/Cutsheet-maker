import os
from datetime import datetime, timedelta

legacy_switch_name = ""
Date = str(datetime.today() - timedelta(days=7))
header = "Legacy Switch,Legacy Switch IP,Legacy Switch Port,PP Port #,New Switch,New Switch IP,New Switch Port,New Patch Cord Color,Critical Device (Y/N),John's suggested switch,John's suggested blade and port,Status,Speed,Duplex,Access Vlan,Voice Vlan,Legacy Port Description,Mac Address,IP Address,Vendor,First Seen,Last Seen"
ap_mac = ["c8:4c:75","50:87:89","88:f0:31"]

ap_vlan = ""
new_switch_name = ""

class new_switch():
    def __init__(self, switch_model: str,filled_blades: dict):
        self.switch_model = switch_model
        self.filled_blades = filled_blades

def legacy_switch_name_finder(file_name):
    global legacy_switch_name

    with open(file_name) as netDB_file:
        netDB_file.readline()

        list_of_i = netDB_file.readline().split(",")
        legacy_switch_name = list_of_i[0]

def line_combiner(file_name):
    global legacy_switch_name

    with open(file_name) as raw_netDB_data:
        with open(f"Lines Combined {legacy_switch_name}.txt", "w") as final_data:
            for i in raw_netDB_data:
                next_line_data = open(file_name)
                for k in next_line_data:
                    if k == i:
                        next_line = next_line_data.readline()
                        next_line_data.close()
                        break

                if i.startswith(legacy_switch_name) and not next_line.startswith(","):
                    final_data.write(i)
                
                if i.startswith(legacy_switch_name) and next_line.startswith(","):
                    final_data.write(i.strip('\n') + next_line)

def only_connected():
    global legacy_switch_name
    global Date

    with open(f"Lines Combined {legacy_switch_name}.txt") as combined_data:
        with open(f"Only Connected {legacy_switch_name}.txt", "w+") as connected:
            for i in combined_data:
                list_of_i = i.split(",")

                if list_of_i[2] == "connected":

                    if list_of_i[1][:2] == "Po" or list_of_i[1][:4] == "Vlan" or list_of_i[1][:4] == "mgmt":
                        continue

                    if list_of_i[5] == "routed" or list_of_i[5] == "trunk" :
                        continue

                    if Date > list_of_i[14][:10] and list_of_i[14][:10] != "" :
                        continue

                    else:
                        connected.write(i)
                
    if os.path.getsize(f"Only Connected {legacy_switch_name}.txt") == 0: 
        os.remove(f"Only Connected {legacy_switch_name}.txt")
        os.remove(f"Lines Combined {legacy_switch_name}.txt")
        print(f"\nThere are no end user devices connected to switch {legacy_switch_name}\n")
        return 1

    else:
        os.remove(f"Lines Combined {legacy_switch_name}.txt")
        
def excess_data_removal():
    global legacy_switch_name

    with open(f"Only connected {legacy_switch_name}.txt") as connected_data:
        with open(f"Excess Data removed {legacy_switch_name}.txt", "w") as exccess_removed:
            for i in connected_data:
                list_of_i = i.split(",")
                list_of_i.pop(9)
                exccess_removed.write(",".join(list_of_i[:14]) + "\n")

    os.remove(f"Only connected {legacy_switch_name}.txt")

def formatter():
    global legacy_switch_name

    with open(f"Excess Data removed {legacy_switch_name}.txt") as exccess_removed:
        with open(f"Formatted {legacy_switch_name}.txt", "w") as formatted:
            for i in exccess_removed:
                list_of_i = i.split(",")

                list_of_i.insert(1,"")

                for i in range(7):
                    list_of_i.insert(3,"")

                list_of_i.insert(10,"")
                list_of_i.insert(15,"")
                list_of_i.pop(19)
                list_of_i.pop(19)

                formatted.write(",".join(list_of_i))

    os.remove(f"Excess Data removed {legacy_switch_name}.txt")

def data_adder(legacy_ip, new_switch, new_ip):
    global legacy_switch_name
    global ap_mac

    with open(f"Formatted {legacy_switch_name}.txt") as formatted:
        with open(f"Finished {legacy_switch_name}.txt", "w") as final_data:
            for i in formatted:
                list_of_i = i.split(",")
                
                match_data = is_there_a_match(legacy_switch_name, list_of_i)

                matches = match_data[0]
                match_count = match_data[1]

                if match_count > 0:
                    for i in range(match_count):
                        formatted.readline()

                if match_count == 0:
                    list_of_i.insert(1,legacy_ip)
                    list_of_i.pop(2)

                    list_of_i.insert(4,new_switch)
                    list_of_i.pop(5)

                    list_of_i.insert(5,new_ip)
                    list_of_i.pop(6)

                    if "(*)" in list_of_i[14]:
                            parentasisesRemover = list_of_i[14].find("(")
                            list_of_i.insert(15,str(list_of_i[14][:parentasisesRemover]))
                            list_of_i.pop(14)
                            list_of_i.insert(14,"")
                            list_of_i.pop(16)
                            
                    if list_of_i[17][:8] in ap_mac:
                        list_of_i.insert(7,"Purple")
                        list_of_i.pop(8)
                        final_data.write(",".join(list_of_i))
                        continue
                            

                    if "KRONOS" in i or "UKG" in i:
                        list_of_i.insert(7,"Yellow")
                        list_of_i.pop(8)   
                        final_data.write(",".join(list_of_i)) 
                        continue        

                    else:
                        list_of_i.insert(7,"Blue")
                        list_of_i.pop(8)
                        final_data.write(",".join(list_of_i))
                        continue


                if match_count == 1:
                    if "Hewlett Packard" or "Dell Inc" in matches:
                        phone_lap = matches[0]

                        phone_lap.insert(1,legacy_ip)
                        phone_lap.pop(2)

                        phone_lap.insert(4,new_switch)
                        phone_lap.pop(5)

                        phone_lap.insert(5,new_ip)
                        phone_lap.pop(6)

                        if phone_lap[7] == "":
                            if "KRONOS" in phone_lap or "UKG" in phone_lap or "KRONOS" in matches[1][7] or "UKG" in matches[1][7]:
                                phone_lap.insert(7,"Yellow")
                                phone_lap.pop(8)  

                            if phone_lap[17][:8] in ap_mac or matches[1][16][:8] in ap_mac or matches[1][17][:8] in ap_mac:
                                phone_lap.insert(7,"Purple")
                                phone_lap.pop(8)   

                            else:
                                phone_lap.insert(7,"Blue")
                                phone_lap.pop(8)

                        if "(" in matches[1][14]:
                            parentasisesRemover = matches[1][14].find("(")
                            phone_lap.insert(15, matches[1][14][:parentasisesRemover])
                            phone_lap.pop(16)
                        else:
                            phone_lap.insert(15, matches[1][14])
                            phone_lap.pop(16)

                        phone_lap.append(matches[1][17])
                        phone_lap.append(matches[1][18])
                        phone_lap.append(matches[1][19])

                        newlinechr = list(phone_lap[21])
                        newlinechr.pop(-1)

                        phone_lap.insert(21, "".join(newlinechr))
                        phone_lap.pop(22)
                        final_data.write(",".join(phone_lap)+"\n")
                    continue

                if match_count > 1:
                    main_row = matches[0]
                    count = 0

                    main_row.insert(1,legacy_ip)
                    main_row.pop(2)

                    main_row.insert(4,new_switch)
                    main_row.pop(5)

                    main_row.insert(5,new_ip)
                    main_row.pop(6)

                    if main_row[7] == "":
                        if "KRONOS" in main_row or "UKG" in main_row:
                            main_row.insert(7,"Yellow")
                            main_row.pop(8)   

                        if "c8:4c:75" in main_row:
                            main_row.insert(7,"Purple")
                            main_row.pop(8)   

                        else:
                            main_row.insert(7,"Blue")
                            main_row.pop(8)

                    parentasisesRemover = matches[1][14].find("(")
                    if "(" in matches[1][14]:
                        main_row.insert(15, matches[1][14][:parentasisesRemover])
                        main_row.pop(16)
                    else:
                        main_row.insert(15, matches[1][14])
                        main_row.pop(16)

                    for i in matches:
                        if i != main_row:
                            count += 1
                            main_row.append(matches[count][17])
                            main_row.append(matches[count][18])
                            main_row.append(matches[count][19])
                            
                    for i in main_row:
                        if "\n" in i:
                            test = list(i[:21])
                            test.pop(-1)
                            main_row.insert(21,"".join(test))

                            main_row.pop(22)

                    final_data.write(",".join(main_row)+"\n")


    os.remove(f"Formatted {legacy_switch_name}.txt")

def is_there_a_match(legacy_switch_name, list_of_i):
    with open(f"Formatted {legacy_switch_name}.txt") as match_finder:

        matches = []
        match_count = 0

        for k in match_finder:
            list_of_k = k.split(",")

            if list_of_k[2] == list_of_i[2] and list_of_k != list_of_i:
                match_count += 1
                if list_of_i not in matches:
                    matches.append(list_of_i)
                matches.append(list_of_k)
                    
        return match_organizer(matches), match_count

def match_organizer(matches):
    pcs = []
    phones = []
    other = []
    total_matches = []

    for i in matches:
        if "Hewlett Packard" in i:
            pcs.append(i)
            continue

        if  "Dell Inc" in i:
            pcs.append(i)
            continue

        if "Cisco Systems Inc" in i:
            phones.append(i)
            continue
        else:
            other.append(i)

    total_matches = pcs + phones + other
    
    return total_matches

def access_vlan_finder():
    with open(f"Finished {legacy_switch_name}.txt") as all_data:
        vlans = {}
        access_vlan_counts = 0
        for i in all_data:
            list_of_i = i.split(",")
            if list_of_i[14] not in vlans and list_of_i[14].isnumeric():
                vlans[list_of_i[14]] = 1
                continue

            if list_of_i[14] in vlans:
                vlans[list_of_i[14]] += 1

        all_data.close()
        
        for i in vlans.items():
            if int(i[1]) > int(access_vlan_counts):
                access_vlan_counts = i[1]
                access_vlan = i[0]

    with open(f"Finished {legacy_switch_name}.txt") as all_data:
        with open(f"vlan added {legacy_switch_name}.txt", "w") as vlan_added:    
            
            for i in all_data:
                list_of_i = i.split(",")

                if list_of_i[14] == "":

                    list_of_i.insert(14,access_vlan)
                    list_of_i.pop(15)

                vlan_added.write(",".join(list_of_i))

def mac_and_ip_2():
    global header

    with open(f"vlan added {legacy_switch_name}.txt") as vlan_filled:
        longest = 0
        header_addition = ""
        count = 1

        for i in vlan_filled:
            list_of_i = i.split(",")
            if len(list_of_i) > longest:
                longest = len(list_of_i)

        vlan_filled.close()

        longest = longest - 22
        header_count = int((longest/3)+1)

        for i in range(header_count):
            if i == 1:
                header_addition = f",Mac Address {count},IP Address {count},Vendor {count}"
            
            else:
                header_addition += f",Mac Address {count},IP Address {count},Vendor {count}"
            count += 1
        header = header + header_addition

    with open(f"vlan added {legacy_switch_name}.txt") as vlan_filled:
        with open(f"Finished cutsheet {legacy_switch_name}.csv", "w") as header_adder:

            header_adder.write(str(header) + "\n")

            for i in vlan_filled:
                header_adder.write(i)
    
    os.remove(f"Finished {legacy_switch_name}.txt")
    os.remove(f"vlan added {legacy_switch_name}.txt")
    return 1


def max_port_finder(wap_file, file_name, switch_count):
    with open(wap_file) as wireless_ap_count:
        with open(file_name) as idf_matcher:
            idf_matcher.readline()
            match = idf_matcher.readline()
            ap_count = 0

            for i in wireless_ap_count:
                list_of_i = i.split(",")
                list_of_match = match.split(",")
                if list_of_i[7] in list_of_match[4] and list_of_i[7] != "":
                    if list_of_i[8] in list_of_match[4] and list_of_i[8] != "":
                        ap_count += 1

            if int(switch_count) == 1:
                total_ports = 96 - ap_count
                return round(total_ports/2)-3
            
            elif int(switch_count) > 1:
                total_ports = (96*int(switch_count)) - ap_count
                return round(total_ports/(2*int(switch_count)))-3

def port_data_adder(file_name, port_file_name,switch_details,max_port):
    with open(file_name) as python_made_data:
        with open(f"Finished Cutsheet.txt", "w") as Cutsheet:    
            switch_1_count = 0
            switch_1_blade_count = 1

            switch_2_count = 0
            switch_2_blade_count = 1

            switch_count = 0

            for i in python_made_data:
                with open(port_file_name) as patch_panel:

                    list_of_i = i.split(",")

                    for k in patch_panel:
                        list_of_k = k.split(",")

                        if list_of_k[1] == list_of_i[2] and list_of_i[3] == "":

                            if "as-" in list_of_k[5].lower():
                                switch_num = "Switch " + list_of_k[5][list_of_k[5].find("AS-".lower())]

                            else:
                                switch_count += 1
                                if switch_count % 2 == 0:                   
                                    switch_num = f"Switch 2"

                                else:
                                    switch_num = f"switch 1"

                            list_of_i.insert(9,switch_num)
                            list_of_i.pop(10)
                            
                            if "b" in list_of_k[5].lower():
                                if list_of_k[5].find("AS".lower()) > list_of_k[5].find("B".lower()):
                                    blade_num = list_of_k[5][list_of_k[5].find("B".lower()):list_of_k[5].find("AS".lower())]

                                elif list_of_k[5].find("AS".upper()) > list_of_k[5].find("B".lower()):
                                    blade_num = list_of_k[5][list_of_k[5].find("B".lower()):list_of_k[5].find("AS".upper())]

                                else:
                                    blade_num = list_of_k[5][list_of_k[5].find("B".lower()):]

                            elif list_of_k[5] == "" or "b" not in list_of_k[5]:
                                
                                if len(switch_details) == 1:                                        
                                        if switch_num[-1] == "1":
                                            switch_1_count += 1

                                            if switch_1_count == max_port:
                                                switch_1_blade_count += 1
                                                switch_1_count = 0
                                                                    
                                                if switch_details[0].switch_model == "9407" and switch_1_blade_count == 3:
                                                    switch_1_blade_count = 5

                                                elif switch_details[0].switch_model == "9410" and switch_1_blade_count == 4:
                                                    switch_1_blade_count = 7

                                            blade_num = f"Blade {switch_1_blade_count}"

                                elif len(switch_details) > 1:
                                    
                                    if switch_num[-1] == "1":
                                        switch_1_count += 1

                                        if switch_1_count == max_port:
                                            switch_1_blade_count += 1
                                            switch_1_count = 0

                                            if switch_details[0].switch_model == "9407" and switch_1_blade_count == 3:
                                                switch_1_blade_count = 5                                    

                                            elif switch_details[0].switch_model == "9410" and switch_1_blade_count == 5:
                                                switch_1_blade_count = 7
                                        
                                        blade_num = f"Blade {switch_1_blade_count}"
                                

                                    elif switch_num[-1] == "2":
                                        switch_2_count += 1

                                        fixed_switch_name = list_of_i[4][:-1] + "2"
                                        list_of_i.insert(4,fixed_switch_name)
                                        list_of_i.pop(5)

                                        if switch_2_count == max_port:
                                            switch_2_blade_count += 1
                                            switch_2_count = 0

                                            if switch_details[1].switch_model == "9407" and switch_2_blade_count == 3:
                                                switch_2_blade_count = 5

                                            elif switch_details[1].switch_model == "9410" and switch_2_blade_count == 5:
                                                switch_2_blade_count = 7

                                        blade_num = f"Blade {switch_2_blade_count}"

                                    else:
                                        blade_num = "n/a"

                            list_of_i.insert(10,blade_num)
                            list_of_i.pop(11)

                            list_of_i.insert(3,list_of_k[2])
                            list_of_i.pop(4)

                            if list_of_i[9][7] != 1:
                                new_host_name = list_of_i[4][:-1] + list_of_i[9][7]
                                list_of_i.insert(4,new_host_name)
                                list_of_i.pop(5)



                Cutsheet.write(",".join(list_of_i))
        
def legacy_ap_count(switch_details, max_port):
    with open(f"Finished Cutsheet.txt") as ap_finder:
        blade_count = {int(i+1):[1,1] for i in range(len(switch_details))}

        for k in ap_finder:
            list_of_k = k.split(",")

            if "Purple" in list_of_k[7]:
                if blade_count[int(list_of_k[9][-1])][1] == max_port:
                    blade_count[int(list_of_k[9][-1])][0] += 1
                    blade_count[int(list_of_k[9][-1])][1] == 1

                else:
                    switch_details[int(list_of_k[9][-1])-1].filled_blades[blade_count[int(list_of_k[9][-1])][0]] += 1
                    blade_count[int(list_of_k[9][-1])][1] += 1

        return switch_details, blade_count
        
def new_switch_port_adder(switch_details,max_port):
    global legacy_switch_name

    with open(f"{legacy_switch_name} cutsheet.csv", "w") as final_cutsheet:
        with open(f"Finished Cutsheet.txt") as cutsheet_w_patchpanel_info:

            final_cutsheet.write(cutsheet_w_patchpanel_info.readline()) 
            ap_data = legacy_ap_count(switch_details, max_port)

            switch_details = ap_data[0]
            switch_blade_count = ap_data[1]

            ap_count = {int(i+1):[1,0] for i in range(len(switch_details))}

            for i in cutsheet_w_patchpanel_info:
                list_of_i = i.split(",")

                if list_of_i[6] == "":
                    if list_of_i[7] == "Purple":
                        if ap_count[int(list_of_i[9][7])][1] == max_port:
                            ap_count[int(list_of_i[9][7])][1] = 0
                            ap_count[int(list_of_i[9][7])][0] += 1

                        ap_count[int(list_of_i[9][7])][1] += 1

                        if switch_details[int(list_of_i[9][7])-1].switch_model == "9300":
                            if 36 >= ap_count[int(list_of_i[9][7])][1]:
                                list_of_i.insert(6,f"Tw{ap_count[int(list_of_i[9][7])][0]}/0/{ap_count[int(list_of_i[9][7])][1]}")
                                list_of_i.pop(7)

                            elif 36 < ap_count[int(list_of_i[9][7])][1]:
                                list_of_i.insert(6,f"Te{ap_count[int(list_of_i[9][7])][0]}/0/{ap_count[int(list_of_i[9][7])][1]}")
                                list_of_i.pop(7)

                        elif switch_details[int(list_of_i[9][7])-1].switch_model == "9407":
                            list_of_i.insert(6,f"Fi{ap_count[int(list_of_i[9][7])][0]}/0/{ap_count[int(list_of_i[9][7])][1]}")
                            list_of_i.pop(7)

                        elif switch_details[int(list_of_i[9][7])-1].switch_model == "9410":
                            list_of_i.insert(6,f"Fi{ap_count[int(list_of_i[9][7])][0]}/0/{ap_count[int(list_of_i[9][7])][1]}")
                            list_of_i.pop(7)

                        final_cutsheet.write(",".join(list_of_i))
                        continue
                
                    else:
                        if switch_blade_count[int(list_of_i[9][7])][0] not in switch_details[int(list_of_i[9][7])-1].filled_blades:
                            while switch_blade_count[int(list_of_i[9][7])][0] not in switch_details[int(list_of_i[9][7])-1].filled_blades:
                                switch_blade_count[int(list_of_i[9][7])][0] += 1

                        if switch_details[int(list_of_i[9][7])-1].filled_blades[switch_blade_count[int(list_of_i[9][7])][0]] == max_port:
                            switch_blade_count[int(list_of_i[9][7])][0] += 1
                            switch_blade_count[int(list_of_i[9][7])][1] = 1

                        if int(list_of_i[10][6]) != switch_blade_count[int(list_of_i[9][7])][0]:
                            if switch_details[int(list_of_i[9][7])-1].filled_blades[int(list_of_i[10][6])] == max_port:
                                continue
                            print(list_of_i)
                            print()

                            if switch_details[int(list_of_i[9][7])-1].switch_model == "9300":
                                if 36 >= switch_details[int(list_of_i[9][7])-1].filled_blades[int(list_of_i[10][6])]:
                                    list_of_i.insert(6,f"Tw{int(list_of_i[10][6])}/0/{switch_details[int(list_of_i[9][7])-1].filled_blades[int(list_of_i[10][6])]}")
                                    list_of_i.pop(7)

                                elif 36 < switch_details[int(list_of_i[9][7])-1].filled_blades[int(list_of_i[10][6])]:
                                    list_of_i.insert(6,f"Te{int(list_of_i[10][6])}/0/{switch_details[int(list_of_i[9][7])-1].filled_blades[int(list_of_i[10][6])]}")
                                    list_of_i.pop(7)

                            elif switch_details[int(list_of_i[9][7])-1].switch_model == "9407":
                                if 3 > int(list_of_i[10][6]):
                                    list_of_i.insert(6,f"Fi{int(list_of_i[10][6])}/0/{switch_details[int(list_of_i[9][7])-1].filled_blades[int(list_of_i[10][6])]}")
                                    list_of_i.pop(7)

                                elif int(list_of_i[10][6]) >= 5:
                                    list_of_i.insert(6,f"Gi{int(list_of_i[10][6])}/0/{switch_details[int(list_of_i[9][7])-1].filled_blades[int(list_of_i[10][6])]}")
                                    list_of_i.pop(7)

                            elif switch_details[int(list_of_i[9][7])-1].switch_model == "9410":
                                if 5 > int(list_of_i[10][6]):
                                    list_of_i.insert(6,f"Fi{int(list_of_i[10][6])}/0/{switch_details[int(list_of_i[9][7])-1].filled_blades[int(list_of_i[10][6])]}")
                                    list_of_i.pop(7)
                                    
                                elif int(list_of_i[10][6]) >= 7:
                                    list_of_i.insert(6,f"Gi{int(list_of_i[10][6])}/0/{switch_details[int(list_of_i[9][7])-1].filled_blades[int(list_of_i[10][6])]}")
                                    list_of_i.pop(7)

                            final_cutsheet.write(",".join(list_of_i))
                            switch_details[int(list_of_i[9][7])-1].filled_blades[int(list_of_i[10][6])] += 1
                            
                        else:
                            if switch_details[int(list_of_i[9][7])-1].switch_model == "9300":
                                if 36 >= switch_blade_count[int(list_of_i[9][7])][1]:
                                    list_of_i.insert(6,f"Tw{switch_blade_count[int(list_of_i[9][7])][0]}/0/{switch_blade_count[int(list_of_i[9][7])][1]}")
                                    list_of_i.pop(7)

                                elif 36 < switch_blade_count[int(list_of_i[9][7])][1]:
                                    list_of_i.insert(6,f"Te{switch_blade_count[int(list_of_i[9][7])][0]}/0/{switch_blade_count[int(list_of_i[9][7])][1]}")
                                    list_of_i.pop(7)

                            elif switch_details[int(list_of_i[9][7])-1].switch_model == "9407":
                                if 3 > switch_blade_count[int(list_of_i[9][7])][0]:
                                    list_of_i.insert(6,f"Fi{switch_blade_count[int(list_of_i[9][7])][0]}/0/{switch_blade_count[int(list_of_i[9][7])][1]}")
                                    list_of_i.pop(7)

                                elif switch_blade_count[int(list_of_i[9][7])][0] >=  5:
                                    list_of_i.insert(6,f"Gi{switch_blade_count[int(list_of_i[9][7])][0]}/0/{switch_blade_count[int(list_of_i[9][7])][1]}")
                                    list_of_i.pop(7)

                            elif switch_details[int(list_of_i[9][7])-1].switch_model == "9410":
                                if 5 > switch_blade_count[int(list_of_i[9][7])][0]:
                                    list_of_i.insert(6,f"Fi{switch_blade_count[int(list_of_i[9][7])][0]}/0/{switch_blade_count[int(list_of_i[9][7])][1]}")
                                    list_of_i.pop(7)
                                    
                                elif switch_blade_count[int(list_of_i[9][7])][0] >= 7:
                                    list_of_i.insert(6,f"Gi{switch_blade_count[int(list_of_i[9][7])][0]}/0/{switch_blade_count[int(list_of_i[9][7])][1]}")
                                    list_of_i.pop(7)

                            
                            final_cutsheet.write(",".join(list_of_i))
                            switch_details[int(list_of_i[9][7])-1].filled_blades[switch_blade_count[int(list_of_i[9][7])][0]] += 1
                            switch_blade_count[int(list_of_i[9][7])][1] += 1

    os.remove(f"Finished Cutsheet.txt")
                        
def list_of_switch_vlans(switch_details):
    global legacy_switch_name

    with open(f"{legacy_switch_name} cutsheet.csv") as finding_vlans:

        vlan_list = {i+1:[] for i in range(len(switch_details))}

        for i in finding_vlans:
            list_of_i = i.split(",")

            if list_of_i[4][int(-1)].isnumeric():
                switch_num = list_of_i[4][int(-1)]

                if list_of_i[14] not in vlan_list[int(switch_num)] and list_of_i[14].isnumeric():
                    vlan_list[int(switch_num)].append(list_of_i[14])

                if list_of_i[15] not in vlan_list[int(switch_num)] and list_of_i[15].isnumeric():
                    vlan_list[int(switch_num)].append(list_of_i[15])

        for i in vlan_list.keys():
            add_vlan_list = []
            for k in vlan_list[i]:
                add_vlan_list.append(f"vlan {k}")       

                if ap_vlan not in vlan_list[i]:
                    add_vlan_list.append(f"vlan {ap_vlan}")   
                    vlan_list[i].append(ap_vlan)
        
            vlan_list[i]=add_vlan_list

        return vlan_list

def new_switch_name_finder():
    global legacy_switch_name

    with open(f"{legacy_switch_name} cutsheet.csv") as cutsheet:
        switch_names = []

        for i in cutsheet:
            list_of_i = i.split(",")
            if list_of_i[4] not in switch_names and list_of_i[4][int(-1)].isnumeric():
                switch_names.append(list_of_i[4])

        return switch_names

def idf_config(site_vlans,switch_details):
    global legacy_switch_name
    global new_switch_name

    vlan_dict = list_of_switch_vlans(switch_details)
    new_switch_name = new_switch_name_finder()

    switch_list = [i+1 for i in range(len(switch_details))]
    vlan_dict_remoover = vlan_dict.copy()

    for j in range(len(switch_details)):
        switch_list[j] = open(f"{new_switch_name[j]} switchport config.txt","w")
        switch_list[j].write(f"conf t\n!\n")

        with open(site_vlans) as switch_vlans:

            for i in switch_vlans:
                vlan = i[:i.find("\"")].lower()

                if vlan in vlan_dict[j+1]:
                    with open(site_vlans) as vlan_name_finder:

                        for k in vlan_name_finder:
                            if k[:i.find("\"")].lower() == vlan and vlan in vlan_dict_remoover[j+1]:
                                vlan_descr = vlan_name_finder.readline()
                                switch_list[j].write(f"{vlan}\n{vlan_descr.lower()}!\n")
                                vlan_dict_remoover[j+1].remove(vlan)
                        vlan_name_finder.close()
                        
        switch_vlans.close()
        
        with open(f"{legacy_switch_name} cutsheet.csv") as switchport_vlans:
            for p in switchport_vlans:
                list_of_p = p.split(',')

                if list_of_p[4][int(-1)].isnumeric():
                    if int(list_of_p[4][int(-1)])-1 == j:

                        if list_of_p[15] != "" and list_of_p[6][-1].isnumeric():
                            switch_list[j].write(f"interface {list_of_p[6]}\nswitchport access vlan {list_of_p[14]}\nswitchport voice vlan {list_of_p[15]}\n!\n")
                            
                        elif list_of_p[15] == "":
                            switch_list[j].write(f"interface {list_of_p[6]}\nswitchport accesss vlan {list_of_p[14]}\n!\n")
            switchport_vlans.close()

def wap_sheet(file_name,wap_file,switch_details):
    global legacy_switch_name

    with open(wap_file) as wap_data:
        with open(file_name) as cutsheet:
            with open(f"wap cutsheet {legacy_switch_name}.csv","w") as wap_cutsheet:
                global ap_vlan
                
                cutsheet.readline()
                match = cutsheet.readline()
                wap_cutsheet.write("PP Port,New Switch name,New Switch Port,New Patch Cord Color,Speed,Duplex,New Access Vlan,New Port Description,Mac Address,IP Address,Hostname,Serial Number,Asset Tag,Model\n")
            
                ap_swapper_count = {int(i+1):{1:[48,0],2:[48,0],3:[1,0]} for i in range(len(switch_details))}
                switch_count = 1

                for i in wap_data:
                    list_of_i = i.split(",")
                    list_of_match = match.split(",")
                
                    if list_of_i[7] in list_of_match[4] and list_of_i[7] != "":
                        if list_of_i[8] in list_of_match[4] and list_of_i[8] != "":

                            if "vlan" in list_of_i[18]:
                                ap_vlan = f"{list_of_i[18][:list_of_i[18].find('n')+1]} {list_of_i[18][list_of_i[18].find('n')+1:-1]}"

                            if ap_swapper_count[switch_count][3][1] == 2:
                                ap_swapper_count[switch_count][3][0] += 1

                            if ap_swapper_count[switch_count][3][1] == 4:
                                ap_swapper_count[switch_count][3][1] = 0
                                ap_swapper_count[switch_count][3][0] = 1
                                switch_count += 1

                                if switch_count > len(switch_details):
                                    switch_count = 1
                            
                            new_switch_port = f"Fi{ap_swapper_count[switch_count][3][0]}/0/{ap_swapper_count[switch_count][ap_swapper_count[switch_count][3][0]][0]}"
                            ap_swapper_count[switch_count][3][1] += 1
                            ap_swapper_count[switch_count][ap_swapper_count[switch_count][3][0]][0] -= 1                            
                            
                            formatted_ap_info = f'{list_of_i[15]},{list_of_match[4][:-1]}{switch_count},{new_switch_port},purple,a-5000,a-full,{ap_vlan},AP={list_of_i[3]} SN={list_of_i[11]} HW=C9130AXI-B,{list_of_i[10]},DHCP,{list_of_i[3]},{list_of_i[11]},{list_of_i[12]},C9130AXI-B\n'
                            wap_cutsheet.write(formatted_ap_info)
                            
def add_wap_to_idf(switch_details):
    global legacy_switch_name
    global new_switch_name

    for i in range(len(switch_details)):
        with open(f"{new_switch_name[i]} switchport config.txt","a") as idf_config:
            with open(f"wap cutsheet {legacy_switch_name}.csv","r") as wap_cutsheet:
                wap_cutsheet.readline()

                for k in wap_cutsheet:
                    list_of_k = k.split(",")
                    if list_of_k[1] == new_switch_name[i]:
                        idf_config.write(f"interface {list_of_k[2]}\nswitchport access {list_of_k[6]}\n!\n")
