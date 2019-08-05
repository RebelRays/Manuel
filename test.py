Me = "set4170"




def LoopRegulateSpeed():
    print("Yay baby")


from threading import Timer

t = Timer(1, LoopRegulateSpeed)
t.start()




use_command_line = input("Your command:")
user_commands = use_command_line.split(' ')

for user_command in user_commands:
    print("user_command : " + user_command)
    #sleep(0.5)

print("donE")




