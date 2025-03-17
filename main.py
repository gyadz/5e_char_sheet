import os
import random
import tkinter as tk

from funcs import Character
from funcs import Init


# settings to change:
#   light/dark mode
# Do I want commandline things like in roll20 along with the buttons?

def eraseCanvas(): # I imagine there is a better method that doesn't erase and rewrite the entire page every time
    # I move between different sections of the code
    for widget in canvas.winfo_children():
        widget.destroy()
# CLASS MANAGEMENT --------------------------
def createP1Class():
    return Init()
def createUserClass(char_name):
    return Character(char_name)
def deleteClass(item): # called in a lambda. Lambda can't call del, so I gotta do it this way
    del item
#--------------------------
def stripStar(stat):
    return stat if stat[0]!='*' else stat[1:]
# STUFF THAT ROLLS DICE -----------------------------------------------------------------------------------------
def roll(self, ndice, tdice):
    rolls=[]
    for num in range(ndice):
        rolls.append(random.randint(1, tdice))
    return rolls

def makeCheckSave(user, stat, skill, type, apply_proficiency):
    roll=roll(1, 20)[0] # this returns a list, so I'm just taking the first (and only) element
    total=int(roll+(user.stats[stat]-10)/2) # int() strips decimals
    if apply_proficiency:
        for item in user.proficiencies[stat]:
            if item[0]=='*' and item[1:]==skill:
                total+=user.prof_bonus
    
    popout=tk.Toplevel(window)
    popout.geometry("300x300")
    popout.config(bg="black")

    label=tk.Label(popout, text=f"{skill} {type}", bg="black", fg="white", font=("Times New Roman", 14))
    label.grid(column=0, row=0, columnspan=2, sticky="new")

    row=1
    if roll==1:
        label=tk.Label(popout, text="Critical fail", bg="black", fg="white", font=("Times New Roman", 11))
        label.grid(column=0, row=row, columnspan=2, sticky="w")
        row+=1
    elif roll==20:
        label=tk.Label(popout, text="Critical success", bg="black", fg="white", font=("Times New Roman", 11))
        label.grid(column=0, row=row, columnspan=2, sticky="w")
        row+=1
    
    label=tk.Label(popout, text=f"Roll: {roll}", bg="black", fg="white", font=("Times New Roman", 11))
    label.grid(column=0, row=row, columnspan=2, sticky="w")
    label=tk.Label(popout, text=f"Total: {total}", bg="black", fg="white", font=("Times New Roman", 11))
    label.grid(column=0, row=row+1, columnspan=2, sticky="w")

    # I'd love to include these two but they're not working and I don't know why
   # popout.bind('<Return>', lambda event: popout.destroy())
   # popout.bind('<Escape>', lambda event: popout.destroy())
# MANAGE STATS/PROFS/SAVES --------------------------------------------------------------------------------------
def editProfsAction(user, stat, skill):
    i=0
    while(True):
        if user.proficiencies[stat][i][0]=='*' and user.proficiencies[stat][i][1:]==skill:
            user.proficiencies[stat][i]=user.proficiencies[stat][i][1:]
            break
        elif user.proficiencies[stat][i]==skill:
            user.proficiencies[stat][i]='*'+user.proficiencies[stat][i]
            break
        i+=1
    
