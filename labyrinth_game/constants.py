# labyrinth_game/constants.py

ROOMS = {
    'entrance': {
        'description': (
            'Вы стоите у руин древнего замка. Туман густым плащом окутывает землю, '
            'а из глубины леса доносится тихий стон ветра.'
        ),
        'exits': {'north': 'wailing_hall', 'east': 'shattered_passage'},
        'items': ['smoked lantern'],
        'puzzle': None,
    },
    'wailing_hall': {
        'description': (
            'Огромный зал с рваными гобеленами, на которых изображены плачущие фигуры. '
            'Стены пропитаны старой магией и горькой тоской.'
        ),
        'exits': {
        'south': 'entrance',
        'west': 'hollow_chamber',
        'north': 'ashen_throne',
        },
        'items': ['soul vial'],
        'puzzle': ('Сколько слез на последнем гобелене?', '9'),
    },
    'shattered_passage': {
        'description': (
            'Коридор, пол которого завален осколками камня. В темноте слышен скрежет — '
            'будто что-то за вами ползет.'
        ),
        'exits': {'west': 'entrance'},
        'items': ['cracked mirror shard'],
        'puzzle': ('Составьте слово из трёх отражений зеркал', 'рак'),
    },
    'hollow_chamber': {
        'description': (
            'Комната с гигантским пустым колодцем в центре.,', 
            'По стенам висят цепи, дрожащие без ветра.'
        ),
        'exits': {'east': 'wailing_hall', 'north': 'oblivion_altar'},
        'items': ['iron key', 'phantom bell'],
        'puzzle': ('Что прозвучит, если вы позвоните в колокол трижды?', 'тишина'),
    },
    'oblivion_altar': {
        'description': (
            'Темная комната с алтарем, покрытым черной пылью. На стенах тлеют руны, '
            'от которых веет холодом.'
        ),
        'exits': {'south': 'hollow_chamber'},
        'items': ['shadow relic', 'vial of night essence'],
        'puzzle': ('Назовите символ, что удерживает ночь в пределах зала', 'ворон'),
    },
    'ashen_throne': {
        'description': (
            'Тронный зал, где трон обуглен и покрыт пеплом. Воздух тяжёлый, '
            'и каждое ваше движение эхом отдаётся в пустоте.'
        ),
        'exits': {'south': 'wailing_hall'},
        'items': ['cursed crown', 'ember shard'],
        'puzzle': ('Кого вознесли на этом троне до падения замка?', 'король-тень'),
    },
}

COMMANDS = {
    "go <direction>": "перейти в направлении (north/south/east/west)",
    "north/south/east/west": "двигаться в направлении",
    "look": "осмотреть текущую комнату",
    "take <item>": "поднять предмет",
    "use <item>": "использовать предмет из инвентаря",
    "inventory": "показать инвентарь",
    "solve": "попытаться решить загадку в комнате",
    "quit": "выйти из игры",
    "help": "показать это сообщение"
}
