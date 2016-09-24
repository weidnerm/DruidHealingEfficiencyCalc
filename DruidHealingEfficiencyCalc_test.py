import unittest

from DruidHealingEfficiencyCalc import readFile, parse_log, dump_summary, setDebugState, convertTimeToSec
#
# test log contents
#
# 1:16    regrowth
# 17:17   ysera gift
# 18:33    regrowth+ysera gift
# 34:51    regrowth+ysera gift
# 52:66    regrowth+ysera gift
# 67:76    rejuv
# 77:86    rejuv
# 87:106    rejuv+ germination
# 107:110   healing touch
# 111:114   healing touch
# 115:117   healing touch
# 118:131   wild growth + Nature's Essence
# 132:145   wild growth + Nature's Essence
# 146:148   swiftmend + living seed
# 149:151   swiftmend + living seed
# 152:154   stray heals from stranger
# 155:197   lifebloom + lots of stray heals
# 198:268   lifebloom + lots of stray
# 269:295   efflorescence + lots of stray
# 296:326   tranquility + barkskin
#


class Test(unittest.TestCase):


    def setUp(self):
        setDebugState(0)


    def tearDown(self):
        pass

    def test_readFile(self):
        log_contents = readFile("test/WoWCombatLog.txt")
        self.assertEqual(326, len(log_contents) )
        # check first few lines
        self.assertEqual('9/22 12:40:00.941  SPELL_CAST_START,Player-113-05CD0880,"Cellifalas-Draka",0x511,0x0,0000000000000000,nil,0x80000000,0x80000000,8936,"Regrowth",0x8', log_contents[0] )
        self.assertEqual('9/22 12:40:02.261  SPELL_HEAL,Player-113-05CD0880,"Cellifalas-Draka",0x511,0x0,Player-113-05CD0880,"Cellifalas-Draka",0x511,0x0,8936,"Regrowth",0x8,0000000000000000,0000000000000000,0,0,0,0,0,0,0,0,0.00,0.00,0,138287,138287,0,1', log_contents[1] )
        self.assertEqual('9/22 12:40:02.261  SPELL_AURA_APPLIED,Player-113-05CD0880,"Cellifalas-Draka",0x511,0x0,Player-113-05CD0880,"Cellifalas-Draka",0x511,0x0,8936,"Regrowth",0x8,BUFF', log_contents[2] )
        # check last line.
        self.assertEqual('9/22 12:46:22.416  SPELL_AURA_REMOVED,Player-113-05CD0880,"Cellifalas-Draka",0x511,0x0,Player-113-05CD0880,"Cellifalas-Draka",0x511,0x0,22812,"Barkskin",0x8,BUFF', log_contents[326-1] )

    def test_parseRegrowth_1(self):
        log_contents = readFile("test/WoWCombatLog.txt")
        parsed_log = parse_log( log_contents[1-1:17] )
        self.assertEqual(2, len(parsed_log))
        self.assertEqual(True ,parsed_log.has_key( "Regrowth"))
        self.assertEqual(True ,parsed_log.has_key( "Ysera's Gift"))
        self.assertEqual(1    ,parsed_log["Ysera's Gift"]["directHealCount"] )
        self.assertEqual(50136,parsed_log["Ysera's Gift"]["directHealAmount"] )
        self.assertEqual(0    ,parsed_log["Ysera's Gift"]["tickHealCount"] )
        self.assertEqual(0    ,parsed_log["Ysera's Gift"]["tickHealAmount"] )
        self.assertEqual(0    ,parsed_log["Ysera's Gift"]["castCount"] )
        self.assertEqual(1    ,parsed_log["Regrowth"]["directHealCount"] )
        self.assertEqual(69143,parsed_log["Regrowth"]["directHealAmount"] )
        self.assertEqual(7    ,parsed_log["Regrowth"]["tickHealCount"] )
        self.assertEqual(23162,parsed_log["Regrowth"]["tickHealAmount"] )
        self.assertEqual(1    ,parsed_log["Regrowth"]["castCount"] )

    def test_parseRegrowth_1_and_2(self):
        log_contents = readFile("test/WoWCombatLog.txt")
        parsed_log = parse_log( log_contents[1-1:33] )
        self.assertEqual(2, len(parsed_log))
        self.assertEqual(True ,parsed_log.has_key( "Regrowth"))
        self.assertEqual(True ,parsed_log.has_key( "Ysera's Gift"))
        self.assertEqual(4    ,parsed_log["Ysera's Gift"]["directHealCount"] )
        self.assertEqual(2    ,parsed_log["Regrowth"]["directHealCount"] )
        self.assertEqual(200542,parsed_log["Ysera's Gift"]["directHealAmount"] )
        self.assertEqual(138286,parsed_log["Regrowth"]["directHealAmount"] )
        self.assertEqual(0    ,parsed_log["Ysera's Gift"]["tickHealCount"] )
        self.assertEqual(14   ,parsed_log["Regrowth"]["tickHealCount"] )
        self.assertEqual(0    ,parsed_log["Ysera's Gift"]["tickHealAmount"] )
        self.assertEqual(46325,parsed_log["Regrowth"]["tickHealAmount"] )
        self.assertEqual(2    ,parsed_log["Regrowth"]["castCount"] )

    def test_parseRegrowth_3_and_4(self):
        log_contents = readFile("test/WoWCombatLog.txt")
        parsed_log = parse_log( log_contents[34-1:66] )
        self.assertEqual(2, len(parsed_log))
        self.assertEqual(True ,parsed_log.has_key( "Regrowth"))
        self.assertEqual(True ,parsed_log.has_key( "Ysera's Gift"))
        self.assertEqual(5    ,parsed_log["Ysera's Gift"]["directHealCount"] )
        self.assertEqual(2    ,parsed_log["Regrowth"]["directHealCount"] )
        self.assertEqual(250678,parsed_log["Ysera's Gift"]["directHealAmount"] )
        self.assertEqual(138286,parsed_log["Regrowth"]["directHealAmount"] )
        self.assertEqual(0    ,parsed_log["Ysera's Gift"]["tickHealCount"] )
        self.assertEqual(14   ,parsed_log["Regrowth"]["tickHealCount"] )
        self.assertEqual(0    ,parsed_log["Ysera's Gift"]["tickHealAmount"] )
        self.assertEqual(46326,parsed_log["Regrowth"]["tickHealAmount"] )
        self.assertEqual(2    ,parsed_log["Regrowth"]["castCount"] )

    def test_parse_Rejuvenation_1(self):
        log_contents = readFile("test/WoWCombatLog.txt")
        parsed_log = parse_log( log_contents[67-1:76] )
        self.assertEqual(1, len(parsed_log))
        self.assertEqual(True ,parsed_log.has_key( "Rejuvenation"))
        self.assertEqual(0    ,parsed_log["Rejuvenation"]["directHealCount"] )
        self.assertEqual(0    ,parsed_log["Rejuvenation"]["directHealAmount"] )
        self.assertEqual(7    ,parsed_log["Rejuvenation"]["tickHealCount"] )
        self.assertEqual(171810,parsed_log["Rejuvenation"]["tickHealAmount"] )
        self.assertEqual(1    ,parsed_log["Rejuvenation"]["castCount"] )

    def test_parse_Rejuvenation_2(self):
        log_contents = readFile("test/WoWCombatLog.txt")
        parsed_log = parse_log( log_contents[77-1:86] )
        self.assertEqual(1, len(parsed_log))
        self.assertEqual(True ,parsed_log.has_key( "Rejuvenation"))
        self.assertEqual(0    ,parsed_log["Rejuvenation"]["directHealCount"] )
        self.assertEqual(0    ,parsed_log["Rejuvenation"]["directHealAmount"] )
        self.assertEqual(7    ,parsed_log["Rejuvenation"]["tickHealCount"] )
        self.assertEqual(171812,parsed_log["Rejuvenation"]["tickHealAmount"] )
        self.assertEqual(1    ,parsed_log["Rejuvenation"]["castCount"] )

    def test_parse_Rejuvenation_and_Germination_1(self):
        log_contents = readFile("test/WoWCombatLog.txt")
        parsed_log = parse_log( log_contents[87-1:106] )
        self.assertEqual(2, len(parsed_log))
        self.assertEqual(True ,parsed_log.has_key( "Rejuvenation"))
        self.assertEqual(True ,parsed_log.has_key( "Rejuvenation (Germination)"))
        self.assertEqual(0    ,parsed_log["Rejuvenation"]["directHealCount"] )
        self.assertEqual(0    ,parsed_log["Rejuvenation"]["directHealAmount"] )
        self.assertEqual(7    ,parsed_log["Rejuvenation"]["tickHealCount"] )
        self.assertEqual(190925,parsed_log["Rejuvenation"]["tickHealAmount"] )  # note that the amount is slightly bigger due to multi-dot buff
        self.assertEqual(0    ,parsed_log["Rejuvenation (Germination)"]["directHealCount"] )
        self.assertEqual(0    ,parsed_log["Rejuvenation (Germination)"]["directHealAmount"] )
        self.assertEqual(7    ,parsed_log["Rejuvenation (Germination)"]["tickHealCount"] )
        self.assertEqual(191856,parsed_log["Rejuvenation (Germination)"]["tickHealAmount"] )
        self.assertEqual(2    ,parsed_log["Rejuvenation"]["castCount"] )  # germination is triggered by rejuv

    def test_parse_Healing_Touch_1(self):
        log_contents = readFile("test/WoWCombatLog.txt")
        parsed_log = parse_log( log_contents[107-1:110] )
        self.assertEqual(1, len(parsed_log))
        self.assertEqual(True ,parsed_log.has_key( "Healing Touch"))
        self.assertEqual(1    ,parsed_log["Healing Touch"]["directHealCount"] )
        self.assertEqual(123797,parsed_log["Healing Touch"]["directHealAmount"] )
        self.assertEqual(0    ,parsed_log["Healing Touch"]["tickHealCount"] )
        self.assertEqual(0    ,parsed_log["Healing Touch"]["tickHealAmount"] )
        self.assertEqual(1    ,parsed_log["Healing Touch"]["castCount"] )

    def test_parse_Healing_Touch_1_to_3(self):
        log_contents = readFile("test/WoWCombatLog.txt")
        parsed_log = parse_log( log_contents[107-1:117] )
        self.assertEqual(1, len(parsed_log))
        self.assertEqual(True ,parsed_log.has_key( "Healing Touch"))
        self.assertEqual(3    ,parsed_log["Healing Touch"]["directHealCount"] )
        self.assertEqual(371394,parsed_log["Healing Touch"]["directHealAmount"] )
        self.assertEqual(0    ,parsed_log["Healing Touch"]["tickHealCount"] )
        self.assertEqual(0    ,parsed_log["Healing Touch"]["tickHealAmount"] )
        self.assertEqual(3    ,parsed_log["Healing Touch"]["castCount"] )

    def test_parse_Wild_Growth_1(self):
        log_contents = readFile("test/WoWCombatLog.txt")
        parsed_log = parse_log( log_contents[118-1:131] )
        self.assertEqual(2, len(parsed_log))
        self.assertEqual(True ,parsed_log.has_key( "Wild Growth"))
        self.assertEqual(0    ,parsed_log["Wild Growth"]["directHealCount"] )
        self.assertEqual(0    ,parsed_log["Wild Growth"]["directHealAmount"] )
        self.assertEqual(9    ,parsed_log["Wild Growth"]["tickHealCount"] )
        self.assertEqual(97772,parsed_log["Wild Growth"]["tickHealAmount"] )
        self.assertEqual(1    ,parsed_log["Wild Growth"]["castCount"] )
        self.assertEqual(True ,parsed_log.has_key( "Nature's Essence"))
        self.assertEqual(1    ,parsed_log["Nature's Essence"]["directHealCount"] )
        self.assertEqual(30949,parsed_log["Nature's Essence"]["directHealAmount"] )
        self.assertEqual(0    ,parsed_log["Nature's Essence"]["tickHealCount"] )
        self.assertEqual(0    ,parsed_log["Nature's Essence"]["tickHealAmount"] )
        self.assertEqual(0    ,parsed_log["Nature's Essence"]["castCount"] )

    def test_parse_Wild_Growth_2(self):
        log_contents = readFile("test/WoWCombatLog.txt")
        parsed_log = parse_log( log_contents[132-1:145] )
        self.assertEqual(2, len(parsed_log))
        self.assertEqual(True ,parsed_log.has_key( "Wild Growth"))
        self.assertEqual(0    ,parsed_log["Wild Growth"]["directHealCount"] )
        self.assertEqual(0    ,parsed_log["Wild Growth"]["directHealAmount"] )
        self.assertEqual(9    ,parsed_log["Wild Growth"]["tickHealCount"] )
        self.assertEqual(97778,parsed_log["Wild Growth"]["tickHealAmount"] )
        self.assertEqual(1    ,parsed_log["Wild Growth"]["castCount"] )
        self.assertEqual(True ,parsed_log.has_key( "Nature's Essence"))
        self.assertEqual(1    ,parsed_log["Nature's Essence"]["directHealCount"] )
        self.assertEqual(30949,parsed_log["Nature's Essence"]["directHealAmount"] )
        self.assertEqual(0    ,parsed_log["Nature's Essence"]["tickHealCount"] )
        self.assertEqual(0    ,parsed_log["Nature's Essence"]["tickHealAmount"] )
        self.assertEqual(0    ,parsed_log["Nature's Essence"]["castCount"] )

    def test_parse_Swiftmend_1(self):
        log_contents = readFile("test/WoWCombatLog.txt")
        parsed_log = parse_log( log_contents[146-1:151] )
        self.assertEqual(1, len(parsed_log))
        self.assertEqual(True ,parsed_log.has_key( "Swiftmend"))
        self.assertEqual(2    ,parsed_log["Swiftmend"]["directHealCount"] )
        self.assertEqual(563278,parsed_log["Swiftmend"]["directHealAmount"] )
        self.assertEqual(0    ,parsed_log["Swiftmend"]["tickHealCount"] )
        self.assertEqual(0    ,parsed_log["Swiftmend"]["tickHealAmount"] )
        self.assertEqual(2    ,parsed_log["Swiftmend"]["castCount"] )

    def test_parse_Stray_heals_1(self):
