import datetime
import random

def september():
    d0 = datetime.date(1993, 9, 1)
    d1 = datetime.date.today()
    delta = d1 - d0
    day = ordinal(delta.days + 1)
    return day

def september_string(day):
    september_strings = [
        "Today is the {} of September, 1993!",
        "It is {} September, 1993.",
        "I greet you on this day: September the {} 1993.",
        "The {} day of The September That Never Ends.",
        "Eternal September: {} day and counting."
    ]
    return random.choice(september_strings).format(day)

SUFFIXES = {1: 'st', 2: 'nd', 3: 'rd'}

def ordinal(num):
    # I'm checking for 10-20 because those are the digits that
    # don't follow the normal counting scheme.
    if 10 <= num % 100 <= 20:
        suffix = 'th'
    else:
        # the second parameter is a default.
        suffix = SUFFIXES.get(num % 10, 'th')
    return str(num) + suffix

missions = {
    'a11': [1969, 7, 16, 13, 32, 0, 0, 'Mission'],
    'tranquility': [1969, 7, 20, 20, 17, 40, 0, 'Tranqility Base'],
    'first_step': [1969, 7, 21, 2, 56, 15, 0, 'First Step']
}

def apollo11():
    mission_delta = mission_time_delta('a11')
    base_delta = mission_time_delta('tranquility')

    #print_mission(missions['a11'][7], mission_delta)
    #print_mission(missions['tranquility'][7], base_delta)
    print_mission('a11')
    print_mission('tranquility')
    print_mission('first_step')

def mission_time_delta(mission_name):
    mission = missions[mission_name]
    d0 = datetime.datetime(mission[0], 
                           mission[1], 
                           mission[2], 
                           mission[3], 
                           mission[4], 
                           mission[5],
                           mission[6],
                           tzinfo=datetime.timezone.utc)
    d1 = datetime.datetime.now(datetime.timezone.utc)
    return d1 - d0
 
def print_mission(mission_name):
    label = missions[mission_name][7]
    time_delta = mission_time_delta(mission_name)
    day, hour, minute, second = time_split(time_delta)
    print('{0:18} T + {1:02d}:{2:02d}:{3:02d}:{4:02d}'.format(label, day, hour, minute, second))


def time_split(td):
    return td.days, td.seconds//3600, (td.seconds//60)%60, td.seconds%60


if __name__ == '__main__':
    apollo11()
