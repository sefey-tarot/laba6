from random import randint, choice
import string
import os

os.system('cls')
RAM = 64000
QUEUE_MAX = 3000


while True:
    try:
        SECTION_SIZE = int(input("Введите размер разделов (от 10 до 65535): "))
        if 10 < SECTION_SIZE <= 65535:
            break
        else:
            print("Введенный размер не подходит")
            continue
    except ValueError:
        print('Введите целое число')

SECTION_COUNT = RAM // SECTION_SIZE
tasks_ram = []
tasks_queue = []

def create_task(name):
    try:
        with open(name, "wb") as task_file:
            print('Введите размер файла')
            size = int(input())
            task_file.write(bytes([65 for i in range(size)]))
        print("[+] Файл создан", name)
        task = [name, size]
        return task
    except Exception:
        print('[-] Ошибка. Файл не создан')

def generate_task():
    print("Введите имя задачи")
    task_name = str(input())+'.txt'
    try:
        file = open(task_name, 'rb')
        file.close()
    except FileNotFoundError:
        print('Нет файла с именем.')
        task2 = create_task(task_name)
        return task2
    task_size = int(os.path.getsize(task_name))
    task = [task_name, task_size]
    print(task)
    return task



def put_task():
    task = generate_task()
    os.system('cls')
    print(task)
    if task[1] >= int(SECTION_SIZE):
        print('\033[31m\033[40m Данная задача превышает размер раздела и не может быть помещена в память\033[0m\n')
    elif len(tasks_ram) < SECTION_COUNT:
        tasks_ram.append(task)
        return tasks_ram
    if len(tasks_queue) < QUEUE_MAX:
        tasks_queue.append(task)
        return tasks_queue
    else:
        print('\033[31m\033[40m ОЗУ и очередь заняты, задача не будет добавлена. Очистите очередь заданий или ОЗУ\033[0m\n')



def close_task(name):
    name +='.txt'
    for search_task_in_ram in tasks_ram:
        if search_task_in_ram[0] == name:
            tasks_ram.pop(tasks_ram.index(search_task_in_ram))
            if len(tasks_queue) != 0:
                tasks_ram.append(tasks_queue[-1])
                tasks_queue.pop(-1)
            return tasks_ram, tasks_queue
    for search_task_in_queue in tasks_queue:
        if search_task_in_queue[0] == name:
            tasks_queue.pop(tasks_queue.index(search_task_in_queue))
            return tasks_queue



while True:

    print('\033[32m\033[40m Если хотите посмотреть список текущих задач, введите list, для выхода введите exit\033[0m\n')
    new_task = input('Хотите ли вы запустить новую задачу? (Y/n): \n')
    if new_task.lower() == 'n' or new_task.lower() == 'no':
        os.system('cls')
        print(f'Вот список задач в ОЗУ:\n'
              f'{tasks_ram}\n'
              f'Вот список задач в очереди задач:\n'
              f'{tasks_queue}')
        name = input('Введите имя задачи, которую вы хотите закрыть: \n')
        close_task(name)
        continue
    elif new_task.lower() == 'list':
        os.system('cls')
        print(f'Вот список задач в ОЗУ:\n'
              f'{tasks_ram}\n'
              f'Вот список задач в очереди задач:\n'
              f'{tasks_queue}')
        continue
    elif new_task.lower() == 'exit':
        os.system('cls')
        print('До свидания')
        os.system('pause')
        break
    else:
        os.system('cls')
        put_task()
        print(f'Состояние памяти в данный момент: \n'
              f'Количество разделов: {SECTION_COUNT};\n'
              f'количество запущенных задач в ОЗУ: {len(tasks_ram)}; \n'
              f'количество задач в очереди: {len(tasks_queue)}; \n'
              f'Вся память| Свободная память| Занятая память|\n'
              f'   {RAM}    |       {RAM - SECTION_SIZE * len(tasks_ram)}       |     {SECTION_SIZE * len(tasks_ram)} ')
        continue