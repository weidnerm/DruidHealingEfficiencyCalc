import os
import sys

debugFlag = 0;

class Spell:
    parseState = 0; # 0=seeking SPELL_CAST_START; 1=parsing; 
    
    # start with SPELL_CAST_START or SPELL_AURA_APPLIED



# info on combat log event (hopefully similar to combat log file)
# 0                             1                   2                  3      4  5                    6                 7     8   9    10         11  12                13              141516171819202122   23   2425     26     2728
# 9/22 12:40:02.261  SPELL_HEAL,Player-113-05CD0880,"Cellifalas-Draka",0x511,0x0,Player-113-05CD0880,"Cellifalas-Draka",0x511,0x0,8936,"Regrowth",0x8,0000000000000000,0000000000000000,0,0,0,0,0,0,0,0,0.00,0.00,0,138287,138287,0,1






def convertTimeToSec(dateTime):
    rawField = dateTime.split()
    theDate = rawField[0]
    theTime = rawField[1]
    (months,days) = theDate.split("/")
    (hours,minutes,seconds) = theTime.split(":")
    returnVal = 0
    returnVal = returnVal + int(float(seconds))
    returnVal = returnVal + int(minutes)*60
    returnVal = returnVal + int(hours)*60*60
    returnVal = returnVal + int(days)*24*60*60
    returnVal = returnVal + int(months)*31*24*60*60
    return returnVal




def readFile(fileName):
    if ( os.path.isfile(fileName) ):
        with open(fileName) as f:
            content = f.readlines();
        for lineNum in range(len(content)):
            content[lineNum] = content[lineNum].rstrip();  # strip out CR/LF whitespace at the end.
        f.close();
    else:
        content = ["",""]  # need at least 2 lines so that the extend operations dont fail on this.  probably a better way exists.
    return content;

# NOT THIS vvvvvv    
# parse_log = [index] = {} ["spellName"] = spellname
#                          ["directHeal"] = healamount
#                          ["tickCount"] = number of ticks
#                          ["tickTotal"] = tick total
# NOT THIS ^^^^^^^


# parse_log = {} [spellname] = {} ["directHealAmount"] = HP total (crit down compensated)
#                                 ["directHealCount"] = count  
#                                 ["tickHealAmount"] = HP total (crit down compensated)  
#                                 ["tickHealCount"] = count  

# info on combat log event (hopefully similar to combat log file)
# 0                             1                   2                  3      4  5                    6                 7     8   9    10         11  12                13              141516171819202122   23   2425     26     2728
# 9/22 12:40:02.261  SPELL_HEAL,Player-113-05CD0880,"Cellifalas-Draka",0x511,0x0,Player-113-05CD0880,"Cellifalas-Draka",0x511,0x0,8936,"Regrowth",0x8,0000000000000000,0000000000000000,0,0,0,0,0,0,0,0,0.00,0.00,0,138287,138287,0,1
#timestamp    event    hideCaster    sourceGUID    sourceName    sourceFlags    sourceRaidFlags    destGUID    destName    destFlags    destRaidFlags

# 0                                      1                   2                  3      4  5                    6                 7     8   9    10         11  12                13              141516171819202122   23   2425   262728
# 9/22 12:40:51.251  SPELL_PERIODIC_HEAL,Player-113-05CD0880,"Cellifalas-Draka",0x511,0x0,Player-113-05CD0880,"Cellifalas-Draka",0x511,0x0,8936,"Regrowth",0x8,0000000000000000,0000000000000000,0,0,0,0,0,0,0,0,0.00,0.00,0,3372,0,0,nil

# 0                                   1                   2                  3      4  5                6   7          8          9    10         11 
# 9/22 12:40:00.941  SPELL_CAST_START,Player-113-05CD0880,"Cellifalas-Draka",0x511,0x0,0000000000000000,nil,0x80000000,0x80000000,8936,"Regrowth",0x8

# 0                                     1                   2                  3      4  5                    6                 7     8   9    10           11  12               13               141516171819202122   23   24
# 9/22 12:44:25.047  SPELL_CAST_SUCCESS,Player-113-05CD0880,"Cellifalas-Draka",0x511,0x0,Player-113-05CD0880,"Cellifalas-Draka",0x511,0x0,18562,"Swiftmend",0x8,0000000000000000,0000000000000000,0,0,0,0,0,0,0,0,0.00,0.00,0


