class Logger:
    def __init__(self, filename='log.txt'):
        self.filename = filename

    def clear_log(self):
        with open(self.filename, 'w') as file:
            file.writelines([''])

    def write(self, string=None):
        with open(self.filename, 'a') as file:
            file.writelines([string])