#        setDebugState(1);
        log_contents = readFile("test/WoWCombatLog.txt")
        parsed_log = parse_log( log_contents[152-1:154] )
        self.assertEqual(0, len(parsed_log))

    def test_parse_Lifebloom_plus_stray_1(self):
        log_contents = readFile("test/WoWCombatLog.txt")
        parsed_log = parse_log( log_contents[155-1:197] )
        self.assertEqual(1, len(parsed_log))
        self.assertEqual(True ,parsed_log.has_key( "Lifebloom"))
        self.assertEqual(1    ,parsed_log["Lifebloom"]["directHealCount"] )
        self.assertEqual(267011/2,parsed_log["Lifebloom"]["directHealAmount"] )
        self.assertEqual(18    ,parsed_log["Lifebloom"]["tickHealCount"] )
        self.assertEqual(159064,parsed_log["Lifebloom"]["tickHealAmount"] )
        self.assertEqual(1    ,parsed_log["Lifebloom"]["castCount"] )

    def test_parse_Lifebloom_plus_stray_2(self):
        log_contents = readFile("test/WoWCombatLog.txt")
        parsed_log = parse_log( log_contents[198-1:268] )
        self.assertEqual(1, len(parsed_log))
        self.assertEqual(True ,parsed_log.has_key( "Lifebloom"))
        self.assertEqual(1    ,parsed_log["Lifebloom"]["directHealCount"] )
        self.assertEqual(267011/2,parsed_log["Lifebloom"]["directHealAmount"] )
        self.assertEqual(18    ,parsed_log["Lifebloom"]["tickHealCount"] )
        self.assertEqual(159064,parsed_log["Lifebloom"]["tickHealAmount"] )
        self.assertEqual(1    ,parsed_log["Lifebloom"]["castCount"] )

    def test_parse_Efflorescence_plus_stray_1(self):
        log_contents = readFile("test/WoWCombatLog.txt")
        parsed_log = parse_log( log_contents[269-1:295] )
        self.assertEqual(1, len(parsed_log))
        self.assertEqual(True ,parsed_log.has_key( "Efflorescence"))
        self.assertEqual(18   ,parsed_log["Efflorescence"]["directHealCount"] )
        self.assertEqual(374389,parsed_log["Efflorescence"]["directHealAmount"] )
        self.assertEqual(0    ,parsed_log["Efflorescence"]["tickHealCount"] )
        self.assertEqual(0    ,parsed_log["Efflorescence"]["tickHealAmount"] )
        self.assertEqual(1    ,parsed_log["Efflorescence"]["castCount"] )

    def test_parse_full_log(self):
        log_contents = readFile("test/WoWCombatLog.txt")
        parsed_log = parse_log( log_contents )
