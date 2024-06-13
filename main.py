import random
import csv

# csv admin
# open the file
data = open("input.csv")
# instantiate the reader
csv_data = csv.reader(data, delimiter=' ')
# reformat into a python object
data_lines = list(csv_data)
# open the file ready for appending
data_output = open("output.csv", mode = "a", newline = "")
# instantiate the writer
csv_writer = csv.writer(data_output, delimiter = " ")


def create_board():
  # Set up grid
  first = "FIREBOLT"
  second =["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
  
  # Generate grid positions
  positions = []
  for i in range(18):
    new_column = first[random.randint(0,7)]
    new_row = second[random.randint(0,9)]
    new = new_column+new_row
    positions.append(new)
    
  # Check for repeats
  ready = False
  while ready == False:
    checked = []
    for item in positions:
      if item not in checked:
        checked.append(item)
    if len(checked) == 18:
      ready = True
    else:
      positions = checked
      more = 18 - len(checked)
      for i in range(more):
        new_column = first[random.randint(0,7)]
        new_row = second[random.randint(0,9)]
        new = new_column+new_row
        positions.append(new)
  return positions

def categorise_board(positions):
  TP = positions[0]
  Q = positions[1]
  GP = [positions[2], positions[3], positions[4], positions[5], positions[6], positions[7]]
  BB = [positions[8], positions[9], positions[10], positions[11]]
  B = [positions[12], positions[13]]
  S = positions[14]
  O = [positions[15], positions[16]]
  GS = positions[17]
  return[TP, Q, GP, BB, B, S, O, GS]

def display_board(positions):
  print("Thestral Poo:", positions[0])
  print("Quaffle:", positions[1])
  print("Goal Posts:", positions[2]+",", positions[3]+",", positions[4]+",", positions[5]+",", positions[6]+",", positions[7])
  print("Beaters bats:", positions[8]+",", positions[9]+",", positions[10]+",", positions[11])
  print("Bludgers:", positions[12]+",", positions[13])
  print("Scoreboard:", positions[14])
  print("Owls:", positions[15]+",", positions[16])
  print("Golden Snitch:", positions[17])

# Initialise the game
positions = create_board()
positions_lists = categorise_board(positions)
display_board(positions)

T = positions_lists[0]
Q = positions_lists[1]
GP = positions_lists[2]
BB = positions_lists[3]
B = positions_lists[4]
S = positions_lists[5]
O = positions_lists[6]
GS = positions_lists[7]


# Score each result
score = 0

# Score each line
for line in data_lines:
  entry = line[1:6]
  score = 0

  # Starting score 10 for playing
  score = score + 10
  
  # For each entry that matches beater bat, +5
  for guess in entry:
    for bat in BB:
      if guess == bat:
        score = score + 5
  
  # For each entry that matches quaffle, +10
  for guess in entry:
    if guess == Q:
      score = score + 10
      
  # For each entry that matches Goal Post, +5
  for guess in entry:
    for post in GP:
      if guess == post:
        score = score + 5
  
  # For each entry that matches Snitch, + 150
  for guess in entry:
    if guess == GS:
      score = score + 150
  
  # For each entry that matches Bludger, - 5
  for guess in entry:
    for bludger in B:
      if guess == bludger:
        score = score - 5
  
  
  # If bat comes before bludger, +5 
  # Initialise order_list
  order_list = ["0", "0", "0", "0", "0"]
  # Loop through the entry to find bats and strikes
  for guess_i in range(5):
    for bat_i in range(4):
      if entry[guess_i] == BB[bat_i]:
        order_list[guess_i] = "B"
    for bludger_i in range(2):
      if entry[guess_i] == B[bludger_i]:
        order_list[guess_i] = "S"
  # Remove any place holders
  order_list = [ele for ele in order_list if ele != "0"]
  # Identify bats and strikes in one string
  order = "".join(order_list)
  # Look for "BS"
  location = order.find("BS")
  if order == "BBSS":
    bonus = 2
  elif location > -1:
    bonus = 1
    leftover = order[location+2:]
    print("leftover :",leftover)
    second_location = leftover.find("BS")
    if second_location > -1:
      bonus = 2
  elif location == -1:
    bonus = 0
  else:
    print("Something went wrong")
  score = score + 5*bonus
  
  # If quaffle comes before goal post, + 10
  # Initialise order_list
  order_list = ["0", "0", "0", "0", "0"]
  # Loop through the entry to find quaffle and goal posts
  for guess_i in range (5):
    if entry[guess_i] == Q:
      order_list[guess_i] = "Q"
    for goalpost_i in range(6):
      if entry[guess_i] == GP[goalpost_i]:
        order_list[guess_i] = "G"
  # Remove any place holders
  order_list = [ele for ele in order_list if ele != "0"]
  # Identify quaffle and goal posts in one string
  order = "".join(order_list)
  # Look for "QG"
  location = order.find("QG")
  if location > -1:
    score = score + 10
  
  # For each entry that matches Owl, - 5
  for guess in entry:
    for owl in O:
      if guess == owl:
        score = score - 5
        
  # For each entry that matches Scoreboard, + 10
  for guess in entry:
    if guess == S:
      score = score + 10
  
  # If score is negative, score becomes 0 and game over
  if score < 0:
    score = 0
  
  # If Thestral Poo - total score 0 and game over
  for guess in entry:
    if guess == T:
      score = 0
  
  #entry.append(score)
  new_line = [line[0]]
  for i in range(5):
    new_line.append(entry[i])
  print(new_line)
  new_line.append(score)
  print(new_line)
  csv_writer.writerow(new_line)

# save it all and shut it down
data_output.close()