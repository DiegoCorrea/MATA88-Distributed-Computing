from random import choice
import rpyc

GODSHOME = [18861, 18862, 18863, 18864]

def killAGod(counter=10):
    while(len(GODSHOME) > 1):
        bombTime = counter
        god = choice(GODSHOME)
        killedGod = 0
        while(bombTime > 0):
            print ("The God is: ", god)
            print ("The Bomb Time is: ", bombTime)
            conn = rpyc.connect("localhost", god)
            (newClock, newGod) = conn.root.getTheBomb(bombTime, GODSHOME)
            conn.close()
            if (newClock <= 0):
                killedGod = god
            god = newGod
            bombTime = newClock
        print '\n'
        print "God down: ", killedGod
        GODSHOME.remove(killedGod)
        print '\n'
    print "The Winner is: ", GODSHOME