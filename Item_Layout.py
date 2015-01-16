# Item_Layout
import pickle
import os.path
import copy as __copyModule


def Save():
    with open("Item_LayoutData.pkl", "wb") as f:
        pickle.dump(layouts, f)


def Load():
    with open("Item_LayoutData.pkl", "rb") as f:
        layouts = pickle.load(f)
    return layouts

layouts = {}
if os.path.isfile("Item_LayoutData.pkl"):
    layouts = Load()
    for item in layouts:
        print "Loaded {0}".format(item)


# Make a dynamic load
validDynamicStats = ["HEALTH", "ENERGY", "HUNGER", "THIRST", "SLEEP"]


def AddLayout(idname, name, desc, u=True):
    """
    Base structure for any item layout
    the idname is the string with wich you can lookup an item, 
    this should be unique
    name is the display name to a user
    desc is the standard discription tied to the item

    u determines weather this function should update the new layout into the other
     layouts
    """
    idname = idname.upper()
    idname = idname.replace(" ", "_")
    print format_idname(idname)

    print format_name(name)

    desc = desc.capitalize()
    print format_desc(desc)

    temp = {str(idname): {"name": str(name), "desc": str(desc)}}
    if u == True:
        layouts.update(temp)
    else:
        return temp


def AddLayout_Consumable(idname, name, desc, STAT, CHANGEVALUE, u=True):
    """
    create a base layout with a  consumable tag in one swoop.
    """
    temp = AddLayout(idname, name, desc, u=False)
    temp = AddConsumableEffect(temp, STAT, CHANGEVALUE, u=False)
    if u == True:
        layouts.update(temp)
    else:
        return temp


def AddConsumableEffect(layoutsToChange, STAT, CHANGEVALUE, u=True):
    """
    Every item can have a AC_CONSUME tag on it, wich means the item can be consumed.
    When consumed it will apply all aplicable effects on the user of said item.
    The effects are stored in a list under the dictionairy tag "AC_CONSUME"
    In this list are dics that are formatted like so: {"stat":str(STAT),"change":float(CHANGEVALUE)}
    Where STAT is the stat you wish to change, and CHANGEVALUE by how much
    """
    STAT = STAT.upper()

    if not STAT in validDynamicStats:
        print "{0} is an unregisterd dynamic stat, and has thus not been added".format(STAT)
        print "The registered dynamic stats are:"
        for i in validDynamicStats:
            print "    {0}".format(i)
        return layoutsToChange

    for key in layoutsToChange.keys():
        if layoutsToChange[key].has_key("AC_CONSUME"):
            layoutsToChange[key]["AC_CONSUME"].append(
                {"stat": str(STAT), "change": float(CHANGEVALUE)})
        else:
            consumable = {
                "AC_CONSUME": [{"stat": str(STAT), "change": float(CHANGEVALUE)}]}
            layoutsToChange[key].update(consumable)
        print format_consumable(layoutsToChange[key])
    if u == True:
        layouts.update(layoutsToChange)
    else:
        return layoutsToChange


# gets layout with id name, wich can be updated back into the layout dict
def GetLayout(idname):
    idname = idname.upper()
    idname = idname.replace(" ", "_")
    return {idname: layouts[idname]}


# gets layout without the idname, as seen in the item class
def GetItemLayout(idname):
    idname = idname.upper()
    idname = idname.replace(" ", "_")
    temp = __copyModule.deepcopy(layouts[idname])
    return temp


def format_idname(idname):
    return "ID name is: '{0}'".format(idname)


def format_name(name):
    return "Item display name is: '{0}'".format(name)


def format_desc(desc):
    return "Item desciption is: '{0}'".format(desc)


def format_consumable(d):
    d = d["AC_CONSUME"]
    temp = "Item has the action 'consume' with effects:\n"
    for e in d:  # For the effects in the layout
        temp += "  - affected cur dynamic stat '{0}' with a change value of {1}\n".format(
            e["stat"], e["change"])
    return temp


def debug_fixConsume(d):
    for key in d.keys():
        if d[key].has_key("AC_CONSUME"):
            if type(d[key]["AC_CONSUME"]) == dict:
                d[key]["AC_CONSUME"] = [d[key]["AC_CONSUME"]]

##    idname = idname.upper()
##    idname = idname.replace(" ", "_")
# print "ID name is: '{0}'".format(idname)
##
# print "Item display name is: '{0}'".format(name)
##
##    desc = desc.capitalize()
# print "Item desciption is: '{0}'".format(desc)
##
##    temp = {str(idname):{"name":str(name), "desc":str(desc),"AC_CONSUME": {"stat":str(STAT),"change":float(CHANGEVALUE)}  }}
# layouts.update(temp)

# def Action


def LogLayouts():
    for idname in layouts:
        LogLayout(idname, layouts)


def LogLayout(idname, Layoutslist):
    print "[]-------------------[{0}]---------------------[]".format(idname)
    d = layouts[idname]
    print format_idname(idname)
    print format_name(d["name"])
    print format_desc(d["desc"])
    if d.has_key("AC_CONSUME"):
        print format_consumable(d)

    print "[]------------------[\\{0}]---------------------[]".format(idname)

    print ""


if __name__ == "__main__":
    print "!Item Editor:"