def editProfsMenu(user, type, stat):
    eraseCanvas()

    editProfs_frame=tk.Frame(canvas)
    canvas.create_window((0,0), window=editProfs_frame, anchor="nw")
    editProfs_frame.config(bg="black")

    label=tk.Label(editProfs_frame, text=f"Select {type} to add/remove:", bg="black", fg="white", font=("Times New Roman", 12))
    label.grid(column=0, row=0, columnspan=3, sticky="w")

    col=0
    row=1
    if stat=="saves": # if it's editing saves
        for stat in user.proficiencies: # repeated code
            button=tk.Button(editProfs_frame, text=user.proficiencies[stat][0], bg="black", fg="white", command=lambda stat_name=stat, stripped_S_name=stripStar(user.proficiencies[stat][0]): (editProfsAction(user, stat_name, stripped_S_name), selectChar(user)))
            button.grid(column=col, row=row, sticky="w")
            col+=1
            if col>2:
                row+=1
                col=0
    else: # if it's editing general skills
        for item in user.proficiencies[stat][1:]:
            button=tk.Button(editProfs_frame, text=item, bg="black", fg="white", command=lambda stat_name=stat, stripped_S_name=stripStar(item): (editProfsAction(user, stat, stripped_S_name), selectChar(user)))
            button.grid(column=col, row=row, sticky="ew")
            col+=1
            if col>2:
                row+=1
                col=0

    button=tk.Button(editProfs_frame, text="Back", bg="black", fg="white", command=lambda: selectChar(user))
    button.grid(column=0, row=row+1, pady=15, sticky="w")
# DISPLAY STATS/PROFS/SAVES -------------------------------------------------------------------------------------
# wups forgot about this shit. Will fix later
def displayProfBonus(user, frame):
    label=tk.Label(frame, text=f"Proficiency Bonus:", bg="black", fg="white", font=("Times New Roman", 10))
    label.grid(column=0, row=0, columnspan=3, sticky="w")

    #
    def editProfBonus(user, value): # literally only used here
        user.prof_bonus=int(value)
    #
    prof_var=tk.StringVar()
    entry=tk.Entry(frame, width=3, textvariable=prof_var) # tracks changes
    entry.insert(0, str(user.prof_bonus))
    prof_var.trace("w", lambda *args: editProfBonus(user, int(prof_var.get()))) # not entry.get() because that fetches info from
    # before it was edited, prof_var is edited, and that's the info I need to fetch
    entry.grid(column=0, row=1, sticky="w")

def displaySaves(user, frame):
    label=tk.Label(frame, text="Saves (* denotes proficiency):", bg="black", fg="white", font=("Times New Roman", 10))
    label.grid(column=0, row=2, sticky="w", columnspan=3)

    col=0
    row=3 
    for stat in user.proficiencies: # repeated code
        button=tk.Button(frame, text=user.proficiencies[stat][0], bg="black", fg="white", command=lambda stat_name=stripStar(stat): makeCheckSave(user, stat_name, stat_name, "save", True)) 
        button.grid(column=col, row=row, sticky="we" if col<2 else "w")
        col+=1
        if col>2:
            row+=1
            col=0
    button=tk.Button(frame, text="edit", bg="black", fg="white", command=lambda: (editProfsMenu(user, "save", "saves")))
    button.grid(column=0, row=row, pady=5, sticky="w")

def displayProfs(user, stat, row, frame):
    for item in user.proficiencies[stat][1:]: # for each item excluding the first, which is the stat name (for saves)
        button=tk.Button(frame, text=item, bg="black", fg="white", font=("Times New Roman", 11), command=lambda skill=item: makeCheckSave(user, stat, stripStar(skill), "check", True))
        button.grid(column=2, row=row)
        row+=1
    
    row+=1
    if stat!="con":
        button=tk.Button(frame, text="Edit", bg="black", fg="white", font=("Times New Roman", 10), command=lambda stat_name=stat: editProfsMenu(user, "skill", stat_name))
        button.grid(column=2, row=row, pady=10, sticky="s")
    return row+1 # the con stat entry was getting cut off without this. I don't know why, but that's what was happening
    # NOTE ^ because of this, everything takes up an extra row. Shouldn't be too much of a problem, but something
    # to be aware of
    # NOTE: need button to edit proficiencies

