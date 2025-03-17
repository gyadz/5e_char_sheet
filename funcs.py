import os
import shutil

import random

class Character: # this class handles everything related to processing information related to characters
    char_name="" # character directory

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

    def __init__(self, c_name):
        self.char_name=c_name
        self.construct_StatsProficiencies()
# DESTRUCTOR FUNCS -----------------------------------------------------------------------------------------
# sec1 = Prof bonus, Profs, Stats
    def save_sec1(self): 
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

    def saveAll(self): # will be expanded as the program grows
        self.saveStatsProfBProfs()

class Init: # this class creates, writes, and deletes files
    mdir="" # main directory holding all character subdirectories

    def createChar(self, char_name): # this will expand with the program
        try:
            os.mkdir(os.path.join(self.mdir, char_name))
            with open(os.path.join(self.mdir, char_name, "stats.txt"), 'w') as stats_file:
                stats_file.write("0\nstr00.dex00.con00.int00.wis00.cha00")
            stats_file.close()
        except Exception as e:
            print(f"Error: {e}. This is in the terminal which is wrong, but whatever. I'll figure it out")

    def editChar(self, char_name, new_name):
        os.rename(os.path.join(self.mdir, char_name), os.path.join(self.mdir, new_name))
        # will add more functionality later (pictures, etc)

    def deleteChar(self, char_name):
        shutil.rmtree(os.path.join(self.mdir, char_name))
# CONSTRUCTOR ----------------------------------------------------------------------------------------------
    def __init__(self):
        if not os.path.isdir(os.path.join(os.getcwd(), "characters")):
            # I should add error handling instead of just forcing it to work no matter where the exe is located
            # but also whatever. Don't fuck with the files and you'll be fine
            os.mkdir(os.path.join(os.getcwd(), "characters"))

        self.mdir=os.path.join(os.getcwd(), "characters")
        self.chars=os.listdir(self.mdir)