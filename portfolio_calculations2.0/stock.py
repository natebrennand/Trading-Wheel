

class Stock:

    def __init__(self, tick, mva):
        self.ticker = str(tick)
        self.mva = mva
        self.days = []

    def __str__(self):
        tostring = ""
        tostring += "ticker: {}".format(self.ticker)
        tostring += "\nnum days: {}".format(len(self.days))
        return tostring

    """
    Finds all instances of where the 'over' MVA cross over the other option
    """
    def find_cross_over(self, under, over):

        over_on_top = None      # initiating
        first = self.days[0]
        if first.mva[under] < first.mva[over]:
            over_on_top = True
        else:
            over_on_top = False

        print under, over, over_on_top

        for day in self.days:
            if mva_flip_spots(day, under, over, over_on_top):
                over_on_top = not over_on_top
                if over_on_top:
                    print 'Trade made!'
                else:
                    print 'Sell it!'


def mva_flip_spots(day, under, over, current_state):
    if day.mva[under] < day.mva[over] and not current_state:
        return True     # 'over' cross over 'under'
    if day.mva[under] > day.mva[over] and current_state:
        return True     # 'under' cross over 'over'
    return False


