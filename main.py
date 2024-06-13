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

# Initialise score and results list
score = 0
name = ""
e1 = ""
r1 = None
e2 = ""
r2 = None
e3 = ""
r3 = None
e4 = ""
r4 = None
e5 = ""
r5 = None
comment = ["", "", "", "", "", ""]
comment_str = ""
results = [name, e1, r1, e2, r2, e3, r3, e4, r4, e5, r5, comment_str]

# Score each line
for line in data_lines:
  # Initialise the entry list and score
  entry = line[1:6]
  score = 0
  results[0] = line[0]

  # Populate the entries into the results list
  for i in range (5):
    results[2*i+1] = entry[i]

  # Starting score 10 for playing
  score = score + 10

  # If Thestral Poo - total score 0, game will only be scored up to this entry index
  game_over = ""
  for i in range(5):
    if entry[i] == T:
      game_over = i
      score = 0
  if game_over != "":
    entry = entry [0:i]
    results[2*i+2] = "- THESTRAL POO!"
    comment[i] = "THESTRAL COMMENT"

  # For each entry that matches beater bat, +5
  for i in range(len(entry)):
    for bat in BB:
      if entry[i] == bat:
        score = score + 5
        results[2*i+2] = "- BEATER'S BAT!"
  
  # For each entry that matches quaffle, +10
  for i in range(len(entry)):
    if entry[i] == Q:
      score = score + 10
      results[2*i+2] = "- QUAFFLE!"
      
  # For each entry that matches Goal Post, +5
  for i in range(len(entry)):
    for post in GP:
      if entry[i] == post:
        score = score + 5
        results[2*i+2] = "- GOAL POST!"
  
  # For each entry that matches Snitch, + 150
  for i in range(len(entry)):
    if entry[i] == GS:
      score = score + 150
      results[2*i+2] = "- GOLDEN SNITCH!"
      comment[i] = "Great catch!  You've got the Golden Snitch! "

  
  # For each entry that matches Bludger, - 5
  for i in range(len(entry)):
    for bludger in B:
      if entry[i] == bludger:
        score = score - 5
        results[2*i+2] = "- BLUDGER!"
        #comment[i] = "Oooh, that hurt!  Need to keep an eye out for those rogue Bludgers!"
  
  
  # If bat comes before bludger, +5 
  # Initialise order_list
  order_list = ["0", "0", "0", "0", "0"]
  hit_BB = []
  hit_B = []

  
  # Loop through the entry to find bats and strikes
  for guess_i in range(len(entry)):
    for bat_i in range(4):
      if entry[guess_i] == BB[bat_i]:
        order_list[guess_i] = "B"
        hit_BB.append(guess_i)
    for bludger_i in range(2):
      if entry[guess_i] == B[bludger_i]:
        order_list[guess_i] = "S"
        hit_B.append(guess_i)
  # Remove any place holders
  order_list = [ele for ele in order_list if ele != "0"]
  # Identify bats and strikes in one string
  order = "".join(order_list)
  # Look for "BS"
  location = order.find("BS")
  if order == "BBSS":
    bonus = 2
    comment[hit_BB[0]] = "You're ready for those stray Bludgers now!"
    comment[hit_BB[1]] = "Another beater bat ready to protect your team!"
    comment[hit_B[0]] = "Great defensive work!"
    comment[hit_B[1]] = "Those Bludgers can't even get close to you!"
  elif location > -1:
    bonus = 1
    leftover = order[location+2:]
    print("leftover :",leftover)
    second_location = leftover.find("BS")
    if second_location > -1:
      bonus = 2
      comment[hit_BB[0]] = "You're ready for those stray Bludgers now!"
      comment[hit_BB[1]] = "Another beater bat ready to protect your team!"
      comment[hit_B[0]] = "Great defensive work!"
      comment[hit_B[1]] = "Those Bludgers can't even get close to you!"
  elif location == -1:
    bonus = 0
  else:
    print("Something went wrong")
  score = score + 5*bonus
  
  # If quaffle comes before goal post, + 10
  # Initialise order_list
  order_list = ["0", "0", "0", "0", "0"]
  hit_Q = ""
  hit_GP = []
  # Loop through the entry to find quaffle and goal posts
  for guess_i in range (len(entry)):
    if entry[guess_i] == Q:
      order_list[guess_i] = "Q"
      hit_Q = guess_i
    for goalpost_i in range(6):
      if entry[guess_i] == GP[goalpost_i]:
        order_list[guess_i] = "G"
        hit_GP.append(guess_i)
  # Remove any place holders
  order_list = [ele for ele in order_list if ele != "0"]
  # Identify quaffle and goal posts in one string
  order = "".join(order_list)
  # Look for "QG"
  location = order.find("QG")
  if location > -1:
    score = score + 10
    comment[hit_Q] = "You've got the Quaffle, now head to the goal!"
    comment[hit_GP[0]] = "You made it to the goal post and scored!!"
  else:
    if len(hit_GP) != 0:
      comment[hit_GP[0]] = "You're at the goal, but you forgot to get the Quaffle first!"

  
  # For each entry that matches Owl, - 5
  for i in range(len(entry)):
    for owl in O:
      if entry[i] == owl:
        score = score - 5
        results[2*i+2] = "- OWL!"
        comment[i] = "Watch out for Errol!  Spit those feathers out and get back in the game!"
        
  # For each entry that matches Scoreboard, + 10
  for i in range(len(entry)):
    if entry[i] == S:
      score = score + 10
      results[2*i+2] = "- SCOREBOARD!"
      comment[i] = "Great work - way to bump up that score!"
  
  # If score is negative, score becomes 0 and game over
  if score < 0:
    score = 0
  
  # Turn blanks into misses
  for i in range (len(entry)):
    if results[2*i+2] == None:
      results[2*i+2] = "- MISS"
  
  # Create a single comment string
  for word in comment:
    comment_str = comment_str + word
  results[-1] = comment_str

  
  # Write the results to the csv file
  csv_writer.writerow(results)

# save it all and shut it down
data_output.close()