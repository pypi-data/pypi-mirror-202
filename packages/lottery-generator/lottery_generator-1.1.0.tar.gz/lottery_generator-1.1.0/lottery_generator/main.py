import random
import sys
import time
import os
from colorama import init, Fore, Style

init()


def get_ball(amount_num, start_list):
    new_list = []
    for i in range(1, amount_num + 1):
        random.shuffle(start_list)
        num = random.choice(start_list)
        new_list.append(num)
        print(Fore.GREEN + f'шар номер {i} >>>: ' + Fore.WHITE + f'{num}')
        time.sleep(1)
        start_list.remove(num)
    return new_list


def sort_ball(new_list):
    print(Fore.MAGENTA + '\nв порядке выпадения' + Fore.WHITE)
    print(Fore.WHITE + '=' * 20)
    print(', '.join(map(str, new_list)))
    time.sleep(1.5)


def sort_ball_min_max(new_list):
    print(Fore.MAGENTA + '\nпосле сортировки min > max' + Fore.WHITE)
    print(Fore.WHITE + '=' * 26)
    list_sort = sorted(new_list)
    print(*list_sort, sep=', ')
    time.sleep(1.5)


while True:
    os.system('cls')
    print(Fore.RED + '"lottery_generator" генератор лотерей(v 1.1.0)')
    print(Fore.WHITE + '=' * 46)
    amount_num = int(input(Fore.GREEN + 'введите количество номеров для выпадения\n>>>: '))
    amount_all = int(input(Fore.GREEN + 'введите общее количество номеров\n>>>: '))
    time.sleep(1)
    if amount_all <= amount_num:
        print(Fore.CYAN + '\nошибка ввода! ')
        print(Fore.RED + 'общее количество номеров не может\n'
              'быть меньше либо равно количества\n'
              'номеров для выпадения, введите ещё раз\n')
        input(Fore.YELLOW + 'нажмите Enter для продолжения\n')
        continue

    else:
        os.system('cls')
        print(Fore.YELLOW + f'это {amount_num} случайных шаров из барабана  от 1 до {amount_all}: ')
        print(Fore.WHITE + '=' * 45)
        start_list = list(range(1, amount_all + 1))
        time.sleep(1)

        new_list = get_ball(amount_num, start_list)
        sort_ball(new_list)
        sort_ball_min_max(new_list)
        print(Fore.RED + '\nпрограмма завершена!')

        while True:
            ex = input(Fore.YELLOW + 'хотите попробовать ещё раз (y/n) >>>: ')
            if ex == 'y':
                break
            elif ex == 'n':
                time.sleep(1.5)
                print(Fore.CYAN + 'good bye')
                sys.exit()





