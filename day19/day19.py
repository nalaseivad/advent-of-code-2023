import sys
import pprint
import re
from math import prod


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


def read_workflows(rows):
  workflows_by_name = {}
  for row in rows:
    if re.match(r'^\s*$', row): break

    rule_match = re.match(r'^(\w+){([^{}]+)}$', row)
    if not rule_match: continue

    workflow_name, rules_string = rule_match.groups()
    workflow = []
    workflows_by_name[workflow_name] = workflow
    rule_strings = rules_string.split(',')
    for rule_string in rule_strings:
      match_no_filter = re.match(r'^(\w+)$', rule_string)
      rule = { 'workflow_name' : workflow_name }
      if match_no_filter:
        action = match_no_filter.groups()[0]
        rule['action'] = action
      else:
        match_filter = re.match(r'^(\w+)(<|>)(\d+):(\w+)$', rule_string)
        if match_filter:
          property_name, op, value, action = match_filter.groups()
          rule['property_name'] = property_name
          rule['op'] = op
          rule['value'] = int(value)
          rule['action'] = action
      workflow.append(rule)

  return workflows_by_name


def parse_part_string(part_string):
  part = {}
  match = re.match(r'{([^{}]+)}', part_string)
  if not match: return None
  kv_list = match.groups()[0]
  for kv in kv_list.split(','):
    k, v = kv.split('=')
    part[k] = int(v)
  return part


def apply_workflow(part, workflow):
  for rule in workflow:
    debug_print(f'  {rule}')
    if 'property_name' not in rule:
      return rule['action']
    property_name = rule['property_name']
    op = rule['op']
    value = rule['value']
    action = rule['action']
    if op == '<':
      if part[property_name] < value:
        debug_print(f'  return {action}')
        return action
    else: # op == '>'
      if part[property_name] > value:
        debug_print(f'  return {action}')
        return action


def apply_workflows(part, workflow, workflows_by_name):
  while True:
    result = apply_workflow(part, workflow)
    if result in ('A', 'R'):
      return result
    workflow = workflows_by_name[result]


def part_1(file_path):
  with open(file_path, 'r') as lines:
    rows = (line.rstrip('\n') for line in lines)
    workflows_by_name = read_workflows(rows)
    debug_pretty_print(workflows_by_name)

    answer = 0
    for part_string in rows:
      part = parse_part_string(part_string)
      debug_print(f'{part} ...')
      result = apply_workflows(part, workflows_by_name['in'], workflows_by_name)
      debug_print(f'... {result=}')
      if result == 'A':
        answer += sum(part.values())
    print(answer)


def possibly_append_filter(filters, rule):
  if 'property_name' in rule:
    return [*filters, make_filter(rule)]
  return filters


def make_negated_filter(rule):
  op = rule['op']
  new_op = '<=' if op == '>' else '>='
  return [ rule['property_name'], new_op, rule['value'] ]


def make_filter(rule):
  return [ rule['property_name'], rule['op'], rule['value'] ]


#
# Find all the paths (lists of filters on properties) that result in the part being accepted
#
def good_workflow_paths(workflow_name, workflows_by_name, filters_so_far, good_paths, level = 0):
  pad = '  ' * level
  debug_print(f'{pad}good_workflow_paths, {workflow_name=}, {filters_so_far=}')

  workflow = workflows_by_name[workflow_name]
  for rule in workflow:
    action = rule['action']
    debug_print(f'{pad}{rule=}')
    debug_print(f'{pad}{action=}')

    if action in ('A', 'R'):
      if action == 'A':
        good_paths.append(possibly_append_filter(filters_so_far, rule))
        debug_print(f'{pad}{good_paths=}')
      if 'property_name' in rule:
        filters_so_far.append(make_negated_filter(rule))
      continue

    new_filters_so_far = [*filters_so_far]
    if 'property_name' in rule:
      new_filters_so_far.append(make_filter(rule))

    good_workflow_paths(action, workflows_by_name, new_filters_so_far, good_paths, level + 1)

    if 'property_name' in rule:
      filters_so_far.append(make_negated_filter(rule))


def part_2(file_path):
  with open(file_path, 'r') as lines:
    rows = (line.rstrip('\n') for line in lines)
    workflows_by_name = read_workflows(rows)
    debug_pretty_print(workflows_by_name)
    debug_print()

    good_paths = []
    good_workflow_paths('in', workflows_by_name, [], good_paths)
    debug_pretty_print(good_paths)
    debug_print()

    #
    # For each path (list of filters) that leads to a part being accepted, trim down the range of possible values for
    # each property.  Then count all the possible combinations of property values (product of property ranges).
    #
    # Then add these up over all the paths.
    #
    num_combinations = 0
    for good_path in good_paths:
      property_ranges = { 'x' : [1, 4000], 'm' : [1, 4000], 'a' : [1, 4000], 's' : [1, 4000] }
      for filter in good_path:
        property_name, op, value = filter
        property_range = property_ranges[property_name]
        debug_print(f'{property_name} {op} {value}')
        if op == '<':
          property_range[1] = value - 1
        elif op == '>':
          property_range[0] = value + 1
        elif op == '<=':
          property_range[1] = value
        else:  # '>='
          property_range[0] = value
      debug_pretty_print(property_ranges)

      product = prod(map(lambda v: v[1] - v[0] + 1, property_ranges.values()))
      debug_print(f'{product=}')
      num_combinations += product

    print(num_combinations)


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
