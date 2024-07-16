import bpy
import os
import random
import json
import csv
import math
import openpyxl
#import find_way
from datetime import datetime


def work_with_dir():
    os.chdir('D:\\teach\\diplom\\work')
    dir = ('D:\\teach\\diplom\\work\\tiles\\')
    files = os.listdir(os.getcwd() + '\\tiles\\')
    blend_files = []
    for file in files:
        if file.endswith('.blend'):
            blend_files.append(dir + file)
    return blend_files


def create_folder_with_current_datetime():
    global original_directory
    # Получаем текущую дату и время
    now = datetime.now()
    original_directory = os.getcwd() 
    # Форматируем дату и время без секунд
    folder_name = now.strftime("%Y-%m-%d_%H-%M")
    # Создаем папку с формированным наименованием, если она не существует
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
        os.chdir(folder_name)
        os.mkdir('cam0')
        os.mkdir('cam1')
        os.mkdir('state_groundtruth_estimate0')
        os.chdir(original_directory)
    return folder_name


def matrix():
    list_right = [[list_cvs[row][col] for row in range(len(list_cvs))] for col in range(len(list_cvs[0]) - 1, -1, -1)]
    return list_right


def list_for_cvs():
    global list_cvs


def ready_txt_file():
    os.chdir(work_folder)

    end_matrix = matrix()
    with open(work_folder + '_matrix_tiles.txt', 'w') as f:
        for item in end_matrix:
            f.write(f'{item}\n')
        f.close()

def delete_all_cameras():
    # Собираем все камеры
    cameras = [obj for obj in bpy.context.scene.objects if obj.type == 'CAMERA']

    # Активируем каждый объект камеры и удаляем его
    for cam in cameras:
        bpy.data.objects.remove(cam, do_unlink=True)


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()


def take_tile(file_path, rotate_on, i, h):
    global list_cvs
    file_name = os.path.basename(file_path)
    file_name = os.path.splitext(file_name)[0]
    midlle = list_cvs[i]
    record = file_name[0] + str(int(rotate_on))
    midlle[h] = record

    imported_objects = []
    with bpy.data.libraries.load(file_path) as (data_from, data_to):
        data_to.objects = data_from.objects
    for obj in data_to.objects:
        bpy.context.collection.objects.link(obj)
        imported_objects.append(obj)
    for obj in imported_objects:
        inital_location = obj.location.copy()
        obj.rotation_euler.z -= 1.5708 * rotate_on
        obj.location = (inital_location.x + 2 * i, inital_location.y + 2 * h, inital_location.z)
    #bpy.context.collection.objects.unlink(obj)


def rand_tile(probably):
    tile = random.randint(0, len(probably) - 1)
    return probably[tile]


def json_file_up(main):
    with open(f'D:/teach/diplom/work/json/{int(main)}.json', 'r') as file:
        data = json.load(file)
    id_rotate = data["face_profiles"]
    return id_rotate[0]["potential_neighbours"]


def json_file_right(main):
    with open(f'D:/teach/diplom/work/json/{int(main)}.json', 'r') as file:
        data = json.load(file)
    id_rotate = data["face_profiles"]
    return id_rotate[1]["potential_neighbours"]


def check_rotate(cell, rotate):
    cell = str(cell)
    cell_1 = int(str(cell)[1]) + int(rotate)
    cell = cell[0] + str(cell_1)
    if int(cell[1]) > 3:
        cell = cell[0] + str(int(cell[1]) + int(rotate))
    if cell[0] == '2':
        cell = cell[0] + str(int(cell[1]) % 2)
    else:
        cell = cell[0] + str(int(cell[1]) % 4)
    return cell


def rotate_cell(list_cells, rotate):
    empty = []
    for element in list_cells:
        element_end = check_rotate(element, rotate)
        empty.append(element_end)
    return list_cells


def add_next(file_paths, i, h):
    global main
    cell = str(i) + str(h)
    cell1 = list_cvs[i]
    cell2 = list_cvs[i - 1]
    cell1, cell2 = cell1[h - 1], cell2[h]
    neighbours1 = json_file_up(cell1[0])
    neighbours2 = json_file_right(cell2[0])
    neighbours1 = rotate_cell(neighbours1, cell1[1])
    neighbours2 = rotate_cell(neighbours2, cell2[1])
    rotate_cell(neighbours2, cell2[1])
    neighbours = [value for value in neighbours1 if value in neighbours2]
    random_element = str(random.choice(neighbours))
    main = str(random_element[0])
    rotate = random_element[-1]

    return main, rotate

def shift_matrix(input_str):
    global path_cells
    path_right = []
    index_row = int(input_str[0]) - 1
    shift_amount = int(input_str[1])
    selected_row = path_cells[index_row]
    row_str = ''.join(selected_row)
    shifted_str = row_str[-shift_amount:] + row_str[:-shift_amount]
    for element in shifted_str:
        path_right.append(element)
    return path_right


