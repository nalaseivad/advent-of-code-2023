import sys
import re
import pprint
from functools import cmp_to_key


debug = 0

def debug_print(s):
  if debug:
    print(s)

#
# Print a more readable version of our maps
#
def debug_pretty_print(x):
  if debug:
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(x)


card_values_1 = {
  '2' : 2,
  '3' : 3,
  '4' : 4,
  '5' : 5,
  '6' : 6,
  '7' : 7,
  '8' : 8,
  '9' : 9,
  'T' : 10,
  'J' : 11,
  'Q' : 12,
  'K' : 13,
  'A' : 14
}

#
# Reinterpet the value of 'J' (jokers) as the lowest value
#
card_values_2 = {
  'J' : 1,
  '2' : 2,
  '3' : 3,
  '4' : 4,
  '5' : 5,
  '6' : 6,
  '7' : 7,
  '8' : 8,
  '9' : 9,
  'T' : 10,
  'Q' : 12,
  'K' : 13,
  'A' : 14
}


def calc_hand_type_1(card_counts):
  counts_desc = sorted(card_counts.values(), reverse = True)
  if counts_desc[0] == 5: return (7, 'Five of a kind')
  if counts_desc[0] == 4: return (6, 'Four of a kind')
  if counts_desc[0] == 3:
    if counts_desc[1] == 2: return (5, 'Full house')
    return (4, 'Three of a kind')
  if counts_desc[0] == 2:
    if counts_desc[1] == 2: return (3, 'Two pair')
    return (2, 'One pair')
  return (1, 'High card')


def calc_hand_type_2(card_counts):
  card_counts_ex = {k : v for k, v in card_counts.items() if k != 'J'}   # Remove the jokers
  if len(card_counts_ex) == 0: return calc_hand_type_1(card_counts)   # 5 Jokers

  cards_by_count_desc = [k for k, _ in sorted(card_counts_ex.items(), key = lambda kv: kv[1], reverse = True)]
  max_count_card = cards_by_count_desc[0]

  num_jokers = card_counts.get('J', 0)
  card_counts_ex[max_count_card] += num_jokers   # Add the jokers back as additional cards of the max count type
  return calc_hand_type_1(card_counts_ex)
  

def parse_line(line, calc_hand_type):
  cards_string, bid = re.split(r'\s+', line)
  bid = int(bid)
  cards = list(cards_string)
  card_counts = {}
  for card in cards:
    n = card_counts.get(card, 0)
    n += 1
    card_counts[card] = n
  type = calc_hand_type(card_counts)
  return { 'cards' : cards, 'card_counts' : card_counts, 'type' : type, 'bid' : bid }


def compare_hands(hand1, hand2, card_values):
  cards1 = hand1['cards']
  cards2 = hand2['cards']

  type1 = hand1['type'][0]
  type2 = hand2['type'][0]
  if type1 < type2: return -1
  if type1 > type2: return 1
  
  for card1, card2 in zip(cards1, cards2):
    value1 = card_values[card1]
    value2 = card_values[card2]
    if value1 < value2: return -1
    if value1 > value2: return 1
  return 0


def calc_winnings(tuple):
  rank, hand = tuple
  return rank * hand['bid']


def part_n(file_path, calc_hand_type, card_values):
  with open(file_path, 'r') as lines:
    lines = (line.rstrip('\n') for line in lines)
    hands = (parse_line(line, calc_hand_type) for line in lines)
    compare_hands_fn = lambda hand1, hand2 : compare_hands(hand1, hand2, card_values)
    hands_ranked = enumerate(sorted(hands, key = cmp_to_key(compare_hands_fn)), 1)
    products = map(calc_winnings, hands_ranked)
    print(sum(products))


def part_1(file_path):
  part_n(file_path, calc_hand_type_1, card_values_1)


def part_2(file_path):
  part_n(file_path, calc_hand_type_2, card_values_2)


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
