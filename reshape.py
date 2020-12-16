"""This is just to reshape the movie dialogue data into a .txt format"""

import json


# characters = {}
# with open('movie-chat/movie_characters_metadata.txt', 'r', encoding='iso-8859-1') as chars:
#   for char in chars:
#       characters[char.split(' +++$+++ ')[0]] = char.split(' +++$+++ ')[1] + ": "

lines = {}
with open('movie-chat/movie_lines.txt', 'r', encoding='iso-8859-1') as f:
    for line in f.readlines():
        lines[line.split(' +++$+++ ')[0]] = line.split(' +++$+++ ')[-1]
#         #lines[line.split(' +++$+++ ')[0]] = characters[line.split(' +++$+++ ')[1]] + line.split(' +++$+++ ')[-1]
       
dialogues = ""
convos = []
with open('movie-chat/movie_conversations.txt') as conversations:
    for convo in conversations:
        convos.append(convo)

for i in range(0, 200):
    ls = convos[i].split(' +++$+++ ')[3].replace('\n', "").replace('[', "").replace("]", "").replace("'", "").split(", ")
    for l in ls:
        dialogues += lines[l]

dialogues2 = ""
for i in range(201, 300):
    ls = convos[i].split(' +++$+++ ')[3].replace('\n', "").replace('[', "").replace("]", "").replace("'", "").split(", ")
    for l in ls:
        dialogues2 += lines[l]

tfile = open('train.txt', 'a')
tfile.write(dialogues)
tfile.close()

tfile = open('val.txt', 'a')
tfile.write(dialogues2)
tfile.close()
# lines = []
# with open('dialogues.txt', 'r', encoding='iso-8859-1') as dialogues:
#     for line in dialogues:
#         lines.append(line)

# print(lines[:10])