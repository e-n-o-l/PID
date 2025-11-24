import additional_decorators
from additional_decorators import *
from command import Command

executable = Command()

@executable.map_func
def help() -> None:
    for _ in executable.descriptions:
        print(_)

@executable.description('prints logs of messages and responses')
@executable.map_func
def history() -> None:
    for _ in additional_decorators.history:
        print(_)

@executable.description('starts the test, which afterwards sends all the log')
@executable.map_func
@send_command(wait_end=True)
@input_val_check('seconds', min_val=0, max_val=60)
def test(seconds: int) -> list:
    return ['T', seconds]

@executable.description('starts program with set parameters')
@executable.map_func
@send_command(wait_end=True)
def start() ->list:
    return ['S', 1]

@executable.description('changes the distance point robot is leading to balance')
@executable.map_func
@send_command()
@input_val_check('distance',min_val=0, max_val=30)
def set_ir(distance: int) -> list:
    return ['s', distance]

@executable.description('changes the servo zero')
@executable.map_func
@send_command()
@input_val_check('distance',min_val=0)
def set_servo_zero(val: int) -> list:
    return ['z', val]

@executable.description('changes the value of kp')
@executable.map_func
@send_command()
@input_val_check('distance',min_val=-10, max_val=10)
def set_kp(kp: int) -> list:
    return ['p', kp]


@executable.description('changes the value of kd')
@executable.map_func
@send_command()
@input_val_check('distance',min_val=-10, max_val=10)
def set_kd(kd: int) -> list:
    return ['d', kd]

@executable.description("changes the value of ki")
@executable.map_func
@send_command()
@input_val_check('distance',min_val=-10, max_val=10)
def set_ki(ki: int) -> list:
    return ['i', ki]