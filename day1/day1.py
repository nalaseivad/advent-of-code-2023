import sys
import re

digit_words = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')
rev_digit_words = list(map(lambda word: word[::-1], digit_words))
pattern_start = r'(?:(\d|'
pattern_end = r'))'
pattern = pattern_start + '|'.join(digit_words) + pattern_end
rev_pattern = pattern_start + '|'.join(rev_digit_words) + pattern_end

lookup_table = {}

def init():
  #print(f"digit_words: {', '.join(digit_words)}")
  #print(f"rev_digit_words: {', '.join(rev_digit_words)}")
  #print(f'pattern: {pattern}')
  #print(f'rev_pattern: {rev_pattern}')
  for enumerable in (enumerate(range(10)), enumerate(digit_words), enumerate(rev_digit_words)):
    for index, word in enumerable:
      lookup_table[str(word)] = index
  #print(lookup_table)

def is_digit(c):
  return c.isdigit()

def process_line_1(line):
  first_digit = next(filter(is_digit, line))
  last_digit = next(filter(is_digit, line[::-1]))
  return int(first_digit + last_digit)

def find_digit(line, pattern):
  #print(line)
  matches = list(re.finditer(pattern, line))
  #list(map(print, rev_matches))
  return lookup_table[matches[0].group()]

def process_line_2(line):
  first_digit = find_digit(line, pattern)
  last_digit = find_digit(line[::-1], rev_pattern)
  #print(f'{index} Found: {first_digit}{last_digit}')
  return first_digit * 10 + last_digit

def partN(process_line_fn):
  with open(file_path, 'r') as file:
    result = sum(map(process_line_fn, file))
  print(result)

def part1():
  partN(process_line_1)

def part2():
  partN(process_line_2)


if len(sys.argv) != 3:
  print(f'Usage: python3 {sys.argv[0]} <part> <file_path>')
  exit(1)

part = sys.argv[1]
file_path = sys.argv[2]

init()

if part == '1':
  part1()
elif part == '2':
  part2()
else:
  print('Unknown part')
  exit(1)
