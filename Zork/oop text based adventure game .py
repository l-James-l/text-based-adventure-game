from cmd import Cmd
import random
import time

class Player:
    def __init__(self):
        self.health = 40
        self.max_hp = 100
        self.coins = 5
        self.items = []

class Room:
    def __init__(self,name, rooms, items, unlocked, enemies, extra=None):
        self.name = name
        self.rooms = rooms
        self.items = items
        self.unlocked = unlocked
        self.enemies = enemies
        self.extra_info = extra

class Enemie:
    def __init__(self, name, health, damage, hit_chance, dialog, prefix=""):
        self.name = name
        self.health = health
        self.damage = damage
        self.hit_chance = hit_chance
        self.dialog = dialog
        self.prefix = prefix

class Item:
    def __init__(self, name, prefix, used_for, message=None):
        self.name = name
        self.prefix = prefix
        self.used_for = used_for
        self.message = message
        
class Prompts(Cmd):

    def do_look(self, args):
        "this will tell you what room your in, whats in it and where you can go from there"
        look(current_room)
    def do_go(self,args):
        "this will move you in the direction you wirte afetr 'go' given that you can move in that direction"
        global current_room
        if len(current_room.enemies) == 0:
            current_room = go(current_room, args)
        else:
            print("you can't leave while there are enemies in the room")
        if current_room.name == "exit":
            print("you won!!")
            if easter_egg in player.items:
                print("and you founf the eater egg, what a gamer")
            return True
    def do_take(self,args):
        "this will take the item you specify from in the room and put it your items"
        if len(current_room.enemies) == 0:
            take(current_room, player, args)
        else:
            print("you can't take items while there is an enamie in the room with you")
    def do_unlock(self, args):
        "use this command to unlock doors. you can do this with a key or by picking them with something sharp"
        split_args = args.split(" ")
        if len(split_args) != 3:
            print("you must say what you want to unlock and what with")
            print("ie. unlock door with key")
        else:
            tool = split_args[2]
            door = split_args[0]
            unlock(current_room, player, door,  tool)
    def do_attack(self, args):
        "this is how you damage enemies, but attacking enemies will cause them to attack you"
        command_split = args.split(" ")
        thing = ""
        for part in command_split:
            if part != "with":
                if thing == "":
                    thing += part
                else:
                    thing += " "
                    thing += part
            else:
                enemie = thing
                thing = ""
        weapon = thing
        if len(enemie) == 0 or len(weapon) == 0:
                print("enter what you want to attack and what with")
                print("ie. attack officer with fists")
        else:
            valid_enemie = False
            for room_enemie in current_room.enemies:
                if room_enemie.name == enemie:
                    enemie = room_enemie
                    valid_enemie = True
                    break
            if weapon == "fists":
                damage = 5
                hit_chance = 85
            else:
                for item in player.items:
                    if item.name == weapon:
                        damage = item.used_for[0][1]
                        hit_chance = item.used_for[0][2]
            if valid_enemie:
                try:
                    player_attack(enemie, damage, hit_chance)
                    time.sleep(1)
                    print("")
                    for enemie in current_room.enemies:
                        enemie_attack(enemie)
                except NameError:
                    print("you dont have that item")
            else:
                print("thats not a valid enemie")
                
            if player.health <=0:
                return True
    def do_eat(self, args):
        "eat food to regain hp"
        for item in player.items:
            if item.name == args:
                food = item 
        try:
            eat(player, food)
        except NameError:
            print("you dont have that item")
    def do_open(self,args):
        "this will open an unlocked door\nit will not work on locked doors as you must unlock them first"
        open_(current_room, args)
    def do_read(self, args):
        "read a peice of paper"
        for item in player.items:
            if item.name == args:
                args= item
                read(args)
        if args not in player.items:
            print("you don't have that item")
    def do_veiw(self, args):
        "veiw your inventory or take a closer look at a specific item"
        veiw(player, args)

