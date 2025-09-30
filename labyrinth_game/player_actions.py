# labyrinth_game/player_actions.py

from .constants import ROOMS
from .utils import describe_current_room, random_event


def show_inventory(game_state):
    print("Ваш инвентарь:")
    for item in game_state['player_inventory']:
        print(f"- {item}")


def move_player(game_state, direction):
    current_room = game_state['current_room']
    room = ROOMS[current_room]

    if direction in room['exits']:
        next_room = room['exits'][direction]

        # Проверка на treasure_room
        if next_room == 'treasure_room':
            if ('treasure_key' in game_state['player_inventory'] or 
            'rusty_key' in game_state['player_inventory']):
                print('Вы используете найденный ключ, чтобы'), 
                ('открыть путь в комнату сокровищ.')
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return  # игрок не может идти

        game_state['current_room'] = next_room
        game_state['steps_taken'] += 1
        describe_current_room(game_state)

        # случайные события после перемещения
        random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state, item_name):
    current_room = game_state['current_room']
    if item_name in ROOMS[current_room]['items']:
        game_state['player_inventory'].append(item_name)
        ROOMS[current_room]['items'].remove(item_name)
        print(f"Вы подняли {item_name}")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    inventory = game_state.get('player_inventory', [])
    current_room = game_state['current_room']

    if item_name not in inventory:
        print(f"У вас нет предмета '{item_name}'.")
        return

    # Пример использования предметов
    if item_name == 'smoked lantern':
        print("Вы зажгли дымный фонарь. Теперь в комнате видно больше деталей.")
        # Можно добавить эффект на игру, например, больше шансов избежать ловушек
        game_state['lantern_lit'] = True

    elif item_name == 'cracked mirror shard':
        if current_room == 'shattered_passage':
            print('Вы направили осколки зеркала и разгадали секрет отражений!'), 
            ('Загадка подсвечена.')
            # Можно автоматически решить загадку при правильном использовании
            game_state['puzzle_solved'][current_room] = True
        else:
            print("Вы посмотрели в осколок зеркала, но ничего особенного не произошло.")

    elif item_name == 'iron key':
        if current_room == 'hollow_chamber':
            print("Вы вставили железный ключ в скрытый замок. Дверь открыта!")
            game_state['hidden_door_open'] = True
        else:
            print("Вы попробовали использовать ключ, но он ни к чему не подошел.")

    else:
        print(f"Вы попытались использовать {item_name}, но ничего не произошло.")


def get_input(prompt="> "):
    return input(prompt).strip().lower()
