import sys
import pprint


cache = {}


debug_level = 0

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


def replace_in_pattern(pattern, values):
  ret = ''
  n = 0
  for c in pattern:
    ret += values[n] if c == '?' else c
  return ret


def possibilities(num_spots, possible_values):
  if num_spots == 1:
    return possible_values
  ret = []
  for x in possible_values:
    for y in possibilities(num_spots -1, possible_values):
      ret.append(x + y)
  return ret


def filter_record(record, pattern):
  for pair in zip(record, pattern):
    if pair[1] == '?':
      continue
    if pair[0] != pair[1]:
      return False
  return True


def possible_records(space_length, block_lengths):
  if len(block_lengths) == 0:
    yield '.' * space_length
  else:
    block_length = block_lengths[0]
    for n in range(space_length - block_length + 1):
      for line in possible_records(space_length - n - block_length - 1, block_lengths[1:]):
        yield '.' * n + '#' * block_length + '.' + line


#
# Brute force ...
#
def part_1(file_path):
  with open(file_path, 'r') as lines:
    lines = (line.rstrip('\n') for line in lines)
    counts = []
    for line in lines:
      pattern, block_lengths_string = line.split(' ')
      block_lengths = list(map(int, block_lengths_string.split(',')))
      count = 0
      for record in possible_records(len(pattern), block_lengths):
        if(filter_record(record, pattern)):
          count += 1
      counts.append(count)
    print(sum(counts))


#
# i   - index of current char in pattern
# bi  - index of current block_length in block_lengths
# cbl - current block length
# chc - cache hit count
# cc  - call count
#
def process_line(pattern, block_lengths, i, bi, cbl, level = 0, chc = 0, cc = 0, use_cache = False):
  cc += 1
  pad = ' ' * level
  pattern_char = pattern[i] if i < len(pattern) else ''
  debug_print(f"{pad}PL {level}: {pattern}, '{pattern_char}', {block_lengths}, {i}, {bi}, {cbl}", 2)
  key = (i, bi, cbl)
  if key in cache:
    chc += 1
    debug_print(f'{pad}PL {level}: return from cache ({cache[key]}, {chc})', 2)
    return (cache[key], chc, cc)
  
  if i == len(pattern):
    debug_print(f'{pad}PL {level}: past end of pattern', 2)
    if bi == len(block_lengths) and cbl == 0:
      debug_print(f'{pad}PL {level}: MATCH return (1, {chc})', 2)
      return (1, chc, cc)
    elif bi == len(block_lengths) - 1 and block_lengths[bi] == cbl:
      debug_print(f'{pad}PL {level}: MATCH - return (1, {chc})', 2)
      return (1, chc, cc)
    else:
      debug_print(f'{pad}PL {level}: NO MATCH return (0, {chc})', 2)
      return (0, chc, cc)
    
  count = 0
  for c in ['.', '#']:
    debug_print(f'{pad}PL {level}: c = {c}', 2)
    if pattern[i] == c or pattern[i] == '?':
      if c == '.' and cbl == 0:
        debug_print(f"{pad}PL {level}: '.', not in a block -> call PL for next pattern char", 2)
        (subcount, chc, cc) = process_line(pattern, block_lengths, i + 1, bi, 0, level + 1, chc, cc, use_cache)
        count += subcount
      elif c == '.' and cbl > 0 and bi < len(block_lengths) and block_lengths[bi] == cbl:
        debug_print(f"{pad}PL {level}: '.', end of block, more blocks -> call PL for next pattern char, next block", 2)
        (subcount, chc, cc) = process_line(pattern, block_lengths, i + 1, bi + 1, 0, level + 1, chc, cc, use_cache)
        count += subcount
      elif c == '#':
        debug_print(f"{pad}PL {level}: '#', in a block -> call PL for next pattern char in this block, cbl + 1", 2)
        (subcount, chc, cc) = process_line(pattern, block_lengths, i + 1, bi, cbl + 1, level + 1, chc, cc, use_cache)
        count += subcount

  debug_print(f'{pad}PL {level}: return ({count}, {chc}, {cc})', 2)
  if(use_cache): cache[key] = count
  return (count, chc, cc)
  

#
# I'm going to need a different strategy for part 2.  There are just too many possible records to generate and filter.
#
# We need to cache subtree searches so that we don't redo the work.  I think this is what is known as Dynamic
# Programming.  The caching logic is in the process_line function above.  Here are some stats from procesing
# test-input.txt with and wihtout caching ...
#
# $ python3 day12.py 2 test-input.txt 1    // with caching
# total_cache_hit_count = 109, total_call_count = 5484
# 525152
#
# $ python3 day12.py 2 test-input.txt 0    // without caching
# total_cache_hit_count = 0, total_call_count = 8841827
# 525152
#
# Total calls to process_line went from 8,841,827 to just 5,484
#
def part_2(file_path, use_cache):
  with open(file_path, 'r') as lines:
    lines = (line.rstrip('\n') for line in lines)
    counts = []
    total_cache_hit_count = 0
    total_call_count = 0
    for line in lines:
      pattern, block_lengths_string = line.split(' ')
      pattern = '?'.join([pattern] * 5)
      block_lengths_string = ','.join([block_lengths_string] * 5)
      block_lengths = [int(x) for x in block_lengths_string.split(',')]
      cache.clear()
      cache_hit_count = 0
      (count, cache_hit_count, call_count) = process_line(pattern, block_lengths, 0, 0, 0, 0, 0, 0, use_cache)
      debug_print(f'{pattern}, {block_lengths}, {count}, cache_hit_count = {cache_hit_count}')
      counts.append(count)
      total_cache_hit_count += cache_hit_count
      total_call_count += call_count
      debug_pretty_print(cache, 2)
    print(f'total_cache_hit_count = {total_cache_hit_count}, total_call_count = {total_call_count}')
    print(sum(counts))


if len(sys.argv) != 4:
  print(f'Usage: python3 {sys.argv[0]} <part> <file_path> <use_cache>')
  exit(1)

part = sys.argv[1]
file_path = sys.argv[2]
use_cache = int(sys.argv[3])
use_cache = True if use_cache == 1 else False

if part == '1':
  part_1(file_path)
elif part == '2':
  part_2(file_path, use_cache)
else:
  print('Unknown part')
  exit(1)
