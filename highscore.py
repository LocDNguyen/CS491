#CODE FROM https://github.com/cpsc-254-spring-2023/cpsc-254-final-project-team20/blob/main/Final/highscore.py
#CODE FROM https://github.com/cpsc-254-spring-2023/cpsc-254-final-project-team20/blob/main/Final/highscore.py
#CODE FROM https://github.com/cpsc-254-spring-2023/cpsc-254-final-project-team20/blob/main/Final/highscore.py

import os

def get_highscore(file_name):
    text = ''

    if os.path.isfile(file_name):
        with open(file_name, 'r') as text_file:
            text = text_file.read()
    else:
        f = open(file_name, 'w')
        text = 'high:Empty:0,mid:Empty:0,low:Empty:0,lowest:Empty:0'
        f.write(text)
        f.close()

    text_list = text.split(',')

    to_return = {}

    for element in text_list:
        i = element.split(':')
        to_return[i[0]] = [i[1], i[2]]

    return to_return


def write_highscore(file_name, score):
    f = open(file_name, 'w')
    to_write = ''
    for name in ('high', 'mid', 'low', 'lowest'):
        to_write += name
        to_write += ':'
        to_write += str(score.get(name)[0])
        to_write += ':'
        to_write += str(score.get(name)[1])
        to_write += ','

    print(to_write)
    to_write = to_write.rstrip(to_write[-1])
    f.write(to_write)
    f.close()


def set_highscore(file_name, player_name, score):
    scores = get_highscore(file_name)

    old_high = scores.get('high')[0]
    old_mid = scores.get('mid')[0]
    old_low = scores.get('low')[0]
    old_highscore = scores.get('high')[1]
    old_midscore = scores.get('mid')[1]
    old_lowscore = scores.get('low')[1]

    if (int(score) >= int(scores.get('high')[1])):
        print('in1')
        scores['high'][0] = player_name
        scores['high'][1] = score
        scores['mid'][0] = old_high
        scores['mid'][1] = old_highscore
        scores['low'][0] = old_mid
        scores['low'][1] = old_midscore
    elif (int(score) >= int(scores.get('mid')[1])):
        print('in2')
        scores['mid'][0] = player_name
        scores['mid'][1] = score
        scores['low'][0] = old_mid
        scores['low'][1] = old_midscore
    elif (int(score) >= int(scores.get('low')[1])):
        print('in3')
        scores['low'][0] = player_name
        scores['low'][1] = score
        scores['lowest'][0] = old_low
        scores['lowest'][1] = old_lowscore

    write_highscore(file_name, scores)
    print(scores)