# Функция для проверки допустимости хода
def is_move_possible(current_pos, path_move, matrix_end):
    possible_moves = []
    x, y = current_pos
    if path_move[0] == '1':
        if x - 1 >= 0:
            possible_moves.append([x - 1, y])
            # Вверх
    if path_move[1] == '1':
        if y + 1 < len(matrix_end[0]):
            possible_moves.append([x, y + 1])
            # Вправо
    if path_move[2] == '1':
        if x + 1 < len(matrix_end):
            possible_moves.append([x + 1, y])
            # Вниз
    if path_move[3] == '1':
        if y - 1 >= 0:
            possible_moves.append([x, y - 1])
            # Влево
    return possible_moves

def get_timestamp():
    now = datetime.now()
    timestamp = int(now.timestamp() * 1_000)  # Переводим в миллисекунды
    return timestamp

def create_matrix_way(hight_cell, matrix_end_way, work_folder):
    global path_cells
    path_cells = [['1', '0', '0', '1'],
                  ['0', '1', '0', '1'],
                  ['0', '1', '1', '1'],
                  ['1', '1', '1', '1']]
    matrix = []
    for i in range(hight_cell + 1):
        matrix_midle = []
        for h in range(hight_cell + 1):
            matrix_midle.append('0')
        matrix.append(matrix_midle)
    print
    start = [hight_cell, 1]
    all_step = []
    next_step = []
    while True:
        midle = matrix_end_way[start[0]][start[1]]
        path_cell = shift_matrix(midle)
        possible = is_move_possible(start, path_cell, matrix_end_way)
        t = 0
        while t < len(possible):
            i, h = possible[t]
            if matrix[i][h] == '0':
                possible_cell = is_move_possible([i, h], shift_matrix(matrix_end_way[i][h]), matrix_end_way)
                if start in possible_cell:
                    matrix[i][h] = '1'
                    next_step.append(start)
                    all_step.append(start)
                    start = [i, h]

                    break
                else:
                    t += 1
            else:
                t += 1
        if t == len(possible):
            if not next_step:
                break
            else:
                all_step.append(start)
                start = next_step[-1]
                next_step.pop()

    with open(work_folder + '_matrix_way.txt', 'w') as f:
        for item in all_step:
            f.write(f'{item}\n')
        f.close()

# Функция для вычисления поворота на основе направления движения
def calculate_rotation(from_coord, to_coord):
    delta_x = to_coord[0] - from_coord[0]
    delta_y = to_coord[1] - from_coord[1]
    
    angle = math.atan2(delta_y, delta_x) + 1.5708 * 2
    return angle



def create_sun(location, color, energy):
    # Создаем новый источник света
    light_data = bpy.data.lights.new(name="Sun Light", type='SUN')
    light_data.energy = energy  # Устанавливаем мощность

    # Устанавливаем цвет света (RGB)
    light_data.color = color

    # Создаем объект, который будет держать источник света
    light_object = bpy.data.objects.new(name="Sun Light", object_data=light_data)

    # Устанавливаем координаты объекта
    light_object.location = location

    # Ссылаемся на контекст сцены
    bpy.context.collection.objects.link(light_object)
    return light_object

clear_scene()
file_paths = work_with_dir()
work_folder = create_folder_with_current_datetime()
list_cvs = []
range_x, range_y = 5, 5
for i in range(range_x + 1):
    clear_list = []
    for h in range(range_y + 1):
        clear_list.append('0')
    list_cvs.append(clear_list)

color = (1.0, 1.0, 0.75)  # Цвет солнца (RGB, от 0.0 до 1.0)
energy = 0.8

take_tile(file_paths[0], 1, 0, 0)
create_sun((0, 0, 10) , color, energy)  #4ртая движение вверх, 3 в право
take_tile(file_paths[0], 2, 0, range_x)
create_sun((0, range_x*2, 10) , color, energy)
take_tile(file_paths[0], 0, range_y, 0)
create_sun((range_y*2, 0, 10) , color, energy)
take_tile(file_paths[0], 3, range_y, range_x)
create_sun((range_x*2, range_y*2, 10) , color, energy)

for i in range(range_x - 1):
    take_tile(file_paths[2], 3, 0, i + 1)
    take_tile(file_paths[2], 1, range_y, i + 1)

for i in range(range_y - 1):
    take_tile(file_paths[2], 0, i + 1, range_x)
    take_tile(file_paths[2], 2, i + 1, 0)

main = 1
for i in range(range_x - 1):
    for h in range(range_y - 1):
        main, rotate = add_next(file_paths, i, h)
        take_tile(file_paths[int(main) - 1], float(rotate), h + 1, i + 1)
ready_txt_file()
bpy.context.view_layer.update()