#        for spell in parsed_log: print(spell);
        self.assertEqual(12, len(parsed_log))
        currentSpell = "Efflorescence"
        self.assertEqual(True ,parsed_log.has_key( currentSpell))
        self.assertEqual(18   ,parsed_log[currentSpell]["directHealCount"] )
        self.assertEqual(374389,parsed_log[currentSpell]["directHealAmount"] )
        self.assertEqual(0    ,parsed_log[currentSpell]["tickHealCount"] )
        self.assertEqual(0    ,parsed_log[currentSpell]["tickHealAmount"] )
        self.assertEqual(1    ,parsed_log[currentSpell]["castCount"] )
        currentSpell = "Healing Touch"
        self.assertEqual(True ,parsed_log.has_key( currentSpell))
        self.assertEqual(3    ,parsed_log[currentSpell]["directHealCount"] )
        self.assertEqual(371394,parsed_log[currentSpell]["directHealAmount"] )
        self.assertEqual(0    ,parsed_log[currentSpell]["tickHealCount"] )
        self.assertEqual(0    ,parsed_log[currentSpell]["tickHealAmount"] )
        self.assertEqual(3    ,parsed_log[currentSpell]["castCount"] )
        currentSpell = "Lifebloom"
        self.assertEqual(True ,parsed_log.has_key( currentSpell))
        self.assertEqual(2    ,parsed_log[currentSpell]["directHealCount"] )
        self.assertEqual(267010,parsed_log[currentSpell]["directHealAmount"] )
        self.assertEqual(36   ,parsed_log[currentSpell]["tickHealCount"] )
        self.assertEqual(318128,parsed_log[currentSpell]["tickHealAmount"] )
        self.assertEqual(2    ,parsed_log[currentSpell]["castCount"] )
        currentSpell = "Nature's Essence"
        self.assertEqual(True ,parsed_log.has_key( currentSpell))
        self.assertEqual(2    ,parsed_log[currentSpell]["directHealCount"] )
        self.assertEqual(61898,parsed_log[currentSpell]["directHealAmount"] )
        self.assertEqual(0    ,parsed_log[currentSpell]["tickHealCount"] )
        self.assertEqual(0    ,parsed_log[currentSpell]["tickHealAmount"] )
        self.assertEqual(0    ,parsed_log[currentSpell]["castCount"] )
        currentSpell = "Regrowth"
        self.assertEqual(True ,parsed_log.has_key( currentSpell))
        self.assertEqual(4    ,parsed_log[currentSpell]["directHealCount"] )
        self.assertEqual(276572,parsed_log[currentSpell]["directHealAmount"] )
        self.assertEqual(28   ,parsed_log[currentSpell]["tickHealCount"] )
        self.assertEqual(92651,parsed_log[currentSpell]["tickHealAmount"] )
        self.assertEqual(4    ,parsed_log[currentSpell]["castCount"] )
        currentSpell = "Rejuvenation (Germination)"
        self.assertEqual(True ,parsed_log.has_key( currentSpell))
        self.assertEqual(0    ,parsed_log[currentSpell]["directHealCount"] )
        self.assertEqual(0    ,parsed_log[currentSpell]["directHealAmount"] )
        self.assertEqual(7    ,parsed_log[currentSpell]["tickHealCount"] )
        self.assertEqual(191856,parsed_log[currentSpell]["tickHealAmount"] )
        self.assertEqual(0    ,parsed_log[currentSpell]["castCount"] )
        currentSpell = "Rejuvenation"
        self.assertEqual(True ,parsed_log.has_key( currentSpell))
        self.assertEqual(0    ,parsed_log[currentSpell]["directHealCount"] )
        self.assertEqual(0 ,parsed_log[currentSpell]["directHealAmount"] )
        self.assertEqual(21   ,parsed_log[currentSpell]["tickHealCount"] )
        self.assertEqual(534547,parsed_log[currentSpell]["tickHealAmount"] )
