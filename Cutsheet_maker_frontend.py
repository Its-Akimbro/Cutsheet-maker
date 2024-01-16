import os
import Cutsheet_maker_backend_Ne as backend

user_choices = ["1","2","3","4","5"]
user_exits = ["exit","end","no","quit","stop",] 
possible_switch_count = ["1","2","3"]
not_ava = ["na", "n/a"]

while True:

    userChoice = input("What do you want to do?\nIf you every want to return to this selection screen type 'exit' at any point.\n\nOption 1: Formats NetDB reports\nOption 2: Adds portmapping data to the Formatted NetDB reports, and builds the IDF config\nOption 5: End the program\n\nYour choice is ")
    print()

    if userChoice == "5" or userChoice in user_exits:
        exit()

    if userChoice not in user_choices:
        while True:
            userChoice = input("\nThat was not a valid choice. Choose 1, 2, or 3\nYour choice is ")
            if userChoice in user_choices:
                break

    if userChoice == "1":
        while True:
            file_name = input("\nWhat is the netDB file name? ").lower()
            print()
            
            if ".txt" not in file_name and file_name not in user_exits:
                file_name = f"{file_name}.txt"

            if os.path.isfile(file_name) == False and file_name not in user_exits:
                while True:
                    file_name = input("That is not a vaild file name\nWhat is the NetDB file name?\n\nYour choice is ").lower()
                    print()

                    if file_name in user_exits:
                        break

                    if ".txt" not in file_name:
                        file_name = f"{file_name}.txt"

                    if os.path.isfile(file_name) == True:
                        break

            if file_name in user_exits:
                break
                    
            legacy_ip = input("\nWhat is the legacy switches IP? ")
            if legacy_ip in user_exits:
                break

            new_ip = input("\nWhat is the new switches IP? ")
            if new_ip in user_exits:
                break
                
            new_switch = input("\nWhat is the new switches hostname? ")
            if new_switch in user_exits:
                break

            backend.legacy_switch_name_finder(file_name)
            backend.line_combiner(file_name)

            no_connections = backend.only_connected()

        
            if no_connections == 1:
                what_to_do = input("\nDo you want to try another file?\nEnter Y or N\nYour choice is ").lower()

                if what_to_do == "y" or what_to_do == "yes":
                    continue
                
                else:
                    continue

            else:
                backend.excess_data_removal()
                backend.formatter()
                backend.data_adder(legacy_ip, new_switch, new_ip)
                backend.access_vlan_finder()
                finished = backend.mac_and_ip_2()

                if finished == 1:
                    yes_or_no = input("\nThe Cutsheet is formatted, The program ran successfully\nDo you want to format another file Y/N\nYour choice is ").lower()
                    print()

                    if yes_or_no == "y" or yes_or_no == "yes":
                        continue
                    
                    else:
                        userChoice = input("What do you want to do?\nOption 1: Formats NetDB reports\nOption 2: Adds portmapping data to the Formatted NetDB reports, and builds the IDF config\n\nYour choice is ")
                        print()
                        continue
    
    if userChoice == "2":
        while True:
            switch_details = []

            file_name = input("What is the formatted NetDB file name?\nYour choice is ").lower()
            print()
            
            if ".csv" not in file_name and file_name not in user_exits:
                file_name = f"{file_name}.csv"

            if os.path.isfile(file_name) == False and file_name not in user_exits:
                while True:
                    file_name = input("That is not a vaild file name\nWhat is the formatted NetDB file name?\n\nYour choice is ").lower()
                    print()

                    if file_name in user_exits:
                        break

                    if ".csv" not in file_name:
                        file_name = f"{file_name}.csv"

                    if os.path.isfile(file_name) == True:
                        break

            if file_name in user_exits:
                break
                
                    
            switch_count = input("How many new switches are in the IDF/MDF, 1 - 3?\nYour choice is ")
            print()
            
            if switch_count.isnumeric() == False and switch_count not in possible_switch_count and switch_count not in user_exits:
                while True:
                    switch_count = input("Thats not a valid switch count please choose 1 - 3\nHow many new switches are in the IDF/MDF, 1 - 3?\n\nYour choice is ")
                    print()
                    
                    if switch_count in user_exits:
                        break

                    if switch_count.isnumeric() and switch_count == "1" or switch_count == "2" or switch_count == "3":
                        break
        
            if switch_count in user_exits:
                break

            patch_panel_file = input("What is the portmapping file name?\nYour choice is ").lower()
            print()
            
            if ".csv" not in patch_panel_file and patch_panel_file not in user_exits:
                patch_panel_file = f"{patch_panel_file}.csv"
            
            if os.path.isfile(patch_panel_file) == False and patch_panel_file not in user_exits:
                while True:
                    patch_panel_file = input("That is not a vaild file name\nWhat is the portmapping file name?\n\nYour choice is ").lower()
                    print()

                    if patch_panel_file in user_exits:
                        break

                    if ".csv" not in patch_panel_file:
                        patch_panel_file = f"{patch_panel_file}.csv"

                    if os.path.isfile(patch_panel_file) == True:
                        break

            if patch_panel_file in user_exits:
                break

            site_vlans = input("What is the Vlan List file name?\nIf you don't have the file input n/a\nYour choice is ").lower()
            print()
            
            if site_vlans not in not_ava and site_vlans not in user_exits:
                site_vlans = f"{site_vlans}.txt"

            if os.path.isfile(site_vlans) == False and site_vlans not in not_ava and site_vlans not in user_exits:
                while True:
                    site_vlans = input("That is not a vaild file name\nWhat is the Vlan List file name?\nIf you don't have the file input n/a\n\nYour choice is ").lower()
                    print()

                    if site_vlans in user_exits:
                        break

                    if ".txt" not in site_vlans:
                        site_vlans = f"{site_vlans}.txt"

                    if os.path.isfile(site_vlans) == True:
                        break

            if site_vlans in user_exits:
                break

            wap_file = input("What is the WAP file name?\nIf you don't have the file input n/a.\n\nYour choice is ").lower()
            print()

            if wap_file not in not_ava and wap_file not in user_exits:
                wap_file = f"{wap_file}.txt"

            if os.path.isfile(wap_file) == False and wap_file not in not_ava and wap_file not in user_exits:
                while True:
                    wap_file = input("That is not a vaild file name\nWhat is the WAP file name?\nIf you don't have the file input n/a.\n\nYour choice is ").lower()
                    print()

                    if wap_file in user_exits:
                        break

                    if ".txt" not in wap_file:
                        wap_file = f"{wap_file}.txt"

                    if os.path.isfile(wap_file) == True:
                        break

            if wap_file in user_exits:
                break

            if int(switch_count) > 1:
                for i in range(int(switch_count)):
                    switch_model = input(f"What is the model of switch {i+1}? ")
                    print()

                    if switch_model == "9410":
                        filled_blades_input = input("What blades are filled in the 9410?\nExample 1,2,7,8 are filled\nYour input is  ")

                    if switch_model == "9407":
                        filled_blades_input = input("What blades are filled in the 9407?\nExample 1,2,5,6 are filled\nYour input is  ")

                    if switch_model == "9300":
                        filled_blades_input = input("How many switchs are in the stack of 9300?\nExample 1,2,3 are filled\nYour input is  ")

                    filled_blades = {int(i):1 for i in filled_blades_input.split(",") if i.isnumeric()}
                    switch = backend.new_switch(switch_model,filled_blades)
                    switch_details.append(switch)

            else:
                switch_model = input(f"What is the model of switch? ")
                print()
                    
                if switch_model == "9410":
                    filled_blades_input = input("What blades are filled in the 9410?\nExample 1,2,7,8 are filled\nYour input is  ")

                if switch_model == "9407":
                    filled_blades_input = input("What blades are filled in the 9407?\nExample 1,2,5,6 are filled\nYour input is  ")

                if switch_model == "9300":
                    filled_blades_input = input("How many switchs are in the stack of 9300?\nExample 1,2,3 are filled\nYour input is  ")

                filled_blades = {int(i):1 for i in filled_blades_input.split(",") if i.isnumeric()}
                switch = backend.new_switch(switch_model,filled_blades)
                switch_details.append(switch)

            if "n/a" in wap_file or "na" in wap_file:
                max_port = 30
            else:
                max_port = backend.max_port_finder(wap_file, file_name, switch_count)

            backend.legacy_switch_name_finder(file_name)
            backend.port_data_adder(file_name, patch_panel_file, switch_details, max_port)
            backend.new_switch_port_adder(switch_details,max_port)

            if "n/a" in site_vlans or "na" in site_vlans:
                pass
            else:
                backend.idf_config(site_vlans,switch_details)

            if "n/a" in wap_file or "na" in wap_file:
                pass
            else:
                backend.wap_sheet(file_name,wap_file,switch_details)
            
            if "n/a" in site_vlans or "na" in site_vlans or "n/a" in wap_file or "na" in wap_file:
                pass
            else:
                backend.add_wap_to_idf(switch_details)

        