player = Player()
#Enemie(name, health, damage, hit chance, dialog)
officer = Enemie("officer vernam", 15, 5, 70, "'hey you, get back in your cell!!'")
SuperMan = Enemie("superman", 1000, 30, 95, "'Im a big fan of justice \nbut then again'\n*lazer eyes intensifies*")
chef = Enemie("chef", 20, 30, 40, "Im gonna cut you up!", "a ")
guard = Enemie("guard", 15, 15, 75, "what are you doing out of your cell!?!?! \n*brandshes batton*", "a ")


def make_items():
    nail = Item("nail", "a", [("attack", 20, 20), "unlock"])
    paper = Item("paper", "a peice of", [("attack", 2, 90), ("read", "Zork intro text.txt")])
    code_paper = Item("code paper", "the", [["attack", 0, 100], ["read", "Zork code p2.txt"]])
    key_paper = Item("key paper", "the", [("attack", 0, 100), ("read", "Zork code.txt")])
    batton = Item("batton", "a", [("attack", 10, 50)])
    cake = Item("cake", "a", [("attack", 1, 100), ("eat", 50)])
    apple = Item("apple", "an", [["attack", 2, 100], ["eat", 15]])
    knife = Item("knife", "a", [["attack", 50, 60]])
    RPG = Item("RPG", "an", [["attack", 200, 100]])
    easter_egg = Item("easter egg", "the", [["attack", 0, 0]], "congrats!!\nyou have found the really cool easter egg\nthis eleveates you to epic gamer status\nwell done")

    return nail, paper, batton, cake, apple, knife, RPG, code_paper, key_paper, easter_egg

nail, paper, batton, cake, apple, knife, RPG, code_paper, key_paper, easter_egg = make_items()


