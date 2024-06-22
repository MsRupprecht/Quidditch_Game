import random
import csv

# csv admin
# open the file
data = open("input.csv")
# instantiate the reader
csv_data = csv.reader(data, delimiter=' ')
# reformat into a python object
data_lines = list(csv_data)

# output file (for posting)
# open the file ready for appending
data_output = open("output.csv", mode = "a", newline = "")
# instantiate the writer
csv_writer = csv.writer(data_output, delimiter = ",")

# create results file (for scoring)
# open the file ready for appending
data_results = open("results.csv", mode = "a", newline = "")
# instantiate the writer
csv_writer_results = csv.writer(data_results, delimiter = ",")
results_headings = ["name", "points", "house"]
csv_writer_results.writerow(results_headings)



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

Ravenclaw = 0
Slytherin = 0
Hufflepuff = 0
Gryffindor = 0


# Score each line
for line in data_lines:
  
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
  house = ""
  comment = ["", "", "", "", "", "", ""]
  comment_str = ""
  results = [name, e1, r1, e2, r2, e3, r3, e4, r4, e5, r5, comment_str]

  # Initialise the entry list and score
  results[0] = line[0] #input name into results
  entry = line[1:6] #slice guesses out of line
  house = line[6][1:] #slice house out of line
  
  # Populate the guesses into the results list
  for i in range (5):
    results[2*i+1] = entry[i]

  # Starting score 10 for playing
  score = score + 10

  # If Thestral Poo, game will only be scored up to this entry index
  game_over = ""
  for i in range(5):
    if entry[i] == T:
      game_over = i
  if game_over != "":
    entry = entry [0:i]
    results[2*i+2] = "-THESTRAL POO!"
    comment[i] = "Oh no - You flew into the invisible Thestral Poo!  Game over for you as you go back to the castle to wash up."

  # For each entry that matches Snitch, + 150
  for i in range(len(entry)):
    if entry[i] == GS:
      score = score + 150
      results[2*i+2] = "-GOLDEN SNITCH!"
      comment[i] = "Great catch!  You've got the Golden Snitch! "

  # For each entry that matches Owl, - 5
  owl_count = 0
  owl_hits = []
  for i in range(len(entry)):
    for owl in O:
      if entry[i] == owl:
        score = score - 5
        results[2*i+2] = "-OWL!"
        owl_count = owl_count + 1
        owl_hits.append(i)
  if owl_count == 1:
    comment[owl_hits[0]] = "Watch out for Errol!  Spit those feathers out and get back in the game!"
  elif owl_count == 2:
    comment[owl_hits[0]] = "Watch out for Errol! Spit those feathers out and get back in the game."
    comment[owl_hits[1]] = "Pigwidgeon just crashed into you!"
        
  # For each entry that matches Scoreboard, + 10
  for i in range(len(entry)):
    if entry[i] == S:
      score = score + 10
      results[2*i+2] = "-SCOREBOARD!"
      comment[i] = "Great work - way to bump up that score!"

  # For each entry that matches quaffle, +10
  for i in range(len(entry)):
    if entry[i] == Q:
      score = score + 10
      results[2*i+2] = "-QUAFFLE!"
      
  # For each entry that matches Goal Post, +5
  for i in range(len(entry)):
    for post in GP:
      if entry[i] == post:
        score = score + 5
        results[2*i+2] = "-GOAL POST!"

  # If quaffle comes before goal post, + 10
  # Initialise order_list
  order_list = ["0", "0", "0", "0", "0"]
  hit_Q = []
  hit_GP = []
  # Loop through the entry to find quaffle and goal posts
  for guess_i in range (len(entry)):
    if entry[guess_i] == Q:
      order_list[guess_i] = "Q"
      hit_Q.append(guess_i)
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
    comment[hit_Q[0]] = "You've got the Quaffle - now head to the goal!"
    comment[hit_GP[0]] = "You made it to the goal post and scored!!"
    if len(hit_GP)>1:
      comment[hit_GP[1]] = "You made it back to the goal post but no one passed you the Quaffle this time."
  else:
    if len(hit_Q) != 0:
      comment[hit_Q[0]] = "You've got the Quaffle! Now head to the goal!"
    if len(hit_GP) != 0:
      comment[hit_GP[0]] = "You made it to the goal post! Next time pick up the Quaffle first."


  # For each entry that matches beater bat, +5
  for i in range(len(entry)):
    for bat in BB:
      if entry[i] == bat:
        score = score + 5
        results[2*i+2] = "-BEATER'S BAT!"
  
  # For each entry that matches Bludger, - 5
  for i in range(len(entry)):
    for bludger in B:
      if entry[i] == bludger:
        score = score - 5
        results[2*i+2] = "-BLUDGER!"
        
  
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
  # Look for "BS" and calculate bonus
  location = order.find("BS")
  if order == "BBSS":
    bonus = 2
  elif location > -1:
    bonus = 1
    leftover = order[location+2:]
    second_location = leftover.find("BS")
    if second_location > -1:
      bonus = 2
  else:
    bonus = 0
  score = score + 5*bonus
  # Insert comments for bats/bludgers
  bats_no_strikes = ["B"]
  save_one_strike = ["BS"]
  save_one_multiple_bats = ["BBBS", "BBSB", "BSBB", "BBBBS", "BBBSB", "BBSBB", "BSBBB"]
  save_two_strikes = ["BBSS", "BSBS", "BBBSS", "BBSBS", "BSBBS"]
  bats_after_one_strike = ["SB", "SBBB", "SBBBB"]
  bats_after_two_strikes = ["SSB", "SSBB", "SSBBB"]
  save_one_miss_one = ["BSS", "SBS", "BSSB", "SBSB", "SBBBS", "SBBSB", "SBSBB"]
  one_strike = ["S"]
  two_strikes = ["SS"]
  if order in bats_no_strikes:
    comment[hit_BB[-1]] = "You're ready for those stray Bludgers now!"
  elif order in save_one_strike:
    comment[hit_B[-1]] = "Good job defending against that bludger!"
  elif order in save_one_multiple_bats:
    comment[hit_B[-1]] = "Good thing you picked up so many bats - you were able to expertly defend against that rogue bludger"
  elif order in save_two_strikes:
    comment[hit_B[-1]] = "Good job defending against both of those bludgers."
  elif order in bats_after_one_strike:
    comment[hit_B[-1]] = "You picked up a bat, but unfortunately it was too late and you still got hit by a rogue bludger."
  elif order in bats_after_two_strikes:
    comment[hit_B[-1]] = "You picked up a bat, but unfortunately it was too late and you still got hit by those rogue bludgers."
  elif order in save_one_miss_one:
    comment[hit_B[-1]] = "You defended admirably against one bludger, but got hit by the other one."
  elif order in one_strike:
    comment[hit_B[-1]] = "Oooh - that hurt!  Need to keep an eye out for those rogue Bludgers!"
  elif order in two_strikes:
    comment[hit_B[-1]] = "Oooh - that double blow really hurt!  Need to keep an eye out for those rogue Bludgers!"



  # If score is negative, score becomes 0 and game over
  if score <= 0 and game_over == "":
    score = 0
    comment[-1] = "Bad luck in today's match - you've been knocked you straight off your broom. Head to Madam Pomfrey to get those bruises seen to."
  
  # Turn blanks into misses
  for i in range (len(entry)):
    if results[2*i+2] == None:
      results[2*i+2] = "-MISS"
  
  # Override score if Thestral Poo
  if game_over != "":
    score = 0

  # Create a single comment string
  comment_simplified = [ele for ele in comment if ele != ""]
  if score != 0:
    if len(comment_simplified) == 0:
      comment_simplified.append(str(score)+" points to "+house+". Thanks for playing!")
    else:
      comment_simplified.append(str(score)+" points to "+house+"!")
  comment_str = " ".join(comment_simplified)
  
  # Concatenate entries and results for better display
  new_line = [results[0]]
  for i in range(5):
    results[2*i+1] = " " + results[2*i+1] + results[2*i+2]
    new_line.append(results[2*i+1])
  new_line.append(" "+comment_str)

  # Update overall score for the game
  if house == "Ravenclaw":
    Ravenclaw = Ravenclaw + score
  elif house == "Hufflepuff":
    Hufflepuff = Hufflepuff + score
  elif house == "Gryffindor":
    Gryffindor = Gryffindor + score
  elif house =="Slytherin":
    Slytherin = Slytherin + score
  else:
    print("No house detected for",name)

  # Write the results to the csv files
  results_line = [results[0], score, house]
  csv_writer.writerow(new_line)
  csv_writer_results.writerow(results_line)

overall_score = ["Ravenclaw:"+str(Ravenclaw),"Hufflepuff:"+str(Hufflepuff),"Gryffindor:"+str(Gryffindor), "Slytherin:"+str(Slytherin)]
csv_writer.writerow(overall_score)

# save it all and shut it down
data_output.close()
data_results.close()