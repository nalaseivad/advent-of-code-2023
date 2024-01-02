import sys
import pprint
import re
from collections import deque
from enum import Enum
from math import lcm


debug_level = 0

def debug(level = 1):
  if level > debug_level: return False
  return True

def debug_print(s = '', level = 1, end = '\n'):
  if level > debug_level: return
  print(s, end=end)

def debug_pretty_print(x, level = 1):
  if level > debug_level: return
  pp = pprint.PrettyPrinter(indent = 4)
  pp.pprint(x)

def debug_print_grid(grid, level = 1):
  if level > debug_level: return
  for row in grid:
    print(''.join(row))
  print()


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
#   partition([1, 2, 3, 4, 5], 2, 1) -> [[1, 2], [2, 3], [3, 4], [4, 5], [5]]
#
def partition(iterable, bucket_size, offset):
  return partition_impl(iterable, bucket_size, offset)


class Pulse(Enum):
  Low = 0
  High = 1


class ModuleType(Enum):
  Broadcast = 0
  FlipFlop = 1
  Conjunction = 2
  End = 3


def make_module_type_and_state(type_character):
  if type_character == '%':
    return ModuleType.FlipFlop, Pulse.Low
  if type_character == '&':
    return ModuleType.Conjunction, {}
  if type_character == '':
    return ModuleType.Broadcast, None
  raise 'Bad module type character'


class Module():
  def __init__(self, row):
    if row == None:
      self.name = ''
      self.output_module_names = []
      self.type = ModuleType.End
      self.state = None
      self.input_module_names = []
      return
    
    pattern = r'^([%&]*)(\w+) -> (.*)$'
    match = re.match(pattern, row)
    if not match: raise 'Bad module pattern'
    type, name, output_module_names_string = match.groups()

    self.name = name
    self.output_module_names = re.split(r',\s*', output_module_names_string)
    self.type, self.state = make_module_type_and_state(type)
    self.input_module_names = []

  def __repr__(self):
    name = self.name
    type = self.type.name
    state = self.state
    outputs = self.output_module_names
    inputs = self.input_module_names
    s = f'{{ {name=}, {type=}, {state=}, {inputs=}, {outputs=} }}'
    return s


def init_modules(file_path):
  modules = {}
  with open(file_path, 'r') as lines:
    rows = (line.rstrip('\n') for line in lines)
    for row in rows:
      module = Module(row)
      modules[module.name] = module

    modules_to_add = []
    for k, v in modules.items():
      for module_name in v.output_module_names:
        if module_name not in modules:
          modules_to_add.append(module_name)
    for module_name in modules_to_add:
      module = Module(None)
      module.name = module_name
      modules[module_name] = module
    
    for k, v in modules.items():
      for module_name in v.output_module_names:
        target_module = modules[module_name]
        target_module.input_module_names.append(k)
        if target_module.type == ModuleType.Conjunction:
          target_module.state[k] = Pulse.Low
    return modules


def process_conjunction_module(module, input_module, input_pulse):
  result = []
  module.state[input_module.name] = input_pulse
  output_pulse = Pulse.Low if all(map(lambda v: v == Pulse.High, module.state.values())) else Pulse.High
  for name in module.output_module_names:
    result.append([name, output_pulse])
  return result


def flip(state):
  new_state = (state.value + 1) % 2
  if new_state == 0:
    return Pulse.Low, Pulse.Low
  else:
    return Pulse.High, Pulse.High


def process_flip_flop_module(module, _, input_pulse):
  result = []
  if input_pulse == Pulse.High:
    return result
  module.state, output_pulse = flip(module.state)
  for name in module.output_module_names:
    result.append([name, output_pulse])
  return result


def process_broadcast_module(module, _, input_pulse):
  result = []
  for name in module.output_module_names:
    result.append([name, input_pulse])
  return result


def process_end_module(module, _, input_pulse):
  return []


def process_pulse(module, input_module, input_pulse):
  handlers = {
    ModuleType.FlipFlop : process_flip_flop_module,
    ModuleType.Conjunction : process_conjunction_module,
    ModuleType.Broadcast : process_broadcast_module,
    ModuleType.End : process_end_module
  }
  handler = handlers[module.type]
  return handler(module, input_module, input_pulse)