end_matrix_way = matrix()
create_matrix_way(range_x, end_matrix_way, work_folder)
start_height = 1.0  # Начальная высота камеры
frame_interval = 40  # Интервал между ключевыми кадрами
fov = 50  # Поле зрения камеры (в градусах)
start_rotation_x = 90  # Начальный поворот камеры по оси X в градусах
start_rotation_y = 0  # Начальный поворот камеры по оси Y в градусах
start_rotation_z = 0  # Начальный поворот камеры по оси Z в градусах

with open(work_folder + '_matrix_way.txt', 'r') as file:
    # Считываем строки из файла
    lines = file.readlines()

# Задаем пустой список для координат
coordinates = []

# Обрабатываем каждую строку из файла
for line in lines:

    # Убираем пробельные символы по краям строки и убираем квадратные скобки
    stripped_line = line.strip()[1:-1]
    # Разделяем строку по запятой, чтобы получить два числа
    x, y = map(int, stripped_line.split(','))
    # Добавляем пару чисел как список в список координат
    coordinates.append([x, y])
# Удалить все объекты из сцены
for z in range(2):
    focal_length = 10
    render_with = 1980
    hender_height = 1024

# Создание камеры
    bpy.ops.object.camera_add(location=(0, 0.2 * z, start_height))
    camera = bpy.context.active_object

# Настройка параметров камеры
    camera.data.angle = math.radians(fov)
    camera.data.lens = focal_length


# Установка начального поворота камеры
    camera.rotation_euler = (
        math.radians(start_rotation_x),
        math.radians(start_rotation_y),
        math.radians(start_rotation_z)
    )


    bpy.context.scene.render.resolution_x = render_with
    bpy.context.scene.render.resolution_y = hender_height

    # Включение автоматической вставки ключевых кадров для объекта камеры
    bpy.context.view_layer.objects.active = camera
    camera.select_set(True)
    bpy.context.scene.frame_set(0)  # Начало с 0 кадра



    # Установка начальной позиции камеры
    camera.location.x = 2 + 0.2 * z
    camera.location.y = 0
    camera.location.z = start_height  # Высота камеры



    # Перемещаем камеру по координатам с интервалом в frame_interval кадров
    frame_number = 0

    for i in range(0, len(coordinates)):
        from_coord = coordinates[i - 1]
        to_coord = coordinates[i]
        
        # Перемещение камеры
        camera.location.x = (to_coord[1]) * 2  + 0.2 * z
        camera.location.y = (range_x - to_coord[0]) * 2
        camera.location.z = start_height  # Высота камеры
        
        # Расчет новой ориентации камеры
        rotation_angle = calculate_rotation(from_coord, to_coord)
        camera.rotation_euler[2] = rotation_angle
        # Вставка ключевых кадров для перемещения и вращения
        camera.keyframe_insert(data_path="location", frame=frame_number)
        camera.keyframe_insert(data_path="rotation_euler", frame=frame_number)
        
        frame_number += frame_interval

    # Установка камеры как активной сцены
    bpy.context.scene.camera = camera

    # Установка конечного кадра временной шкалы анимации
    bpy.context.scene.frame_end = frame_number - frame_interval


    bpy.context.scene.render.image_settings.file_format = 'JPEG'
    bpy.context.scene.render.resolution_percentage = 100  # Процент разрешения
    os.chdir(original_directory + '\\' + work_folder + '\\' + f'cam{z}')
    os.mkdir('data')
    # Задайте путь к папке вывода
    output_folder = original_directory + '\\' + work_folder + '\\' + f'cam{z}\\data\\' 

    # Функция для получения текущего TIMESTAMP в формате Unix-времени
    

    # Количество кадров для рендера (от 1 до 5)
    frame_start = 1

    wb = openpyxl.Workbook()
    ws = wb.active
    save_list = []
    # Устанавливаем имя для листа
    ws.title = "data"
    # Рендер каждого кадра
    if z == 0:
        for frame in range(frame_start, frame_number):
            bpy.context.scene.frame_set(frame)
            timestamp = get_timestamp()
            filepath = bpy.path.abspath(f'{output_folder}{timestamp}.jpeg')
            bpy.context.scene.render.filepath = filepath
            save_list.append(f'{timestamp}')
            ws.append([f'{timestamp}, {timestamp}.jpeg'])
            bpy.ops.render.render(write_still=True)
        wb.save(original_directory + '\\' + work_folder + '\\' + f'cam{z}\data.xlsx')
        wb.save(original_directory + '\\' + work_folder + '\\' + f'cam{z+1}\data.xlsx')
    else:
        print(save_list)
        for frame in range(frame_start, frame_number):
            bpy.context.scene.frame_set(frame)
            timestamp = get_timestamp()
            filepath = bpy.path.abspath(f'{output_folder}{save_list[frame]}.jpeg')
            bpy.context.scene.render.filepath = filepath
            bpy.ops.render.render(write_still=True)
    # Вызываем функцию удаления камер
    delete_all_cameras()
    