class Inventaire:
    def __init__(self):
        self.steps = 700
        self.gold = 0
        self.gems = 1
        self.keys = 10
        self.dice = 0
        self.shovel=0
        self.lockpicks=1

    def depenser_step(self) -> bool:
        if self.steps <= 0: return False
        self.steps -= 1; return True

    def payer_gemmes(self, n:int) -> bool:
        if self.gems >= n:
            self.gems -= n; return True
        return False
