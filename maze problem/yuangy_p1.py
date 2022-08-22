import re
game_file = open("game1.txt","r")
map = {}
object = []
game_infor = {}
inv = []
npc = {}
word_number = 1

# read each line in txt files
for line in game_file:
    if '---' in line:
        continue
    # remove underlina and enter key
    else:
        line = line.rstrip('\n')
        infor = line.split('_')

        # create a game information dictionary
        if 'game' in infor[0]:
            g = infor[1]
            game_set = infor[1].split(':')   # split words on colon
            information = game_set[1].strip()
            game_infor.setdefault(game_set[0],information)

        # create a npc information dictionary
        elif 'npc' in infor[0]:
            npc_name = infor[1]

            npc_set = infor[2].split(':')    # split words on colon
            if 'loc' in npc_set[0]:
                npc_dict = {}
                location_number = npc_set[1].strip()
                npc_dict['name'] = npc_name
                npc_dict['loc'] = location_number
                npc.setdefault(location_number, npc_dict)  # attach npc name into npc dictionary
            else:
                for word_number in npc_set[0]:
                    npc_words = npc_set[1].strip()
                    npc_dict[str(word_number)] = npc_words

        # create a map
        else:
            r = infor[1].split(':')

            if r[0].startswith('id'):

                # screen ID number
                round_content = {}
                id_number = r[1]
                round_content.setdefault(r[0],id_number)
                round_content['obj'] = []
                map.setdefault(id_number, round_content)

            # add description into map
            elif 'desc' in r[0]:
                description = r[1].lstrip()
                round_content['desc'] = description

            # use startswith to distinguish object and hiddenobject
            # and add obj into map
            elif r[0].startswith('obj'):
                obj = r[1].strip()
                object.append(obj)
                round_content['obj'] = [obj]

            # add hiddenobj into map
            elif 'hiddenobj' in r[0]:
                hiddenobj = r[1].lstrip()
                round_content['hiddenobj'] = hiddenobj

            #add hiddenpath into map
            elif 'hiddenpath' in r[0]:
                hiddenpath = r[1].lstrip()
                round_content['hiddenpath'] = hiddenpath

            # some places they have south direction and add south into map
            elif 'south' in r[0]:
                south = r[1].lstrip()
                round_content['south'] = south

            # some places they have east direction and add east into map
            elif 'east' in r[0]:
                east = r[1].lstrip()
                round_content['east'] = east

            # some places they have west direction and add west into map
            elif 'west' in r[0]:
                west = r[1].lstrip()
                round_content['west'] = west
# print(game_infor)
# print(map)

# ---------------------------------------------
# implement game


loca_number = 0
found_path = False
talk_times = 1
npc_is_here = False

# At the begin of game, it will show the information about this game
print('Welcome to', game_infor['name'])
print()
print('The goal of this game is to:')
print(game_infor['goal'])
print()

# locate the start locaiton
loca_number = game_infor['start']
total_size = int(game_infor['xsize'])* int(game_infor['ysize'])

# use while true to loop each command
while True:

    # get goal
    if loca_number == game_infor['goalloc']:
        if game_infor['goalobj'] in map[loca_number]['obj']:

            #  when users achieve the goal, break the game
            print()
            print("Congratulations! You have won the game.")
            break
        else:
            pass

    print('You are on', map[loca_number]['desc'])

    # list object
    if 'obj' in map[loca_number]:
        if len(map[loca_number]['obj']) == 0:
            pass
        else:
            for i in map[loca_number]['obj']:
                object_name = i
                print('There is a', object_name)

    # if already found hiddenpath
    if 'hiddenpath' in map[loca_number]:
        if found_path == True:
            print('There is a hiddenpath')
        else:
            pass


    # list npc
    if loca_number in npc:
        n_name = npc[str(loca_number)]['name']
        print(n_name + ' is here. You can talk with him/her')
        npc_is_here = True


    # input command
    next_step = input('What Next?')

     # exit
    if next_step.lower() == 'exit':
        break

     # direction, walk in the map
     # go north
    elif next_step.lower().strip() in ['move north', 'go north', 'north']:
        int_loca_number = int(loca_number) - int(game_infor['xsize'])

        # if user at top location of this game and want to continue go north
        if int_loca_number <= 0:
            int_loca_number = int_loca_number + total_size
            loca_number = str(int_loca_number)
            print()

        # else just go north
        else:
            loca_number = str(int_loca_number)
            print()

     # go south
    elif next_step.lower().strip() in ['move south', 'go south', 'south']:

        # screen special id
        special_south = 'south'
        special_id_list = []

        # there is special location that when user enter south, it will go to the specific location.
        # find those special locations
        for i in range(1, total_size + 1):
            if special_south in map[str(i)]:
                special_id = str(i)
                special_id_list.append(special_id)
            else:
                continue

        # when user in the special location and enter south, it will execute the specific command
        if loca_number in special_id_list:
            loca_number = map[loca_number]['south']
            print()

        # when user not in the special location
        else:
            int_loca_number = int(loca_number) + int(game_infor['xsize'])

            # if user in the bottom of games and want to continue go south
            if int_loca_number > total_size:
                int_loca_number = int_loca_number - total_size
                loca_number = str(int_loca_number)
                print()

            # just go south
            else:
                loca_number = str(int_loca_number)
                print()

    # go west
    elif next_step.lower().strip() in ['move west', 'go west', 'west']:
        x_range = []
        for i in range(0, total_size + 1):
            x_range.append(int(game_infor['xsize']) * i)

        # screen special id
        # there is special location that when user enter west, it will go to the specific location.
        special_west = 'west'
        special_id_list = []
        for i in range(1, total_size + 1):
            if special_west in map[str(i)]:
                special_id = str(i)
                special_id_list.append(special_id)
            else:
                continue

        if loca_number in special_id_list:
            loca_number = map[loca_number]['west']
            print()

        else:
            int_loca_number = int(loca_number) - 1

            # if user at left end of this game and want to continue go west
            if int_loca_number in x_range:
                int_loca_number = int_loca_number + int(game_infor['xsize'])
                loca_number = str(int_loca_number)
                print()

            # just go west
            else:
                loca_number = str(int_loca_number)
                print()

    # east
    elif next_step.lower().strip() in ['move east', 'go east', 'east']:
        x_range = []
        for i in range(0, total_size + 1):
            x_range.append(int(game_infor['xsize']) * i)

        # screen special id
        # there is special location that when user enter east, it will go to the specific location.
        special_east = 'east'
        special_id_list = []
        for i in range(1, total_size + 1):
            if special_east in map[str(i)]:
                special_id = str(i)
                special_id_list.append(special_id)
            else:
                continue

        if loca_number in special_id_list:
            loca_number = map[loca_number]['east']
            print()

        else:
            if int(loca_number) in x_range:

                # if user at left end in game and want to continue go east
                int_loca_number = int_loca_number + 1 - int(game_infor['xsize'])
                loca_number = str(int_loca_number)
                print()

            # just go east
            else:
                int_loca_number = int(loca_number) + 1
                loca_number = str(int_loca_number)
                print()

    # go hiddenpath
    elif next_step.lower().strip() in ['move path', 'go path', 'path','hiddenpath', 'go hiddenpath', 'move hiddenpath']:
        special_path = 'hiddenpath'
        special_id_list = []

        # find out those location which have hiddenpath
        for i in range(1, total_size + 1):
            if special_path in map[str(i)]:
                special_id = str(i)
                special_id_list.append(special_id)
            else:
                continue

        # if user already found the hiddenpath,
        # it will print the information about hiddenpath when the user arrive this location again
        if loca_number in special_id_list:
            if found_path == True:
                loca_number = map[loca_number]['hiddenpath']
                print()

        # if user dose not find hiddenpath, but enter go hiddenpath
            else:
                print("No hiddenpath found")
                print()

