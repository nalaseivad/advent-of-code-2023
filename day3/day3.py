import sys
import re
from itertools import tee, islice


debug = 0

def debug_print(s):
  if debug:
    print(s)


def generate_lines_window(lines):
  iter_current, iter_lead, iter_lag = tee(enumerate(lines), 3)

  while True:
    try:
      blank_line = ''
      current_line_index, current_line = next(iter_current)
      current_line = current_line.rstrip('\n')
      if len(blank_line) == 0:
        blank_line = '.' * len(current_line)

      if current_line_index == 0:
        lag_line = blank_line
        _ = next(iter_lead)
      else:
        _, lag_line = next(iter_lag)
        lag_line = lag_line.rstrip('\n')

      _, lead_line = next(iter_lead)
      lead_line = lead_line.rstrip('\n')

      yield lag_line, current_line, lead_line

    except StopIteration:
      yield lag_line, current_line, blank_line
      return


def check_line_1(line, start_index, end_index):
  chars = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.')
  for index in range(max(0, start_index - 1), min(end_index + 1, len(line) - 1)):
    char = line[index]
    if(line[index] not in chars):
      return True
  return False


def get_adjacent_numbers(line, start_index, end_index):
  numbers = []
  pattern = r'\d+'
  for match in re.finditer(pattern, line):
    number = int(match.group())
    number_start_index = match.start()
    number_end_index = match.end()

    #    *
    #      xx  no
    #    *
    #     xx   yes
    #    *
    #    xx    yes
    #    *
    #   xx     yes
    #    *
    #  xx      yes
    #    *
    # xx       no

    if number_start_index > end_index or number_end_index < start_index:
      continue
    numbers.append(number)

  return numbers


def is_part_number(lag_line, current_line, lead_line, start_index, end_index):
  if check_line_1(lag_line, start_index, end_index):
    return True
  if check_line_1(current_line, start_index, end_index):
    return True
  if check_line_1(lead_line, start_index, end_index):
    return True
  return False


def get_gear_info(lag_line, current_line, lead_line, start_index, end_index):
  numbers = []

  lag_line_numbers = get_adjacent_numbers(lag_line, start_index, end_index)
  for number in lag_line_numbers:
    numbers.append(number)

  current_line_numbers = get_adjacent_numbers(current_line, start_index, end_index)
  for number in current_line_numbers:
    numbers.append(number)
  
  lead_line_numbers = get_adjacent_numbers(lead_line, start_index, end_index)
  for number in lead_line_numbers:
    numbers.append(number)

  if len(numbers) == 2:
    return (True, numbers[0], numbers[1])
  
  return (False, 0, 0)


def part_1(file_path):
  part_numbers = []
  with open(file_path, 'r') as file:
    for lag_line, current_line, lead_line in generate_lines_window(file):
      debug_print('')
      debug_print(lag_line)
      debug_print(current_line)
      debug_print(lead_line)
      pattern = r'\d+'
      for match in re.finditer(pattern, current_line):
        number = match.group()
        start_index = match.start()
        end_index = match.end()
        print(f'{number} {start_index} {end_index}')
        if is_part_number(lag_line, current_line, lead_line, start_index, end_index):
          debug_print('Is part')
          part_numbers.append(int(number))
  result = sum(part_numbers)
  debug_print('')
  print(result)


def part_2(_file_path):
  gears = []
  with open(file_path, 'r') as file:
    for lag_line, current_line, lead_line in generate_lines_window(file):
      debug_print('')
      debug_print(lag_line)
      debug_print(current_line)
      debug_print(lead_line)
      pattern = r'\*'
      for match in re.finditer(pattern, current_line):
        start_index = match.start()
        end_index = match.end()
        debug_print(f'* {start_index} {end_index}')
        gear_info = get_gear_info(lag_line, current_line, lead_line, start_index, end_index)
        if gear_info[0]:
          debug_print('Is gear')
          gears.append((gear_info[1], gear_info[2]))
  debug_print(gears)
  result = sum(map(lambda x: x[0] * x[1], gears))
  print(result)


if len(sys.argv) != 3:
  print("Usage: python3 day3.py <part> <file_path>")
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