#        self.assertEqual(3    ,parsed_log[currentSpell]["castCount"] )
        currentSpell = "Swiftmend"
        self.assertEqual(True ,parsed_log.has_key( currentSpell))
        self.assertEqual(2    ,parsed_log[currentSpell]["directHealCount"] )
        self.assertEqual(563278,parsed_log[currentSpell]["directHealAmount"] )
        self.assertEqual(0    ,parsed_log[currentSpell]["tickHealCount"] )
        self.assertEqual(0    ,parsed_log[currentSpell]["tickHealAmount"] )
        self.assertEqual(2    ,parsed_log[currentSpell]["castCount"] )
        currentSpell = "Wild Growth"
        self.assertEqual(True ,parsed_log.has_key( currentSpell))
        self.assertEqual(0    ,parsed_log[currentSpell]["directHealCount"] )
        self.assertEqual(0    ,parsed_log[currentSpell]["directHealAmount"] )
        self.assertEqual(18   ,parsed_log[currentSpell]["tickHealCount"] )
        self.assertEqual(195550,parsed_log[currentSpell]["tickHealAmount"] )
        self.assertEqual(2    ,parsed_log[currentSpell]["castCount"] )
        currentSpell = "Ysera's Gift"
        self.assertEqual(True ,parsed_log.has_key( currentSpell))
        self.assertEqual(9    ,parsed_log[currentSpell]["directHealCount"] )
        self.assertEqual(451220,parsed_log[currentSpell]["directHealAmount"] )
        self.assertEqual(0    ,parsed_log[currentSpell]["tickHealCount"] )
        self.assertEqual(0    ,parsed_log[currentSpell]["tickHealAmount"] )
        self.assertEqual(0    ,parsed_log[currentSpell]["castCount"] )
        currentSpell = "Tranquility"
        self.assertEqual(True ,parsed_log.has_key( currentSpell))
        self.assertEqual(5    ,parsed_log[currentSpell]["directHealCount"] )
        self.assertEqual(579372,parsed_log[currentSpell]["directHealAmount"] )
        self.assertEqual(0    ,parsed_log[currentSpell]["tickHealCount"] )
        self.assertEqual(0    ,parsed_log[currentSpell]["tickHealAmount"] )
        self.assertEqual(1    ,parsed_log[currentSpell]["castCount"] )
        currentSpell = "Barkskin"
        self.assertEqual(True ,parsed_log.has_key( currentSpell))
        self.assertEqual(0    ,parsed_log[currentSpell]["directHealCount"] )
        self.assertEqual(0    ,parsed_log[currentSpell]["directHealAmount"] )
        self.assertEqual(0    ,parsed_log[currentSpell]["tickHealCount"] )
        self.assertEqual(0    ,parsed_log[currentSpell]["tickHealAmount"] )
        self.assertEqual(1    ,parsed_log[currentSpell]["castCount"] )

    def test_parse_full_log_extra_time(self):
        log_contents = readFile("test/WoWCombatLog_long.txt")
        parsed_log = parse_log( log_contents )
        outputText = dump_summary(parsed_log)
        self.assertEqual(8, len(outputText))
        self.assertEqual("Efflorescence,378907,0",outputText[0] )
        self.assertEqual("Healing Touch,122424,0",outputText[1] )
        self.assertEqual("Lifebloom,133673,163001",outputText[2] )
        self.assertEqual("Regrowth,68376,23736",outputText[3] )
        self.assertEqual("Rejuvenation,0,175461",outputText[4] )
        self.assertEqual("Swiftmend,278514,0",outputText[5] )
        self.assertEqual("Wild Growth,0,100331",outputText[6] )
        self.assertEqual("Tranquility,572941,0",outputText[7] )
      

    def test_convertTimeToSec(self):
        self.assertEqual(9*31*24*60*60+23*24*60*60+23*60*60+15*60+22,convertTimeToSec("9/23 23:15:22.693") )
        convertTimeToSec















if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