# ---------------------------------------------
# action in the game
    # search
    elif next_step.lower().strip() == 'search':

        # search hiddenpath
        if 'hiddenpath' in map[loca_number]:
            found_path = True
            print()
            print('You found a hiddenpath')
            print()

        # search hiddenobject
        elif 'hiddenobj' in map[loca_number]:
            print()
            object_name = map[loca_number]['hiddenobj']
            print('You found a', map[loca_number]['hiddenobj'])
            print()

        # when there is no hidden things, but user enter search
        else:
            print('Nothing find')
            print()

    #take object
    elif next_step.lower().strip().startswith("take"):

        # check there is two words in the command
        if len(next_step.lower().split()) == 2:

            # object name is behind the word 'take'
            object_name = next_step.split()[1]
            if next_step.lower().strip() == ('take' + ' ' + object_name):

                # if object name fit the object name in the locaiton
                if object_name == object_name:

                    if object_name in map[loca_number]['obj']:
                        inv.append(object_name)
                        map[loca_number]['obj'].remove(object_name)
                        print()


                    elif 'hiddenobj' in map[loca_number]:

                        # if user find hidden object, and want to take it
                        if object_name in map[loca_number]['hiddenobj']:
                            inv.append(object_name)
                            map[loca_number].pop('hiddenobj')
                            print()

                        # if user dose not find hidden object but take it
                        else:
                            print('That object is not here.')
                            print()

                    else:
                        print('That object is not here.')
                        print()
                else:
                    print('That object is not here.')
                    print()
        else:
            print("Please enter object name")
            print()

    # check inventory
    elif next_step.lower().strip() in ['inv', 'inventory']:
        print(inv)
        print()

    #drop
    elif next_step.lower().strip().startswith("drop"):

        # check there is object behind the word 'drop'
        if len(next_step.lower().split()) == 2:
            inv_object_name = next_step.split()[1]
            if next_step.lower().strip() == ('drop' + ' ' + inv_object_name):

                # check the object is in the inventory list
                if inv_object_name in inv:
                    map[loca_number]['obj'].append(inv_object_name)
                    inv.remove(inv_object_name)
                    print()
                else:
                    print('The object is not in inventory')
                    print()
        else:
            print("Please enter object name")
            print()

    # goal
    elif next_step.lower().strip() == 'goal':
        print()
        print("The goal of this game is to: ")
        print(game_infor['goal'])
        print()

    # talk
    elif next_step.lower().strip().startswith("talk"):

        # check is there a person's name behind the word 'talk'
        if len(next_step.lower().split()) == 2:
            interact_npc_name = next_step.split()[1]

            # if the npc is in that location
            if npc_is_here == True:
                if interact_npc_name == n_name:
                    if str(talk_times) in npc[loca_number]:
                        print(npc[loca_number][str(talk_times)])
                        print()

                        # because each npc can speak two or more sentences
                        # print each sentence after user enter talk to the ncp each time
                        talk_times += 1

                        # if npc talked all sentences, it will return to the first sentence
                        if str(talk_times) not in npc[loca_number]:
                            talk_times = 1
                else:
                    print('Could not find this people')
                    print()

            else:
                print('There is no people')
                print()
        else:
            print('please enter the name you want to talk to')
            print()


     # wrong input and ask user enter again
    else:
        print('Please enter valid information!')
        print()

# ---------------------------------------------