def make_rooms():
    #Room(name, rooms, items, unlocked, enemies)
    cell = Room("cell", [], [], [], [])
    office = Room("Prison Office", [], [], [], [officer])
    store_room = Room("store room", [], [], [], [])
    customs = Room("customs", [], [], [], [guard])
    canteen = Room("canteen", [], [], [], [])
    kitchen = Room("kitchen", [], [], [], [chef])
    gym = Room("gym", [], [], [], [SuperMan])
    prison_hallway = Room("prison hallway", [], [], [], [])
    prison_hallway1 = Room("hallway", [], [], [], [guard])
    vent_cross = Room("vent A" , [], [], [], [])
    vent_cross1 = Room("vent B", [], [], [], [])
    vent_cross2 = Room("vent C", [], [], [], [])
    vent_cross3 = Room("vent D", [], [], [], [])
    vent_cross4 = Room("vent E", [], [], [], [])
    escape = Room("exit", [], [], [], [])

    #cell
    adjasent_rooms = [["NORTH", "NIL"],["EAST", "NIL"],["SOUTH", "NIL"],["WEST", "locked door"],["DOWN", "NIL"],["UP", "NIL"]]
    items = [nail, paper]
    unlocked = [["locked door", "closed door"], ["closed door", prison_hallway]]
    cell.rooms = adjasent_rooms
    cell.items = items
    cell.unlocked = unlocked

    # office
    adjasent_rooms = [["NORTH", "NIL"],["EAST", "NIL"],["SOUTH", prison_hallway],["WEST", store_room],["DOWN", "NIL"],["UP", "NIL"]]
    items = ["closed drawer"]
    unlocked = [["closed drawer", [batton, cake]]]
    office.rooms = adjasent_rooms
    office.items = items
    office.unlocked = unlocked

    #store room
    adjasent_rooms = [["NORTH", "NIL"],["EAST", office],["SOUTH", "NIL"],["WEST", "NIL"],["DOWN", "NIL"],["UP", "closed vent"]]
    items = [apple]
    unlocked = [["closed vent", vent_cross]]
    store_room.rooms = adjasent_rooms
    store_room.items = items
    store_room.unlocked = unlocked

    #customs
    adjasent_rooms = [["NORTH", escape],["EAST", "NIL"],["SOUTH", "NIL"],["WEST", "NIL"],["DOWN", "NIL"],["UP", vent_cross1]]
    items = [code_paper]
    customs.rooms = adjasent_rooms
    customs.items = items

    #canteen
    adjasent_rooms = [["NORTH", kitchen],["EAST", "NIL"],["SOUTH", prison_hallway1],["WEST", "NIL"],["DOWN", "NIL"],["UP", vent_cross2]]
    items = [knife, cake]
    canteen.rooms = adjasent_rooms
    canteen.items = items

    #kitchen
    adjasent_rooms = [["NORTH", escape],["EAST", "NIL"],["SOUTH", canteen],["WEST", "NIL"],["DOWN", "NIL"],["UP", "NIL"]]
    items = [cake, key_paper]
    kitchen.rooms = adjasent_rooms
    kitchen.items = items

    #gym
    adjasent_rooms = [["NORTH", prison_hallway1],["EAST", "NIL"],["SOUTH", "NIL"],["WEST", "NIL"],["DOWN", "NIL"],["UP", "NIL"]]
    items = [easter_egg]
    gym.rooms = adjasent_rooms
    gym.items = items

    #prison hallway
    adjasent_rooms = [["NORTH", office],["EAST", cell],["SOUTH", "NIL"],["WEST", "NIL"],["DOWN", "NIL"],["UP", "NIL"]]
    prison_hallway.rooms = adjasent_rooms

    #prisom hallway 1
    adjasent_rooms = [["NORTH", canteen],["EAST", "NIL"],["SOUTH", gym],["WEST", "NIL"],["DOWN", "NIL"],["UP", vent_cross3]]
    prison_hallway1.items = ["locked safe"]
    prison_hallway1.unlocked = [["locked safe", "closed safe"], ["closed safe", [RPG]]]
    prison_hallway1.rooms = adjasent_rooms
    prison_hallway1.extra_info = "the safe in this room reqires a 4-didget code to unlock"

    #vent cross
    adjasent_rooms = [["NORTH", vent_cross1],["EAST", "NIL"],["SOUTH", vent_cross4],["WEST", vent_cross2],["DOWN", office],["UP", "NIL"]]
    vent_cross.rooms = adjasent_rooms

    #vent cross 1
    adjasent_rooms = [["NORTH", "NIL"],["EAST", "NIL"],["SOUTH", vent_cross],["WEST", "NIL"],["DOWN", customs],["UP", "NIL"]]
    vent_cross1.rooms = adjasent_rooms

    #vent cross 2
    adjasent_rooms = [["NORTH", "NIL"],["EAST", vent_cross],["SOUTH", "NIL"],["WEST", "NIL"],["DOWN", canteen],["UP", "NIL"]]
    vent_cross2.rooms = adjasent_rooms

    #vent cross 3
    adjasent_rooms = [["NORTH", "NIL"],["EAST", vent_cross4],["SOUTH", "NIL"],["WEST", "NIL"],["DOWN", prison_hallway1],["UP", "NIL"]]
    vent_cross3.rooms = adjasent_rooms

    #vent cross 4
    adjasent_rooms = [["NORTH", vent_cross],["EAST", "NIL"],["SOUTH", "NIL"],["WEST", vent_cross3],["DOWN", "NIL"],["UP", "NIL"]]
    vent_cross4.rooms = adjasent_rooms
    return cell
cell = make_rooms()
current_room = cell


