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

    def on_enter_state1(self, event): # insert
        
        # command error handling
        insertHelp = "指令：insert,{資料庫},{資料}\n{資料庫}為資料庫名稱，若該名稱不存在，則會自動新建一個資料庫\n{資料}將會被插入指定資料庫的最後，不同筆資料請以換行做為區分"
        if len(self.command) != 3:
            reply_token = event.reply_token
            send_text_message(reply_token, insertHelp)
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

    def on_enter_state2(self, event): # print
        
        # command error handling
        printHelp = "指令：print,{資料庫}\n{資料庫}為資料庫名稱，輸入此指令將會顯示出該資料庫存放的所有資料\n\n指令：print,index\n輸入此指令將會顯示出所有已存在的資料庫\n\n指令：print,all\n輸入此指令將會顯示出所有已存在的資料庫與所有資料"
        if len(self.command) != 2:
            reply_token = event.reply_token
            send_text_message(reply_token, printHelp)
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

    def on_enter_state3(self, event): # delete
        
        # command error handling
        deleteHelp = "指令：delete,{資料庫}\n{資料庫}為資料庫名稱，輸入此指令將會刪除該資料庫與其中的資料\n\n指令：delete,{資料庫},{編號}\n{資料庫}為資料庫名稱\n{編號}為該資料庫中資料的編號，編號從0開始計算\n輸入此指令將會刪除該資料庫中的該筆資料\n\n指令：delete,all\n輸入此指令將會刪除所有已存在的資料庫與所有資料"
        if len(self.command) != 2 and len(self.command) != 3:
            reply_token = event.reply_token
            send_text_message(reply_token, deleteHelp)
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
                send_text_message(reply_token, deleteHelp)
                self.go_back()
            if not (resultIndex >= 0 and resultIndex < len(self.result[count].split('\n'))):
                reply_token = event.reply_token
                send_text_message(reply_token, "result not found")
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