def parse_log(log_contents):
    global debugFlag
    parsed_log = {}
    
    lastTimeStamp = convertTimeToSec(log_contents[len(log_contents)-1])
    
    for line in log_contents:
#        print("evaluating <%s>" % line)
		if convertTimeToSec(line)>lastTimeStamp-10*60:
			fields = line.split(",")  # split the CSV
			if "SPELL_HEAL" in fields[0] or "SPELL_PERIODIC_HEAL" in fields[0]:
				castByPlayer = fields[2][1:-1]   # [1:-1] drops the surrounding quotes
				healedPlayer = fields[6][1:-1]
				spellName    = fields[10][1:-1]
				if fields[28]=="nil": critDivider = 1; 
				else: critDivider = int(fields[28])+1;  # crit divider =1 for no crit; 2 for crit
				healedAmount = int(fields[25])
				if debugFlag == 1: print("healing cast %s by %s to %s for %d with critDivider=%d" % (spellName,castByPlayer,healedPlayer,healedAmount,critDivider));
				healedAmount = healedAmount / critDivider

				if castByPlayer == "Cellifalas-Draka" and healedPlayer == "Cellifalas-Draka":
					if not spellName in parsed_log:
						parsed_log[spellName] = createNewSpellEntry()
						
					if "SPELL_HEAL" in fields[0]:
						parsed_log[spellName]["directHealAmount"] = parsed_log[spellName]["directHealAmount"] + healedAmount
						parsed_log[spellName]["directHealCount"]  = parsed_log[spellName]["directHealCount"] + 1
					
					if "SPELL_PERIODIC_HEAL" in fields[0]:
						parsed_log[spellName]["tickHealAmount"] = parsed_log[spellName]["tickHealAmount"] + healedAmount
						parsed_log[spellName]["tickHealCount"]  = parsed_log[spellName]["tickHealCount"] + 1

			if "SPELL_CAST_SUCCESS" in fields[0]:
				castByPlayer = fields[2][1:-1]   # [1:-1] drops the surrounding quotes
				spellName    = fields[10][1:-1]
				if debugFlag == 1: print("cast success %s by %s" % (spellName,castByPlayer));

				if castByPlayer == "Cellifalas-Draka" :
					if not spellName in parsed_log:
						parsed_log[spellName] = createNewSpellEntry()
					parsed_log[spellName]["castCount"] = parsed_log[spellName]["castCount"] + 1
    
    # do special handling.
    if parsed_log.has_key("Tranquility"):
        parsed_log["Tranquility"]["castCount"] = parsed_log["Tranquility"]["castCount"]/6   # initial cast plus 5 ticks per cast.
        
    return parsed_log;

def createNewSpellEntry():
    parsed_log = {}
    parsed_log["directHealAmount"] = 0
    parsed_log["directHealCount"] = 0
    parsed_log["tickHealAmount"] = 0
    parsed_log["tickHealCount"] = 0
    parsed_log["castCount"] = 0
    
    return parsed_log
    
def dump_summary(log_summary):
    output_data = []
    for spell in ("Efflorescence", "Healing Touch", "Lifebloom", "Regrowth", "Rejuvenation", "Swiftmend", "Wild Growth", "Tranquility"):
        directAmount = 0;
        tickAmount = 0;
        if log_summary[spell]["castCount"] > 0:
            directAmount = log_summary[spell]["directHealAmount"]/log_summary[spell]["castCount"];
            tickAmount   = log_summary[spell]["tickHealAmount"]  /log_summary[spell]["castCount"];

        output_data.append( "%s,%d,%d" % (spell, directAmount, tickAmount) )
    return output_data;

def printOutputList(outputList):
    for index in xrange(len(outputList)):
        print(outputList[index])
        
def setDebugState(newState):
    global debugFlag
    debugFlag = newState;





if __name__ == "__main__":
    if ( len(sys.argv) == 2):
        filename = sys.argv[1]
        
        log_contents = readFile(filename)
        parsed_log = parse_log(log_contents)
        outputList = dump_summary(parsed_log)
        printOutputList(outputList)

        