def displayStat(user, stat, value, row, frame):
    button=tk.Button(frame, text=stat, bg="black", fg="white", font=("Times New Roman", 12), command=lambda stat_name=stat: makeCheckSave(user, stat_name, stat_name, "check", False))
    button.grid(column=0, row=row, sticky="ew")

    #
    def editStat(user, stat, value): #entering non-int characters raises an error and it just doesn't happen
        if value<99 and value>=0:
            user.stats[stat]=value
        elif value>99:
            user.stats[stat]=99
        elif value<0:
            user.stats[stat]=0      
    #
    stat_tracker=tk.StringVar()
    entry=tk.Entry(frame, width=3, textvariable=stat_tracker)
    entry.insert(0, value)
    stat_tracker.trace("w", lambda *args: editStat(user, stat, int(stat_tracker.get())))
    entry.grid(column=0, row=row+1)
# CHARACTER SHEET --------------------------------------------------------------------------------------------------------------
def selectChar(user): # displays character sheet
    eraseCanvas()
    # NOTE: p1 is deleted here and must be reconstructed before main() is called again
# col 4 I will reserve as a buffer
# rename/refactor? Seperate stats/profs/saves into different frames? Will do that in a bit, 
# gotta fix the first menu
    frame=tk.Frame(canvas)
    canvas.create_window((0,0), window=frame, anchor="nw")
    frame.config(bg="black")

    displayProfBonus(user, frame)
    displaySaves(user, frame)

    row=6
    for key, value in user.stats.items():
        displayStat(user, key, value, row, frame)
        row=displayProfs(user, key, row, frame)
        label=tk.Label(frame, text="----------------------------------------------", bg="black", fg="white")
        label.grid(column=0, row=row, columnspan=3)
        row+=1
    #print(row) this outputs fucking 43. Whaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatever
    button=tk.Button(frame, text="Save", bg="black", fg="white", command=lambda: (user.saveAll(), deleteClass(user), mainMenu(createP1Class())))
    button.grid(column=5, row=6) # will move this to the bottom I guess
    # NOTE: ^ this exists

    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all")) # this needs to be everywhere apparently
# --------------------------------------------------------------------------------------------------------------
def deleteChar(p1, c_name):
    popout=tk.Toplevel(window)
    popout.geometry("200x150")
    popout.config(bg="black")

    label=tk.Label(popout, text="Deleting a character\nCANNOT be undone. Continue?", bg="black", fg="white")
    label.grid()

    button=tk.Button(popout, text="Cancel", bg="black", fg="white", command=lambda: (popout.destroy(), editMenu(p1)))
    button.grid()
    button=tk.Button(popout, text="Continue", bg="black", fg="white", command=lambda: (popout.destroy(), p1.deleteChar(c_name), mainMenu(p1)))
    button.grid()

def editChar(p1, c_name):
    eraseCanvas()

    editC_frame=tk.Frame(canvas)
    canvas.create_window((0,0), window=editC_frame, anchor="nw")
    editC_frame.config(bg="black")

    label=tk.Label(editC_frame, text="Character name:", bg="black", fg="white", font=("Times New Roman", 12))
    label.grid(column=0, row=0, pady=7, columnspan=2, sticky="w")

    entry=tk.Entry(editC_frame)
    entry.insert(0, c_name)
    entry.grid(column=0, row=1, pady=10, columnspan=2, sticky="w")

    editC_frame.bind('<Return>', lambda event: (p1.editChar(c_name, entry.get()), mainMenu(p1)))
    button=tk.Button(editC_frame, text="Submit", bg="black", fg="white", command=lambda: (p1.editChar(c_name, entry.get()), mainMenu(p1)))
    button.grid(column=1, row=2)
    button=tk.Button(editC_frame, text="Cancel", bg="black", fg="white", command=lambda: mainMenu(p1))
    button.grid(column=0, row=2)
    button=tk.Button(editC_frame, text="Delete", bg="black", fg="red", command=lambda: deleteChar(p1, c_name))
    button.grid(column=0, row=3, pady=10, columnspan=2, sticky="nsew")

