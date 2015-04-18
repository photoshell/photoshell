class Progress(object):

    def __init__(self, num_to_complete=100):
        super(Progress, self).__init__()
        self.num_to_complete = num_to_complete
        self.num_complete = 0

    def advance(self):
        self.num_complete += 1
        return self.percent()

    def percent(self):
        return self.num_complete / self.num_to_complete
