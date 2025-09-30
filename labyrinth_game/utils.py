# labyrinth_game/utils.py

import math

from .constants import ROOMS


def describe_current_room(game_state):
    room = game_state['current_room']
    room_data = ROOMS[room]

    print(room_data['description'])
    
    # Выходы с названием комнат
    exits = []
    for direction, dest in room_data['exits'].items():
        exits.append(f"{direction} -> {dest}")
    print("Выходы:", ", ".join(exits))

    if room_data['items']:
        print("Предметы в комнате:", ", ".join(room_data['items']))
    
    # Загадка
    puzzle = room_data.get('puzzle')
    if puzzle and not game_state['puzzle_solved'].get(room, False):
        print("Загадка:", puzzle[0])



def solve_puzzle(game_state):
    current_room = ROOMS[game_state['current_room']]
    puzzle = current_room.get('puzzle')

    if not puzzle:
        print("Загадок здесь нет.")
        return

    question, answer = puzzle
    user_answer = input(f"{question}\nВаш ответ: ").strip().lower()

    # Альтернативные варианты ответа
    valid_answers = [answer.lower()]
    if answer.isdigit():
        valid_answers.append(str(int(answer)))
        # Для чисел словом можно добавить вручную, если хотим
        if answer == "10":
            valid_answers.append("десять")

    if user_answer in valid_answers:
        print("Правильно! Вы решили загадку.")
        # награда в зависимости от комнаты
        if game_state['current_room'] == 'hall':
            game_state['player_inventory'].append('treasure_key')
            print("Вы получили предмет: treasure_key")
        elif game_state['current_room'] == 'library':
            game_state['player_inventory'].append('rusty_key')
            print("Вы получили предмет: rusty_key")

        current_room['puzzle'] = None
    else:
        print("Неверно. Попробуйте снова.")
        if game_state['current_room'] == 'trap_room':
            trigger_trap(game_state)


def show_help(COMMANDS):
    print("Список команд:")
    for cmd, desc in COMMANDS.items():
        print(f"{cmd}: {desc}")

def pseudo_random(seed, modulo):
    """
    Генератор предсказуемых случайных чисел на основе синуса.
    Возвращает целое число в диапазоне [0, modulo)
    """
    x = math.sin(seed * 12.9898) * 43758.5453
    x = x - math.floor(x)  # берем только дробную часть
    return int(x * modulo)

def trigger_trap(game_state):
    print("Ловушка активирована! Пол стал дрожать...")
    inventory = game_state['player_inventory']
    if inventory:
        idx = pseudo_random(game_state['steps_taken'], len(inventory))
        lost_item = inventory.pop(idx)
        print(f"Вы потеряли предмет: {lost_item}")
    else:
        chance = pseudo_random(game_state['steps_taken'], 10)
        if chance < 3:
            print("Вы попали в ловушку и проиграли!")
            game_state['game_over'] = True
        else:
            print("Вам повезло, вы уцелели.")

def random_event(game_state):
    current_room = ROOMS[game_state['current_room']]

    # решаем, произойдет ли событие
    if pseudo_random(game_state['steps_taken'], 10) != 0:
        return  # событие не произошло

    event_type = pseudo_random(game_state['steps_taken'] + 1, 3)

    if event_type == 0:
        print("Вы нашли на полу монетку!")
        current_room['items'].append('coin')
    elif event_type == 1:
        print("Вы слышите странный шорох...")
        if 'sword' in game_state['player_inventory']:
            print("Ваш меч отпугнул существо!")
    elif event_type == 2:
        if (game_state['current_room'] == 'trap_room' and 
        'torch' not in game_state['player_inventory']):
            print("Вы заметили опасность под ногами!")
            trigger_trap(game_state)

def attempt_open_treasure(game_state):
    current_room = game_state['current_room']
    room_items = ROOMS[current_room]['items']
    if 'treasure_chest' not in room_items:
        print("Сундук уже открыт или отсутствует.")
        return
    if ('treasure_key' in game_state['player_inventory'] or 
    'rusty_key' in game_state['player_inventory']):
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room_items.remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
    else:
        ans = input("Сундук заперт. Попробовать ввести код? (да/нет) ").strip().lower()
        if ans == 'да':
            code = input("Введите код: ").strip().lower()
            puzzle_answer = ROOMS[current_room].get('puzzle', {}).get('answer', '')
            if (code == puzzle_answer or 
            code in ROOMS[current_room].get('puzzle', {}).get('alt_answers', [])):
                print("Код верный! Сундук открыт!")
                room_items.remove('treasure_chest')
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
            else:
                print("Неверный код.")
        else:
            print("Вы отступаете от сундука.")
