from transitions.extensions import GraphMachine

from utils import send_text_message

class TocMachine(GraphMachine):

    keyword = []
    result = []
    command = []

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_state1(self, event):
        text = event.message.text
        self.command = text.split(',')
        text = self.command[0]
        return text.lower() == "remember"

    def is_going_to_state2(self, event):
        text = event.message.text
        self.command = text.split(',')
        text = self.command[0]
        return text.lower() == "show"

    def is_going_to_state3(self, event):
        text = event.message.text
        self.command = text.split(',')
        text = self.command[0]
        return text.lower() == "forget"

    def on_enter_state1(self, event):
        print("I'm entering state1")
        if len(self.command) < 3:
            reply_token = event.reply_token
            send_text_message(reply_token, "wrong command")
            self.go_back()
            return
        count = 0
        for i in self.keyword:
            if i == self.command[1]:
                self.result[count] = self.command[2]
                reply_token = event.reply_token
                send_text_message(reply_token, "OK")
                self.go_back()
                return
            count = count + 1
        self.keyword.append(self.command[1])
        self.result.append(self.command[2])
        reply_token = event.reply_token
        send_text_message(reply_token, "OK")
        self.go_back()

    def on_exit_state1(self):
        print("Leaving state1")

    def on_enter_state2(self, event):
        print("I'm entering state2")
        if len(self.command) < 2:
            reply_token = event.reply_token
            send_text_message(reply_token, "wrong command")
            self.go_back()
            return
        count = 0
        for i in self.keyword:
            if i == self.command[1]:
                reply_token = event.reply_token
                send_text_message(reply_token, self.result[count])
                self.go_back()
                return
            count = count + 1
        reply_token = event.reply_token
        send_text_message(reply_token, "result not found")
        self.go_back()

    def on_exit_state2(self):
        print("Leaving state2")

    def on_enter_state3(self, event):
        print("I'm entering state3")
        if len(self.command) < 2:
            reply_token = event.reply_token
            send_text_message(reply_token, "wrong command")
            self.go_back()
            return
        count = 0
        for i in self.keyword:
            if i == self.command[1]:
                self.keyword.pop(count)
                self.result.pop(count)
                reply_token = event.reply_token
                send_text_message(reply_token, "OK")
                self.go_back()
                return
            count = count + 1
        reply_token = event.reply_token
        send_text_message(reply_token, "result not found")
        self.go_back()

    def on_exit_state3(self):
        print("Leaving state3")