def process_modules_1(modules):
  queue = deque()
  queue.append(['broadcaster', 'button', Pulse.Low])
  low_count = high_count = 0
  while queue:
    module_name, input_module_name, input_pulse = queue.popleft()
    if input_pulse == Pulse.Low:
      low_count += 1
    else:
      high_count += 1
    if module_name not in modules: continue
    module = modules[module_name]
    input_module = modules[input_module_name] if input_module_name != 'button' else None
    for output_module_name, output_pulse in process_pulse(module, input_module, input_pulse):
      queue.append([output_module_name, module_name, output_pulse])
  return low_count, high_count


#
# Simulate a lot of button presses and watch a given list of module names to see when they get a low input.  Save all
# the button press counts and then calc the (hopefully constant) cycle length for each module.  Then return each of
# those cycle lengths.
#
def process_modules_2(modules, module_names):
  queue = deque()
  result = {}
  button_press_counts = {}
  # Keep pressing the button ...
  n = 1
  while True:
    queue.append(['broadcaster', 'button', Pulse.Low])
    while queue:
      module_name, input_module_name, input_pulse = queue.popleft()
      if module_name in module_names and input_pulse == Pulse.Low:
        if module_name not in button_press_counts: button_press_counts[module_name] = []
        button_press_counts[module_name].append(n)
        # Are we done?  Wait until we have at least 5 button count samples for each module and have verified that the
        # cycle length for each module is constant.
        if len(button_press_counts.keys()) == len(module_names):                 # Got a sample for all modules
          if all(map(lambda x: len(button_press_counts[x]) >= 5, module_names)): # Got enough samples for all modules
            for k, v in button_press_counts.items():
              cycle_lengths = [x[1] - x[0] for x in partition(v, 2, 1) if len(x) == 2]
              if len(set(cycle_lengths)) > 1:
                raise(f'Non-constant cycle length for module {k}')
              result[k] = cycle_lengths[0]
            return result

      module = modules[module_name]
      input_module = modules[input_module_name] if input_module_name != 'button' else None
      for output_module_name, output_pulse in process_pulse(module, input_module, input_pulse):
        queue.append([output_module_name, module_name, output_pulse])
    n += 1


#
# Press the button 1000 times and measure how many low and high pulses we see.  This is just a simple simulation.
#
def part_1(file_path):
  modules = init_modules(file_path)
  total_low_count = total_high_count = 0
  for _ in range(1000):
    low_count, high_count = process_modules_1(modules)
    total_low_count += low_count
    total_high_count += high_count
  print(f'{total_low_count=}, {total_high_count=}, product={total_low_count * total_high_count}')


#
# We are supposed to find the minimum number of button presses required in order for the 'rx' module to receive a
# low pulse.  A simple simulation and wait for it to happen approach seems infeasible so we're going to have to be
# clever.
#
# From an analysis of the graph of modules we can see that the 'rx' module is the single output of the 'mf'
# conjunction module, which itself has four input modules: 'bh', 'jf', 'sh' and 'mz', all also conjunction modules.
# Then each of these conjunction modules itself has a single input, another conjuntion module.
#
# A conjunction module with one input is essentially a NOT gate and a conjunction module with multiple inputs is
# essentially a NAND gate.  For 'rx' to receive a low pulse, 'mf' needs to have all its inputs be high at the same time.
# Each of the inputs to 'mf' will be high when each of those modules receives a low pulse.
#
# rx <-low- &mf <-high- &bh <-low- &gh
#               <-high- &jf <-low- &xc
#               <-high- &sh <-low- &cn
#               <-high- &mz <-low- &hz
#
# I am going to assume that each of the inputs to 'mf' ('bh', 'jf', 'sh' and 'mz') will receive a low pulse on a cycle
# of fixed length.  If we can calculate those cycle lengths (number of button presses to get to a low input pulse) then
# we can calculate the length of the cycle on which 'all' of the inputs will receive a low pulse at the same time as the
# lowest common multiple (LCM) of the four input cycle lengths.
#
# BTW, the above assumption of constant cycle length was true.  How convenient.
#
def part_2(file_path):
  modules = init_modules(file_path)
  module_names = ['bh', 'jf', 'sh', 'mz']
  result = process_modules_2(modules, module_names)
  print(result)
  print(lcm(*(result.values())))


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