def editMenu(p1):
    eraseCanvas()

    editM_frame=tk.Frame(canvas)
    canvas.create_window((0,0), window=editM_frame, anchor="nw")
    editM_frame.config(bg="black")

    label=tk.Label(editM_frame, text="Select character to edit:", bg="black", fg="white", font=("Times New roman", 15))
    label.grid(column=0, row=0, pady=10, sticky="w")

    # listing characters
    i=1
    for item in os.listdir(p1.mdir):
        button=tk.Button(editM_frame, text=item, bg="black", fg="white", command=lambda c_name=item: editChar(p1, c_name))
        button.grid(column=0, row=i, pady=5, sticky="w")
        i+=1
    
    button=tk.Button(editM_frame, text="Back", bg="black", fg="white", command=lambda: mainMenu(p1))
    button.grid(column=0, row=i+2, pady=50, sticky="w")

def newChar(p1):
    popout=tk.Toplevel(window)
    popout.geometry("200x150")
    popout.config(bg="black")

    label=tk.Label(popout, text="Enter character name:", bg="black", fg="white")
    label.grid()

    entry=tk.Entry(popout)
    entry.grid()

# binds escape to terminate popout and enter to accept inputs
# lambda takes the event parameter because when an event happens, tkinter passes an event object to the event
# handler, in this case the lambda
    # buttons handling inputs
    popout.bind('<Escape>', lambda event: (popout.destroy(), mainMenu(p1)))
    popout.bind('<Return>', lambda event: (p1.createChar(entry.get()), popout.destroy(), mainMenu(p1)))
    button=tk.Button(popout, text="Submit", command=lambda: (p1.createChar(entry.get()), popout.destroy(), mainMenu(p1)))
    button.grid()

def mainMenu(p1):
    eraseCanvas()

    main_frame=tk.Frame(canvas)
    canvas.create_window((0,0), window=main_frame, anchor="nw")
    main_frame.config(bg="black")

    # listing characters
    label=tk.Label(main_frame, text="Characters:", bg="black", fg="white", font=("Times New Roman", 15))
    label.grid(column=0, row=0, pady=5, sticky="w")
    i=1
    for item in os.listdir(p1.mdir): 
        button=tk.Button(main_frame, text=item, bg="black", fg="white", command=lambda char_name=item: (deleteClass(p1), selectChar(createUserClass(char_name))))
        button.grid(column=0, row=i, pady=2, sticky="w")
        i+=1
    
    main_frame.columnconfigure(2, minsize=125) # adding some whitespace between tutorial messages and everything else
    label=tk.Label(main_frame, text="Welcome! Thanks for using this app :)", bg="black", fg="white", font=("Times New Roman", 12))
    label.grid(column=3, row=1)
    label=tk.Label(main_frame, text="To select a character, use the associated button", bg="black", fg="white", font=("Times New Roman", 12))
    label.grid(column=3, row=2)
    label=tk.Label(main_frame, text="To create a new character, select the NEW button", bg="black", fg="white", font=("Times New Roman", 12))
    label.grid(column=3, row=3)
    label=tk.Label(main_frame, text="To edit character names/pictures and to delete characters,\nselect the EDIT button", bg="black", fg="white", font=("Times New Roman", 12))
    label.grid(column=3, row=4)

    # new/edit buttons. inline row logic ensures it remains beneath the tutorial messages
    button=tk.Button(main_frame, text="new", bg="black", fg="white", command=lambda: newChar(p1)) 
    button.grid(column=0, row=5 if i<5 else i+1, pady=25, sticky="w")
    button=tk.Button(main_frame, text="Edit", bg="black", fg="white", command=lambda: editMenu(p1))
    button.grid(column=1, row=5 if i<5 else i+1, sticky="e")
    main_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
#------------------------------------------------------------------------------------------------------------
window=tk.Tk()
window.geometry("900x600")
window.title("Dumb App for Dumb Stupid Dumb Dumbs")
window.config(bg="black")

canvas=tk.Canvas(window)
canvas.pack(side="left", fill="both", expand=True)
vsb=tk.Scrollbar(window, orient="vertical", command=canvas.yview)
vsb.pack(side="right", fill="y") 
canvas.configure(yscrollcommand=vsb.set)
canvas.config(bg="black")

p1=Init()
mainMenu(p1)
window.mainloop()