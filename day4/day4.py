import sys
import re


debug = 0

def debug_print(s):
  if debug:
    print(s)


def parse_card_data(line):
  bits = re.split(r'\s*:\s*', line)
  card_number = re.split(r'\s+', bits[0])[1]
  winning_numbers_string, numbers_string = re.split(r'\s*\|\s*', bits[1])
  winning_numbers = set()
  for n in re.split(r'\s+', winning_numbers_string):
    winning_numbers.add(int(n))
  numbers = list(map(lambda n: int(n), re.split(r'\s+', numbers_string)))
  debug_print(winning_numbers)
  debug_print(numbers)
  return int(card_number), winning_numbers, numbers


def part_1(file_path):  
  with open(file_path, 'r') as lines:
    points = 0
    data = (parse_card_data(line.rstrip('\n')) for line in lines)
    for card_number, winning_numbers, numbers in data:
      my_winning_numbers = []
      card_points = 0
      for number in numbers:
        if number in winning_numbers:
          my_winning_numbers.append(number)
      count = len(my_winning_numbers)
      if count > 0:
        card_points = pow(2, count - 1)
      debug_print(f'For card {card_number}: My winning numbers = {my_winning_numbers}, points = {card_points}')
      points += card_points
    print(points)


def process_card(card_number, winning_numbers, numbers):
  my_winning_numbers = []
  for number in numbers:
    if number in winning_numbers:
      my_winning_numbers.append(number)
  return len(my_winning_numbers)


def part_2(file_path):
  with open(file_path, 'r') as lines:
    winning_card_counts = {}
    data = (parse_card_data(line.rstrip('\n')) for line in lines)
    for card_number, winning_numbers, numbers in data:
      count = winning_card_counts[card_number] = winning_card_counts.get(card_number, 0) + 1
      for n in range(count):
        winning_numbers_count = process_card(card_number, winning_numbers, numbers)
        if winning_numbers_count > 0:
          for n in range(card_number + 1, card_number + winning_numbers_count + 1):
            winning_card_counts[n] = winning_card_counts.get(n, 0) + 1
      debug_print(f'Card {card_number}: Count of this card = {winning_card_counts[card_number]}')
    print(sum(winning_card_counts.values()))


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
