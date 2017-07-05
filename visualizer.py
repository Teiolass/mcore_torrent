class Visualizer:
    def __init__(self):
        self.messages = {}
        self.check = {}

    def append_message(self, ip, text, priority=0):
        self.messages[ip] = text
        self.show()

    def set_check(self, ip, text):
        self.check[ip] = text
        self.show()


    def show(self):
        print(chr(27) + "[2J")
        for ip, text in self.messages.items():
            try:
                check = self.check[ip]
            except:
                check = 'NO'
            print('{}\t\t{}\t\t{}'.format(ip, check, text))
