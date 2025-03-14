import os
import shutil

import random

class Character: # this class handles everything related to processing information related to characters
    prof_bonus=0 
    stats={
        "str":0, "dex":0, "con":0, "wis":0, "int":0, "cha":0
    }
    proficiencies={
    # repeated to accomodate saves
        "str":["str", "athletics"],
        "dex":["dex", "acrobatics", "stealth", "sleight of hand"],
        "con":["con"],
        "wis":["wis", "animal handling", "insight", "medicine", "perception", "survival"],
        "int":["int", "arcana", "history", "medicine", "investigation", "nature", "religion"],
        "cha":["cha", "deception", "intimidation", "performance", "persuasion"]
    }

    char_name="" # character directory

# CONSTRUCTOR FUNCTIONS ----------------------------------------------------------------------------
    def construct_StatsProficiencies(self):
        temp=[]
        with open(os.path.join(os.getcwd(), "characters", self.char_name, "stats.txt"), 'r') as stats_file:
            for line in stats_file:
                temp.append(line.strip())
        stats_file.close() 
        self.prof_bonus=int(temp[0]) # assign proficiency bonus
        stats_temp=temp[1].split('.') # split stats apart

        for item in stats_temp:
            stat=item[0:3] # fetch current stat name
            self.stats[stat]=int(item[3:5]) # assign stat value

            temp_profs=item.split(':') # split proficiencies
            del temp_profs[0] # delete stat value, it's not applicable

            for index in range(0, len(self.proficiencies[stat])): # assign proficiencies
                if self.proficiencies[stat][index] in temp_profs:
                    self.proficiencies[stat][index]='*'+self.proficiencies[stat][index]
        # doesn't allow for custom proficiencies currently       

    def __init__(self, c_name):
        self.char_name=c_name
        self.construct_StatsProficiencies()
# END OF CONSTRUCTOR FUNCS ---------------------------------------------------------------------------------
# DESTRUCTOR FUNCS -----------------------------------------------------------------------------------------
    def saveStatsProfBProfs(self): # unofficial destructor. Might have to main one in main.py
        with open(os.path.join(os.getcwd(), "characters", self.char_name, "stats.txt"), 'w') as stats_file:
            stats_file.write(str(self.prof_bonus)+'\n')
            
            for stat, value in self.stats.items(): # for item in stats, write stat value pairs
                stats_file.write(stat)
                if value<10:
                    stats_file.write('0'+str(value))
                else:
                    stats_file.write(str(value))

                for prof in self.proficiencies[stat]:
                    if prof[0]=='*':
                        stats_file.write(':'+prof[1:])# everything except the *
                
                if stat!="cha": # don't need the extra . at the end, just leads to an extra empty string
                    stats_file.write('.')
        stats_file.close()
# FUNCTIONALITY -------------------------------------------------------------------------------------------
    def roll(self, ndice, tdice):
        rolls=[]
        for num in range(ndice):
            rolls.append(random.randint(1, tdice))
        return rolls

class Init: # this class creates, writes, and deletes files
    mdir="" # main directory holding all character subdirectories
    chars=[]

    def createChar(self, char_name): # I suspect this function will only get more complex. Also why not have this
        # in the other class? Jesus christ this is so overengineered
        # I don't have this in the other class because it's not opening anything or processing any information
        try:
            os.mkdir(os.path.join(self.mdir, char_name))
            with open(os.path.join(self.mdir, char_name, "stats.txt"), 'w') as stats_file:
                stats_file.write("0\nstr00.dex00.con00.int00.wis00.cha00")
            stats_file.close()
        except Exception as e:
            print(f"Error: {e}. This is in the terminal which is wrong, but whatever. I'll fucking figure it out")

    def editChar(self, char_name, new_name):
        os.rename(os.path.join(self.mdir, char_name), os.path.join(self.mdir, new_name))
        # will add more functionality later (pictures, etc)

    def deleteChar(self, char_name):
        shutil.rmtree(os.path.join(self.mdir, char_name))
# -------------------------------------------------------------------------------------------
    def __init__(self):
        if not os.path.isdir(os.path.join(os.getcwd(), "characters")):
            os.mkdir(os.path.join(os.getcwd(), "characters"))

        self.mdir=os.path.join(os.getcwd(), "characters")
        self.chars=os.listdir(self.mdir)