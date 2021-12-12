#################################################
#
# Author: Carl Buford

#################################################

import math, copy, string, random
import os

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

class MMGoodBoySolver(object):
    def __init__(self, gb1=[2,2,1,2,2], gb2 = [2,2,1,2,2], cc1=False, cc2=False):
        self.gb1 = gb1
        self.gb2 = gb2
        self.cc1 = cc1
        self.cc2 = cc2

    def doGBThings(self, GB, gbU, mirrorGB=-1):
        atk = GB[3]
        hel = GB[4]
        if mirrorGB == 2:
            GB[3] = 1
            GB[4] = 1
        self.gb1[3] += gbU*atk
        self.gb1[4] += gbU*hel
        self.gb2[3] += gbU*atk
        self.gb2[4] += gbU*hel

    def calcGB(self, goodCharsRem, gb, mirrorGB):
        totalStats = 0
        gbU1 = self.gb1[2]
        gbU2 = self.gb2[2]
        if gb == 1:
            if mirrorGB == 1:
                gbU1 = 1
            totalStats += (self.gb1[3] * gbU1 * goodCharsRem) + \
                          (self.gb1[4] * gbU1 * goodCharsRem)
            self.doGBThings(self.gb1, gbU1, mirrorGB)
        if gb == 2:
            if mirrorGB == 1:
                gbU2 = 1
            totalStats += (self.gb2[3] * gbU2 * goodCharsRem) + \
                          (self.gb2[4] * gbU2 * goodCharsRem)
            self.doGBThings(self.gb2, gbU2, mirrorGB)
        return totalStats

    def calcStatsGiven(self, goodCharsRem, cc, mirrorCC):
        totalStats = 0
        if cc == 1:
            totalStats += (self.gb1[3] * self.gb1[2] * goodCharsRem) + \
                          (self.gb1[4] * self.gb1[2] * goodCharsRem)
            self.doGBThings(self.gb1, self.gb1[2])
            if (not mirrorCC and self.cc1):
                totalStats += (self.gb1[3] * self.gb1[2] * goodCharsRem) + \
                              (self.gb1[4] * self.gb1[2] * goodCharsRem)
                self.doGBThings(self.gb1, self.gb1[2])
        if cc == 2:
            totalStats += (self.gb1[3] * self.gb1[2] * goodCharsRem) + \
                          (self.gb1[4] * self.gb1[2] * goodCharsRem)
            self.doGBThings(self.gb1, self.gb1[2])
            totalStats += (self.gb2[3] * self.gb2[2] * goodCharsRem) + \
                          (self.gb2[4] * self.gb2[2] * goodCharsRem)
            self.doGBThings(self.gb2, self.gb2[2])
            if (not mirrorCC and self.cc2):
                totalStats += (self.gb1[3] * self.gb1[2] * goodCharsRem) + \
                              (self.gb1[4] * self.gb1[2] * goodCharsRem)
                self.doGBThings(self.gb1, self.gb1[2])
                totalStats += (self.gb2[3] * self.gb2[2] * goodCharsRem) + \
                          (self.gb2[4] * self.gb2[2] * goodCharsRem)
                self.doGBThings(self.gb2, self.gb2[2])
        return totalStats

    def simCombatGB(self, cc1Suic=True, cc2Suic=True, boots=False):
        statsGiven = 0
        goodCharsRem = 7
        posList = [1,2,3,4]
        # 2 is alive, 1 is mirror 0 is dead
        aliveList = [2,2,2,2]
        attackerPos = 0
        firstAtkList = [False, True]
        if boots:
            firstAtkList = [True]
        firstAtk = random.choice(firstAtkList)
        if firstAtk:
            newPosList = []
            while attackerPos < 2:
                while aliveList[attackerPos] == 0 and attackerPos < 2:
                    attackerPos += 1
                if attackerPos >= 2:
                    break
                mirrorGB = aliveList[attackerPos]
                goodCharsRem = 3
                for i in range(len(aliveList)):
                    if aliveList[i] > 0:
                        goodCharsRem += 1
                statsGiven += self.calcGB(goodCharsRem, attackerPos+1, mirrorGB)
                aliveList[attackerPos] -= 1
                newPosList = []
                for i in range(len(aliveList)):
                    if aliveList[i] != 0:
                        newPosList.append(i)
                atkPos = random.choice(newPosList)
                if atkPos == 0 or atkPos == 1:
                    mirrorGB = aliveList[atkPos]
                    statsGiven += self.calcGB(goodCharsRem, atkPos+1, mirrorGB)
                aliveList[atkPos] -= 1
                newPosList = []
                for i in range(len(aliveList)):
                    if aliveList[i] != 0:
                        newPosList.append(i)
        else:
            newPosList = []
            while attackerPos < 2:
                while aliveList[attackerPos] == 0 and attackerPos < 2:
                    attackerPos += 1
                if attackerPos >= 2:
                    break
                newPosList = []
                for i in range(len(aliveList)):
                    if aliveList[i] != 0:
                        newPosList.append(i)
                atkPos = random.choice(newPosList)
                if atkPos == 0 or atkPos == 1:
                    mirrorGB = aliveList[atkPos]
                    statsGiven += self.calcGB(goodCharsRem, atkPos+1, mirrorGB)
                aliveList[atkPos] -= 1
                newPosList = []
                for i in range(len(aliveList)):
                    if aliveList[i] != 0:
                        newPosList.append(i)
                while aliveList[attackerPos] == 0 and attackerPos < 2:
                    attackerPos += 1
                if attackerPos >= 2:
                    break
                mirrorGB = aliveList[attackerPos] == 1
                statsGiven += self.calcGB(goodCharsRem, attackerPos+1, mirrorGB)
                aliveList[attackerPos] -= 1
                newPosList = []
                for i in range(len(aliveList)):
                    if aliveList[i] != 0:
                        newPosList.append(i)
        statsGiven += (self.gb1[3] * self.gb1[2] * 2) + (self.gb1[4] * self.gb1[2] * 2)
        self.doGBThings(self.gb1, self.gb1[2])
        statsGiven += (self.gb2[3] * self.gb2[2]) + (self.gb2[4] * self.gb2[2])
        self.gb1[3] = self.gb1[0]
        self.gb1[4] = self.gb1[1]
        self.gb2[3] = self.gb2[0]
        self.gb2[4] = self.gb2[1]
        return statsGiven

    def simCombatCC(self, cc1Suic=True, cc2Suic=True, crown=False, boots=False):
        statsGiven = 0
        goodCharsRem = 5
        if crown:
            goodCharsRem = 7
        posList = [1,2,3,4]
        # 2 is alive, 1 is mirror 0 is dead
        aliveList = [2,2,2,2]
        attackerPos = 0
        firstAtkList = [False, True]
        if boots:
            firstAtkList = [True]
        firstAtk = random.choice(firstAtkList)
        if firstAtk:
            newPosList = []
            while attackerPos < 2:
                while aliveList[attackerPos] == 0 and attackerPos < 2:
                    attackerPos += 1
                if attackerPos >= 2:
                    break
                mirrorCC = aliveList[attackerPos] == 1
                goodCharsRem = 3
                for i in range(len(aliveList)):
                    if crown:
                        if aliveList[i] > 0:
                            goodCharsRem += 1
                    else:
                        if aliveList[i] > 0 and i > 1:
                             goodCharsRem += 1
                statsGiven += self.calcStatsGiven(goodCharsRem, attackerPos+1, mirrorCC)
                aliveList[attackerPos] -= 1
                newPosList = []
                for i in range(len(aliveList)):
                    if aliveList[i] != 0:
                        newPosList.append(i)
                atkPos = random.choice(newPosList)
                aliveList[atkPos] -= 1
                newPosList = []
                for i in range(len(aliveList)):
                    if aliveList[i] != 0:
                        newPosList.append(i)
        else:
            newPosList = []
            while attackerPos < 2:
                while aliveList[attackerPos] == 0 and attackerPos < 2:
                    attackerPos += 1
                if attackerPos >= 2:
                    break
                newPosList = []
                for i in range(len(aliveList)):
                    if aliveList[i] != 0:
                        newPosList.append(i)
                atkPos = random.choice(newPosList)
                aliveList[atkPos] -= 1
                newPosList = []
                for i in range(len(aliveList)):
                    if aliveList[i] != 0:
                        newPosList.append(i)
                while aliveList[attackerPos] == 0 and attackerPos < 2:
                    attackerPos += 1
                if attackerPos >= 2:
                    break
                mirrorCC = aliveList[attackerPos] == 1
                statsGiven += self.calcStatsGiven(goodCharsRem, attackerPos+1, mirrorCC)
                aliveList[attackerPos] -= 1
                newPosList = []
                for i in range(len(aliveList)):
                    if aliveList[i] != 0:
                        newPosList.append(i)
        statsGiven += (self.gb1[3] * self.gb1[2] * 2) + (self.gb1[4] * self.gb1[2] * 2)
        self.doGBThings(self.gb1, self.gb1[2])
        statsGiven += (self.gb2[3] * self.gb2[2]) + (self.gb2[4] * self.gb2[2])
        self.gb1[3] = self.gb1[0]
        self.gb1[4] = self.gb1[1]
        self.gb2[3] = self.gb2[0]
        self.gb2[4] = self.gb2[1]
        return statsGiven

    def simEV(self):
        totalStats = 0
        for i in range(1000):
            totalStats += self.simCombatCC(crown=False, boots=False)
        return totalStats / 1000

    def simEVGB(self):
        totalStats = 0
        for i in range(1000):
            totalStats += self.simCombatGB(boots=False)
        return totalStats / 1000

#########################################
# Test Function
#########################################

def testSolveGB():
    evListCC = 0
    evListGB = 0
    test = MMGoodBoySolver(gb1=[35,5,1,35,5],gb2=[5,5,1,5,5])
    for i in range(200):
        ev = test.simEV()
        evListCC += ev
    for i in range(200):
        ev = test.simEVGB()
        evListGB += ev
    print(evListCC / 200, evListGB / 200)


#################################################
# testAll and main
#################################################

def testAll():
    testSolveGB()

def main():
    testAll()

if (__name__ == '__main__'):
    main()
