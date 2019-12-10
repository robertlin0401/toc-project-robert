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
        return text.lower() == "insert"

    def is_going_to_state2(self, event):
        text = event.message.text
        self.command = text.split(',')
        text = self.command[0]
        return text.lower() == "print"

    def is_going_to_state3(self, event):
        text = event.message.text
        self.command = text.split(',')
        text = self.command[0]
        return text.lower() == "delete"

    def on_enter_state1(self, event):
        
        # command error handling
        if len(self.command) < 3:
            reply_token = event.reply_token
            send_text_message(reply_token, "wrong command")
            self.go_back()
            return

        # insert
        count = 0
        for i in self.keyword:
            if i == self.command[1]:
                self.result[count] += '\n' + self.command[2]
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
        
        # command error handling
        if len(self.command) < 2:
            reply_token = event.reply_token
            send_text_message(reply_token, "wrong command")
            self.go_back()
            return
        
        # print all
        if self.command[1] == "all":
            if len(self.keyword) == 0:
                reply_token = event.reply_token
                send_text_message(reply_token, "result not found")
                self.go_back()
                return
            temp = []
            count = 0
            for i in self.keyword:
                temp.append(i)
                temp[count] = temp[count] + ':\n' + self.result[count] + '\n\n'
                count = count + 1
            output = ""
            for i in temp:
                output = output + i
            output = output[0:len(output)-2]
            reply_token = event.reply_token
            send_text_message(reply_token, output)
            self.go_back()
            return

        # print index
        if self.command[1] == "index":
            if len(self.keyword) == 0:
                reply_token = event.reply_token
                send_text_message(reply_token, "result not found")
                self.go_back()
                return
            output = ""
            for i in self.keyword:
                output = output + i + '\n'
            output = output[0:len(output)-1]
            reply_token = event.reply_token
            send_text_message(reply_token, output)
            self.go_back()
            return

        # print target
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
        
        # command error handling
        if len(self.command) < 2:
            reply_token = event.reply_token
            send_text_message(reply_token, "wrong command")
            self.go_back()
            return

        # delete all
        if self.command[1] == "all":
            self.keyword = []
            self.result = []
            reply_token = event.reply_token
            send_text_message(reply_token, "OK")
            self.go_back()
            return

        # delete single result
        if len(self.command) == 3:
            count = 0
            for i in self.keyword:
                if i == self.command[1]:
                    break
                count = count + 1
            if count == len(self.keyword):
                reply_token = event.reply_token
                send_text_message(reply_token, "result not found")
                self.go_back()
                return
            resultIndex = -1
            try:
                resultIndex = int(self.command[2])
            except:
                reply_token = event.reply_token
                send_text_message(reply_token, "wrong command")
                self.go_back()
            if not (resultIndex >= 0 and resultIndex < len(self.result[count].split('\n'))):
                reply_token = event.reply_token
                send_text_message(reply_token, "wrong command")
                self.go_back()
                return
            if len(self.result[count]) != 1:
                temp = self.result[count].split('\n')
                temp.pop(int(self.command[2]))
                self.result[count] = ""
                for i in temp:
                    self.result[count] += i + '\n'
                self.result[count] = self.result[count][0:len(self.result[count])-1]
                reply_token = event.reply_token
                send_text_message(reply_token, "OK")
                self.go_back()
                return

        # delete target
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