# labyrinth_game/main.py

from labyrinth_game.constants import COMMANDS, ROOMS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    describe_current_room,
    show_help,
)


def process_command(game_state, command_line): 
    command_parts = command_line.strip().split()
    if not command_parts:
        return

    command = command_parts[0].lower()

    if command in ['north', 'south', 'east', 'west']:
        move_player(game_state, command)
    elif command == 'go' and len(command_parts) > 1:
        direction = command_parts[1].lower()
        move_player(game_state, direction)
    elif command == 'look':
        describe_current_room(game_state)
    elif command == 'take' and len(command_parts) > 1:
        take_item(game_state, ' '.join(command_parts[1:]))
    elif command == 'use' and len(command_parts) > 1:
        use_item(game_state, ' '.join(command_parts[1:]))
    elif command == 'inventory':
        show_inventory(game_state)
    elif command == 'solve':
        room = game_state['current_room']
        puzzle = ROOMS[room].get('puzzle')
        if puzzle is None or game_state.get('puzzle_solved', {}).get(room, False):
            print("В этой комнате нет загадки.")
            return

        print(f"Загадка: {puzzle[0]}")
        answer = input("> ").lower().strip()
        correct_answer = puzzle[1].lower().strip()
        if answer == correct_answer:
            print("Вы решили загадку!")
            if 'puzzle_solved' not in game_state:
                game_state['puzzle_solved'] = {}
            game_state['puzzle_solved'][room] = True
            # проверка на победу
            all_puzzles = [r for r in ROOMS if ROOMS[r].get('puzzle')]
            solved_count = sum(1 for r in all_puzzles 
            if game_state['puzzle_solved'].get(r, False))
            if solved_count == len(all_puzzles):
                print("Поздравляем! Вы разгадали все загадки и победили!")
                exit(0)
        else:
            print("Неправильный ответ.")
    elif command == 'help':
        show_help(COMMANDS)
    elif command == 'quit':
        print("Выход из игры...")
        exit()
    else:
        print("Неизвестная команда. Введите 'help' для списка команд.")

def main():
    game_state = {
        "current_room": "entrance",
        "player_inventory": [],
        'steps_taken': 0,
        'puzzle_solved': {}
    }

    print("Добро пожаловать в Лабиринт!")
    describe_current_room(game_state)

    while True:
        command_line = get_input()
        process_command(game_state, command_line)


if __name__ == "__main__":
    main()
