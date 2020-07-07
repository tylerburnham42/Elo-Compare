from itertools import combinations
import random
import json
import os
from operator import itemgetter
import pprint


def calculate_elo(rating1, rating2, winner, k_value):
    """

    """
    transformed1 = 10 ** (rating1/400)
    transformed2 = 10 ** (rating2/400)

    expected1 = transformed1 / (transformed1 + transformed2)
    expected2 = transformed2 / (transformed1 + transformed2)

    score1 = winner
    score2 = 1 - winner

    new_rating1 = rating1 + k_value * (score1 - expected1)
    new_rating2 = rating2 + k_value * (score2 - expected2)

    return([new_rating1, new_rating2])



def make_first_json(input_file, json_file):
    names = {}
    with open(input_file, "r") as input_file:
        for line in input_file:
            if line == "":
                break
            names[line.strip()] = 1000
        
    with open(json_file, 'w') as outfile:
        json.dump(names, outfile, indent=4, sort_keys=True)



def main():
    json_file_path = "save_file.json"
    if not os.path.exists(json_file_path):
        make_first_json("list of musicals.txt", json_file_path)

    names = {}
    with open(json_file_path, 'r') as json_file:
        names = json.load(json_file)

    matchups = list(combinations(names.keys(), 2))
    random.shuffle(matchups)
    for matchup in matchups:
        print("{0} VS {1}".format(matchup[0], matchup[1]))
        print("")
        print("Press 1 for {0}".format(matchup[0]))
        print("Press 2 for {0}".format(matchup[1]))
        print("Press 3 for a draw.")
        print("Press 4 to save and quit.")
        answer = input().strip()

        if answer == '4':
            with open(json_file_path, 'w') as outfile:
                json.dump(names, outfile, indent=4, sort_keys=True)

            rank = []
            for key, value in names.items():
                rank.append([key, value])
            pp = pprint.PrettyPrinter(indent=4)
            rank = sorted(rank, key=itemgetter(1), reverse=True)
            print(pp.pprint(rank))

            return

        elif answer == '3':
            results = calculate_elo(names[matchup[0]], names[matchup[1]], .5, 25)
        
        elif answer == '2':
            results = calculate_elo(names[matchup[0]], names[matchup[1]], 0, 25)
        
        elif answer == '1':
            results = calculate_elo(names[matchup[0]], names[matchup[1]], 1, 25)

        if len(results) == 2:
            names[matchup[0]] = results[0]
            names[matchup[1]] = results[1]

        
if __name__ == "__main__":
    # execute only if run as a script
    main()



