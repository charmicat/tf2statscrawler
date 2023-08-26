# coding=utf-8

from User import User

class ScoreContainer:
    
    def __init__(self):
        self.statByClass = dict({"Soldier":User(),
                   "Spy":User(),
                   "Scout":User(),
                   "Medic":User(),
                   "Engineer":User(),
                   "Demoman":User(),
                   "Heavy":User(),
                   "Pyro":User(),
                   "Sniper":User()})
        
    def __repr__(self):
        return self.statByClass.__repr__()