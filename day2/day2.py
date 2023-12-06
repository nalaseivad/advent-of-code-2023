import sys
import re


cubes = { 'red' : 12, 'blue' : 14, 'green' : 13 }

debug = 0

def debug_print(s):
  if debug:
    print(s)


def process_game_1(line):
  def process_color(color_data):
    pattern = r'^(\d+)\s+(\w+)$'
    match = re.match(pattern, color_data)
    if match:
      color_count, color = match.groups()
      color_count = int(color_count)
      debug_print(f"COLOR: '{color_count}' '{color}'")
      if color_count > cubes[color]:
        return False
      return True
    else:
      raise Exception(f"color_data does not match regex: '{color_data}'")

  def process_draw(draw_data):
    colors = re.split(r',\s*', draw_data)
    debug_print('DRAW:')
    for color in colors:
      if not process_color(color):
        return False
    return True

  def process_game_data(game_data):
    draws = re.split(r';\s*', game_data)
    for draw in draws:
      if not process_draw(draw):
        return False
    return True

  pattern = r'^Game (\d+):\s+(.+)\s*$'
  match = re.match(pattern, line)
  if match:
    game_number, game_data = match.groups()
    game_number = int(game_number)
    debug_print(f'GAME {game_number}: {game_data}')
    if process_game_data(game_data):
      return game_number
    return 0
  else:
    raise Exception(f'Line does not match regex: {line}')


def process_game_2(line):
  def process_color(color_data):
    pattern = r'^(\d+)\s+(\w+)$'
    match = re.match(pattern, color_data)
    if match:
      color_count, color = match.groups()
      color_count = int(color_count)
      debug_print(f"COLOR: '{color_count}' '{color}'")
      return (color, color_count)
    else:
      raise Exception(f"color_data does not match regex: '{color_data}'")

  def process_draw(draw_data):
    colors = re.split(r',\s*', draw_data)
    debug_print('DRAW:')
    cube_counts = { }
    for color in colors:
      color, color_count = process_color(color)
      cube_counts[color] = color_count
    return cube_counts

  def process_game_data(game_data):
    draws = re.split(r';\s*', game_data)
    cube_counts = { 'red' : 0, 'blue' : 0, 'green' : 0 }
    for draw in draws:
      draw_cube_counts = process_draw(draw)
      for key, value in draw_cube_counts.items():
        cube_counts[key] = max(cube_counts[key], value)
    return cube_counts

  pattern = r'^Game (\d+):\s+(.+)\s*$'
  match = re.match(pattern, line)
  if match:
    game_number, game_data = match.groups()
    game_number = int(game_number)
    debug_print(f'GAME {game_number}: {game_data}')
    cube_counts = process_game_data(game_data)
    product = 1
    for count in cube_counts.values():
      product *= count
    return product
  else:
    raise Exception(f'Line does not match regex: {line}')


def part_n(process_line_fn, file_path):
  with open(file_path, 'r') as file:
    result = sum(map(process_line_fn, file))
    print(result)


def part_1(file_path):
  part_n(process_game_1, file_path)


def part_2(_file_path):
  part_n(process_game_2, file_path)


if len(sys.argv) != 3:
  print(f'Usage: python3 {sys.argv[0]} <part> <file_path>')
  exit(1)

part = sys.argv[1]
file_path = sys.argv[2]

if part == '1':
  part_1(file_path)
elif part == '2':
  part_2(file_path)
else:
  print('Unknown part')
  exit(1)
