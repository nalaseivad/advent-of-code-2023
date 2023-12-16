import sys
import re
import pprint
from collections import deque
from functools import reduce


debug_level = 1

def debug_print(s, level = 1):
  if level > debug_level: return
  print(s)

#
# Print a more readable version of our maps
#
def debug_pretty_print(x, level = 1):
  if level > debug_level: return
  pp = pprint.PrettyPrinter(indent = 4)
  pp.pprint(x)


def partition_impl(iterable, bucket_size, offset):
  buckets = deque()
  n = 0
  for item in iterable:
    if n % offset == 0:
      buckets.append([])
    for bucket in buckets:
      bucket.append(item)
    if len(buckets[0]) == bucket_size:
      yield buckets.popleft()
    n += 1
  while len(buckets) > 0:
    yield buckets.popleft()


#
# Partition a list into an iterable of sublists of a certain size with a specific offset.  The last list may be
# incomplete.
# Examples
#   partition([1, 2, 3, 4, 5, 6, 7], 2)    -> [[1, 2], [3, 4], [5, 6], [7]]
#   partition([1, 2, 3, 4, 5, 6, 7], 3, 2) -> [[1, 2, 3], [3, 4, 5], [5, 6, 7], [7]]
#
def partition(iterable, bucket_size, offset = None):
  if offset == None: offset = bucket_size
  return partition_impl(iterable, bucket_size, offset)


def hash_char(accumulator, c):
  return ((accumulator + ord(c)) * 17) % 256


def hash(s):
  return reduce(hash_char, s, 0)


def part_1(file_path):
  with open(file_path, 'r') as lines:
    tokens = ''.join((line.rstrip('\n') for line in lines)).split(',')
    print(sum(map(hash, tokens)))


def op_dash(boxes, label, _):
  label_hash = hash(label)
  if label_hash not in boxes:
    return
  list = boxes[label_hash]
  for n, elem in enumerate(list):
    if elem[0] == label:
      boxes[label_hash] = list[:n] + list[n+1:]


def op_equals(boxes, label, focal_length):
  label_hash = hash(label)
  if label_hash not in boxes: boxes[label_hash] = []
  list = boxes[label_hash]
  for elem in list:
    if elem[0] == label:
      elem[1] = int(focal_length)
      return
  boxes[label_hash].append([label, int(focal_length)])


def part_2(file_path):
  with open(file_path, 'r') as lines:
    tokens = ''.join((line.rstrip('\n') for line in lines)).split(',')
    boxes = {}
    for token in tokens:
      label, op, focal_length = re.match(r'^([a-z]*)(=|-)(\d*)', token).groups()
      label_hash = hash(label)
      if label_hash not in boxes: boxes[label_hash] = []
      { '-' : op_dash, '=' : op_equals }[op](boxes, label, focal_length)
    answer = 0
    for k, list in boxes.items():
      for n, elem in enumerate(list):
        answer += (int(k) + 1) * (n + 1) * elem[1]
    print(answer)


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
