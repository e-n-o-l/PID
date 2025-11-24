import command_enum

entering = "enter command:\n"

for num,key in enumerate(command_enum.executable.allowed_commands.keys()):
    entering = f"{entering} {num}. {key} \n"

try:
    while "quit" not in (comm := input(entering)):
        try:
            command_enum.executable.command = comm
            command_enum.executable.execute()
        except RuntimeError | ValueError:
            print("error, please try again")
except KeyboardInterrupt:
    print("exiting")
finally:
    command_enum.arduino.close()