def look(current_room):
    string = ("")
    for i in range(0, len(current_room.name)):
        string += ("-")
    print("")
    print(string)
    print(current_room.name)
    print(string)

    if len(current_room.enemies) == 0:

        if len(current_room.items) == 0:
            print("the room is empty")
        elif len(current_room.items) == 1:
            if type(current_room.items[0]) == type(cake):
                print("there is",(current_room.items[0]).prefix, (current_room.items[0]).name)
            else:
                print(f"there is a {current_room.items[0]}")
        else:
            string = "there is "
            for index, item in enumerate(current_room.items ):
                if type(item) == type(cake):
                    string += item.prefix
                    string += " "
                    string += item.name
                else:
                    strng += (f"a {item}")
                if index <= len(current_room.items) - 3:
                    string += ", "
                elif index == len(current_room.items) - 2:
                    string += " and "
                else:
                    pass
                
            print(string)

                       
            

        for i in range(0, len(current_room.rooms)): 
            if current_room.rooms[i][1] != "NIL":
                if current_room.rooms[i][0] != "DOWN" and current_room.rooms[i][0] != "UP":
                    if type(current_room.rooms[i][1]) == type(cell):
                        print("there is a", current_room.rooms[i][1].name, "to the", current_room.rooms[i][0])
                    else:
                        print("there is a", current_room.rooms[i][1], "to the", current_room.rooms[i][0])
                else:
                    if current_room.rooms[i][0] == "UP":
                        if type(current_room.rooms[i][1]) == type(cell):
                            print("above you there is a", current_room.rooms[i][1].name)
                        else:
                            print("above you there is a", current_room.rooms[i][1])
                    elif current_room.rooms[i][0] == "DOWN":
                        if type(current_room.rooms[i][1]) == type(cell): 
                            print("below you there is a", current_room.rooms[i][1].name)
                        else:
                            print("below you there is a", current_room.rooms[i][1])
        if current_room.extra_info != None:
            print(current_room.extra_info)
    else:
        print(f"this room has {(current_room.enemies[0]).prefix}{(current_room.enemies[0]).name} in it!")
        print((current_room.enemies[0]).dialog)
                

def take(current_room, player, item):
    found  = False
    for room_item in current_room.items:
        if room_item.name == item:
            found = True
            (current_room.items).remove(room_item)
            (player.items).append(room_item)
            print("taken", item)
            if room_item.message != None:
                print(room_item.message)
    if not found:
        print("there is no item by that name here")


def unlock(current_room, player, door, tool):
    if door == "safe":
        if tool == "2004":
            current_room.items[0] = "closed safe"
            print("unlocked safe")
            return True

    valid_tool = False
    for item in player.items:
        if item.name == tool:
            tool = item
            if any("unlock" in used_for for used_for in tool.used_for):
                valid_tool = True
    
    if not valid_tool:
        print("invalid tool")

    valid_door = False

    for i in range(0, len(current_room.rooms)):
        room_door = current_room.rooms[i][1]
        try:
            split_door = room_door.split(" ")
        except AttributeError:
            break
        if split_door[0] == "locked" and split_door[1] == door:
            valid_door = True
            door_pos = ["rooms", i]
    for i  in range(len(current_room.items)):
        room_door = current_room.items[i]
        try:
            split_door = room_door.split(" ")
        except AttributeError:
            break
        if split_door[0] == "locked" and split_door[1] == door:
            valid_door = True
            door_pos = ["items" , i]


    if not valid_door:
        print("that is not something that can be unlocked")
    elif valid_door and valid_tool:
        print("you have unlocked the" ,door)
        door = "locked " + door
        for i in range(len(current_room.unlocked)):
            if current_room.unlocked[i][0] == door:
                if door_pos[0] == "items":
                    current_room.items[door_pos[1]] = current_room.unlocked[i][1]
                if door_pos[0] == "rooms":
                    current_room.rooms[door_pos[1]][1] = current_room.unlocked[i][1]
        (player.items).remove(tool)
        print(f"but the {tool.name} was broken in the process")
                             

def go(current_room, direction):

    direction = direction.upper()
    for i in range(0, len(current_room.rooms)):     
            
        if current_room.rooms[i][0] == direction:
            if type(current_room.rooms[i][1]) == type(cell):
                current_room = current_room.rooms[i][1]
                print("you move", direction)
                if current_room.name != "exit":
                    look(current_room)
            elif current_room.rooms[i][1] == "NIL":
                #print(current_room.rooms[i][1])
                print("you cant go that way")
            else:
                rooms_split = current_room.rooms[i][1].split(" ")
                if rooms_split[0] == "locked":
                    print("that is locked")
                elif  rooms_split[0] == "closed" or rooms_split[0] == "shut":
                    print("that door is closed")
            break
    return current_room


def player_attack(enemie, damage, hit_chance):
    if random.randint(0, 101) <= hit_chance:
        enemie.health -= damage
        print("the attack landed!! \nyou did", damage, "damage")
    else:
        print("you missed")
    if enemie.health <= 0:
        print("you have defeated the", enemie.name)
        (current_room.enemies).remove(enemie)
        look(current_room)
    else:
        print("the", enemie.name, "has", enemie.health, "left")


def enemie_attack(enemie):
    if random.randint(0, 101) <= enemie.hit_chance:
        player.health -= enemie.damage
        print("the", enemie.name, "landed!! \nthey did", enemie.damage, "damage")
    else:
        print("the", enemie.name, "missed")
    if player.health <= 0:
        print("you have died")
    else:
        print("you now have", player.health, "health")

  
def eat(player, food):
    added_hp = False
    if any("eat" in used_for for used_for in food.used_for):
        for use in food.used_for:
            if use[0] == "eat":
                hp = use[1]
                break
        player.health += hp
        (player.items).remove(food)
        added_hp = True
        if player.health > player.max_hp:
            player.health = player.max_hp
            print("this would exeeded your max hp so you have been set to your max hp")
        print(f"you ate the food, it gave you {hp} hp")
        print(f"you are now at {player.health} hp")
    
    if not added_hp:
        print("you can't eat that")
    

def open_(current_room, door):
    valid_door = False

    full_door1 = "shut " + str(door)
    full_door2 = "closed " + str(door)
    for index, values in enumerate(current_room.rooms):
        if values[1] == full_door1 or values[1] == full_door2:
            valid_door = True
            door_pos = ["rooms", index]

    for index, item in enumerate(current_room.items):
        if item == full_door1 or item == full_door2:
            valid_door = True
            door_pos = ["items", index, ]

    if valid_door == False:
        print("thats not a valid door")
    else:
        for index, unlocked in enumerate(current_room.unlocked):
            if unlocked[0] == full_door1 or unlocked[0] == full_door2:
                if door_pos[0] == "rooms":
                    current_room.rooms[door_pos[1]][1] = unlocked[1]
                    print("opened")
                if door_pos[0] == "items":
                    if type(unlocked[1]) != list:
                        current_room.items[door_pos[1]] == unlocked[1]
                    else:
                        try:
                            (current_room.items).remove(full_door1)
                        except ValueError:
                            (current_room.items).remove(full_door2)
                        for item in unlocked[1]:
                            (current_room.items).append(item)
                    print("opened")


def read(item):
    for use in item.used_for:
        if use[0] == "read":
            my_file = open(use[1])
            contents = my_file.read()
            print(contents)


def veiw(player, item):
    if item == "inventory":
        print("you have:")
        for item in player.items:
            print(f"{item.prefix} {item.name}")
    else:
        for p_item in player.items:
            if p_item.name == item:
                print(f"{p_item.name}:")
                for use in p_item.used_for:
                    if use[0] == "attack":
                        print(f"{use[0]}: damage:{use[1]} hit chance:{use[2]}")
                    elif use[0] == "eat":
                        print(f"eat: health:{use[1]}")
                    elif use[0] == "read":
                        print("this item is readable")
                    else:
                        print(f"{use}")
                break
        try:
            if use == "":
                pass
        except NameError:
            print("you dont have that item") 


look(current_room)
if __name__ == '__main__':
    prompt = Prompts()
    prompt.prompt = '> '
    prompt.cmdloop('')
    