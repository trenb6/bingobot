import numpy as np
import pandas as pd

google_sheet_id = "1iw95G45aRZdfxxqgwBZNI6E3dyKgQvNskmO6_Ouei88"
file_url = f"https://docs.google.com/spreadsheets/d/{google_sheet_id}/export?format=xlsx"

individual = "individual"
team = "team"
individualhard = "individualhard"
teamhard = "teamhard"

emma = "Emmahard"
gerard = "Gérardhard"
tren = "Trenhard"
tim = "Timhard"
wessel = "Wesselhard"

df_ind = pd.read_excel(io=file_url, sheet_name=individual, engine="openpyxl")
df_ind["Challenge"] = df_ind["Challenge"].astype(str)
df_ind["Game"] = df_ind["Game"].astype(str)

df_team = pd.read_excel(io=file_url, sheet_name=team, engine="openpyxl")
df_team["Challenge"] = df_team["Challenge"].astype(str)
df_team["Game"] = df_team["Game"].astype(str)

df_ind_hard = pd.read_excel(io=file_url, sheet_name=individualhard, engine="openpyxl")
df_ind_hard["Challenge"] = df_ind_hard["Challenge"].astype(str)
df_ind_hard["Game"] = df_ind_hard["Game"].astype(str)

df_team_hard = pd.read_excel(io=file_url, sheet_name=teamhard, engine="openpyxl")
df_team_hard["Challenge"] = df_team_hard["Challenge"].astype(str)
df_team_hard["Game"] = df_team_hard["Game"].astype(str)

# remove é, replace with e, and make lowercase
df_team["For who?"] = df_team["For who?"].astype(str).str.replace("é", "e").str.lower()
df_team_hard["For who?"] = df_team_hard["For who?"].astype(str).str.replace("é", "e").str.lower()
df_ind["For who?"] = df_ind["For who?"].astype(str).str.replace("é", "e").str.lower()
df_ind_hard["For who?"] = df_ind_hard["For who?"].astype(str).str.replace("é", "e").str.lower()

df_emma = pd.read_excel(io=file_url, sheet_name=emma, engine="openpyxl")
df_emma["Challenge"] = df_emma["Challenge"].astype(str)
df_emma["Game"] = df_emma["Game"].astype(str)

df_gerard = pd.read_excel(io=file_url, sheet_name=gerard, engine="openpyxl")
df_gerard["Challenge"] = df_gerard["Challenge"].astype(str)
df_gerard["Game"] = df_gerard["Game"].astype(str)

df_tren = pd.read_excel(io=file_url, sheet_name=tren, engine="openpyxl")
df_tren["Challenge"] = df_tren["Challenge"].astype(str)
df_tren["Game"] = df_tren["Game"].astype(str)

df_tim = pd.read_excel(io=file_url, sheet_name=tim, engine="openpyxl")
df_tim["Challenge"] = df_tim["Challenge"].astype(str)
df_tim["Game"] = df_tim["Game"].astype(str)

df_wessel = pd.read_excel(io=file_url, sheet_name=wessel, engine="openpyxl")
df_wessel["Challenge"] = df_wessel["Challenge"].astype(str)
df_wessel["Game"] = df_wessel["Game"].astype(str)

df_team["For who?"] = df_team["For who?"].str.split(", ")
df_team_hard["For who?"] = df_team_hard["For who?"].str.split(", ")
df_ind["For who?"] = df_ind["For who?"].str.split(", ")
df_ind_hard["For who?"] = df_ind_hard["For who?"].str.split(", ")

def apply_player_availability_filters(
    df_team,
    df_team_hard,
    df_ind,
    df_ind_hard,
    player_list,
    person_column="For who?",
    player_cols=("2 man", "3 man", "4 man", "5 man")
):
    player_set = set(player_list)

    def count_available_players(players):
        return len(player_set & set(players))

    def row_has_any_person(people):
        return any(person in player_set for person in people)

    def has_enough_players(row):
        available = row["available_players"]

        valid_cols = [
            col for col in player_cols
            if int(col.split()[0]) <= available
        ]

        if not valid_cols:
            return False

        return (row[valid_cols] == "O").any()

    df_team = df_team.copy()
    df_team_hard = df_team_hard.copy()

    # Count available players for team exercises
    df_team["available_players"] = df_team[person_column].apply(count_available_players)
    df_team_hard["available_players"] = df_team_hard[person_column].apply(count_available_players)

    # Keep only team exercises that can be done with the available number of players
    df_team = df_team[df_team.apply(has_enough_players, axis=1)]
    df_team_hard = df_team_hard[df_team_hard.apply(has_enough_players, axis=1)]

    # Keep only individual exercises that include at least one selected player
    df_ind = df_ind[df_ind[person_column].apply(row_has_any_person)]
    df_ind_hard = df_ind_hard[df_ind_hard[person_column].apply(row_has_any_person)]

    return df_team, df_team_hard, df_ind, df_ind_hard


def personal_hard_draw(players_list, number_of_players):
    bingo_list_pers_hard = []

    # for each player in player list, random select one hard challenge for that player and add it to the bingo list
    for player in players_list:
        if player == 'emma':
            df_draw = df_emma
        elif player == 'gerard':
            df_draw = df_gerard
        elif player == 'tren':
            df_draw = df_tren
        elif player == 'tim':
            df_draw = df_tim
        elif player == 'wessel':
            df_draw = df_wessel

        random_index = np.random.choice(df_draw.index)
        game = df_draw.loc[random_index, 'Game']
        challenge = df_draw.loc[random_index, 'Challenge']
        bingo_list_pers_hard.append(f'{player}: {game} - {challenge}')
    
    return(bingo_list_pers_hard)

def individual_hard_draw(df_ind_hard, n_draw):
    used_games = []
    bingo_list_ind_hard = []

    while len(bingo_list_ind_hard) < n_draw:
        random_index = np.random.choice(df_ind_hard.index)
        game = df_ind_hard.loc[random_index, 'Game']
        challenge = df_ind_hard.loc[random_index, 'Challenge']

        if game not in used_games:
            bingo_list_ind_hard.append(f'Individual hard: {game} - {challenge}')
            used_games.append(game)

    return bingo_list_ind_hard


def individual_draw(df_ind, n):
    used_challenges = []
    bingo_list_ind = []

    while len(bingo_list_ind) < n:
        random_index = np.random.choice(df_ind.index)
        game = df_ind.loc[random_index, 'Game']
        challenge = df_ind.loc[random_index, 'Challenge']

        if challenge not in used_challenges:
            bingo_list_ind.append(f'Individual: {game} - {challenge}')
            used_challenges.append(challenge)

    return bingo_list_ind


def team_hard_draw(df_team_hard, n):
    used_challenges = []
    bingo_list_team_hard = []

    while len(bingo_list_team_hard) < n:
        random_index = np.random.choice(df_team_hard.index)
        game = df_team_hard.loc[random_index, 'Game']
        challenge = df_team_hard.loc[random_index, 'Challenge']

        if challenge not in used_challenges:
            bingo_list_team_hard.append(f'Team hard: {game} - {challenge}')
            used_challenges.append(challenge)

    return bingo_list_team_hard


def team_draw(df_team, n):
    used_challenges = []
    bingo_list_team = []

    while len(bingo_list_team) < n:
        random_index = np.random.choice(df_team.index)
        game = df_team.loc[random_index, 'Game']
        challenge = df_team.loc[random_index, 'Challenge']

        if challenge not in used_challenges:
            bingo_list_team.append(f'Team: {game} - {challenge}')
            used_challenges.append(challenge)

    return bingo_list_team

def large_bingo_draw(players_list, number_of_players, n=25):
    # Use the module-level original DataFrames,
    # but create local filtered versions
    (
        df_team_filtered,
        df_team_hard_filtered,
        df_ind_filtered,
        df_ind_hard_filtered
    ) = apply_player_availability_filters(
        df_team,
        df_team_hard,
        df_ind,
        df_ind_hard,
        players_list
    )

    bingo_list = []
    number_of_challenges_left = n

    # Personal hard
    personal_bingo_list = personal_hard_draw(players_list, number_of_players)
    bingo_list.extend(personal_bingo_list)

    amount_of_pers_hard_challenges = len(personal_bingo_list)
    number_of_challenges_left -= amount_of_pers_hard_challenges

    # Individual hard
    extra_ind_hard = []

    if len(personal_bingo_list) < 8:
        number_of_indhard_challenges_left = 8 - amount_of_pers_hard_challenges
        extra_ind_hard = individual_hard_draw(
            df_ind_hard_filtered,
            number_of_indhard_challenges_left
        )
        bingo_list.extend(extra_ind_hard)

    number_of_challenges_left -= len(extra_ind_hard)

    # Individual
    individual_challenges = individual_draw(df_ind_filtered, n=10)
    bingo_list.extend(individual_challenges)

    number_of_challenges_left -= len(individual_challenges)

    # Team hard
    team_hard_challenges = team_hard_draw(df_team_hard_filtered, n=1)
    bingo_list.extend(team_hard_challenges)

    number_of_challenges_left -= len(team_hard_challenges)

    # Team
    team_challenges = team_draw(df_team_filtered, n=6)
    bingo_list.extend(team_challenges)

    number_of_challenges_left -= len(team_challenges)

    return bingo_list

def medium_bingo_draw(players_list, number_of_players, n=16):
    # Use the module-level original DataFrames,
    # but create local filtered versions
    (
        df_team_filtered,
        df_team_hard_filtered,
        df_ind_filtered,
        df_ind_hard_filtered
    ) = apply_player_availability_filters(
        df_team,
        df_team_hard,
        df_ind,
        df_ind_hard,
        players_list
    )

    bingo_list = []
    number_of_challenges_left = n

    # Personal hard
    personal_bingo_list = personal_hard_draw(players_list, number_of_players)
    bingo_list.extend(personal_bingo_list)

    amount_of_pers_hard_challenges = len(personal_bingo_list)
    number_of_challenges_left -= amount_of_pers_hard_challenges

    # Individual hard
    extra_ind_hard = []

    if len(personal_bingo_list) < 4:
        number_of_indhard_challenges_left = 4 - amount_of_pers_hard_challenges
        extra_ind_hard = individual_hard_draw(
            df_ind_hard_filtered,
            number_of_indhard_challenges_left
        )
        bingo_list.extend(extra_ind_hard)

    number_of_challenges_left -= len(extra_ind_hard)

    # Individual
    individual_challenges = individual_draw(df_ind_filtered, n=7)
    bingo_list.extend(individual_challenges)

    number_of_challenges_left -= len(individual_challenges)

    # Team hard
    team_hard_challenges = team_hard_draw(df_team_hard_filtered, n=1)
    bingo_list.extend(team_hard_challenges)

    number_of_challenges_left -= len(team_hard_challenges)

    # Team
    team_challenges = team_draw(df_team_filtered, n=4)
    bingo_list.extend(team_challenges)

    number_of_challenges_left -= len(team_challenges)

    return bingo_list

def small_bingo_draw(players_list, number_of_players, n=9):
    # Use the module-level original DataFrames,
    # but create local filtered versions
    (
        df_team_filtered,
        df_team_hard_filtered,
        df_ind_filtered,
        df_ind_hard_filtered
    ) = apply_player_availability_filters(
        df_team,
        df_team_hard,
        df_ind,
        df_ind_hard,
        players_list
    )

    bingo_list = []
    number_of_challenges_left = n

    # Personal hard
    personal_bingo_list = personal_hard_draw(players_list, number_of_players)
    bingo_list.extend(personal_bingo_list)

    amount_of_pers_hard_challenges = len(personal_bingo_list)
    number_of_challenges_left -= amount_of_pers_hard_challenges

    # Individual hard
    extra_ind_hard = []

    if len(personal_bingo_list) < 3:
        number_of_indhard_challenges_left = 3 - amount_of_pers_hard_challenges
        extra_ind_hard = individual_hard_draw(
            df_ind_hard_filtered,
            number_of_indhard_challenges_left
        )
        bingo_list.extend(extra_ind_hard)

    number_of_challenges_left -= len(extra_ind_hard)

    # Individual
    individual_challenges = individual_draw(df_ind_filtered, n=3)
    bingo_list.extend(individual_challenges)

    number_of_challenges_left -= len(individual_challenges)

    # # Team hard
    # team_hard_challenges = team_hard_draw(df_team_hard_filtered, n=1)
    # bingo_list.extend(team_hard_challenges)

    # number_of_challenges_left -= len(team_hard_challenges)

    # Team
    team_challenges = team_draw(df_team_filtered, n=3)
    bingo_list.extend(team_challenges)

    number_of_challenges_left -= len(team_challenges)

    return bingo_list

def personal_hard_player_draw(player):

    player_dfs = {
        'emma': df_emma,
        'gerard': df_gerard,
        'tren': df_tren,
        'tim': df_tim,
        'wessel': df_wessel
    }

    df_draw = player_dfs[player]

    random_index = np.random.choice(df_draw.index)

    game = df_draw.loc[random_index, 'Game']
    challenge = df_draw.loc[random_index, 'Challenge']

    return f'{player}: {game} - {challenge}'

def draw_one_challenge(challenge_type, players_list=None):

    if players_list is not None:
        (
            df_team_filtered,
            df_team_hard_filtered,
            df_ind_filtered,
            df_ind_hard_filtered
        ) = apply_player_availability_filters(
            df_team,
            df_team_hard,
            df_ind,
            df_ind_hard,
            players_list
        )
    else:
        df_team_filtered = df_team
        df_team_hard_filtered = df_team_hard
        df_ind_filtered = df_ind
        df_ind_hard_filtered = df_ind_hard

    if challenge_type == "Individual":
        return individual_draw(df_ind_filtered, 1)[0]

    elif challenge_type == "Individual hard":
        return individual_hard_draw(df_ind_hard_filtered, 1)[0]

    elif challenge_type == "Team":
        return team_draw(df_team_filtered, 1)[0]

    elif challenge_type == "Team hard":
        return team_hard_draw(df_team_hard_filtered, 1)[0]

    # Personal hard challenges
    elif challenge_type in ['emma', 'gerard', 'tren', 'tim', 'wessel']:
        return personal_hard_player_draw(challenge_type)

    else:
        raise ValueError(f"Unknown challenge type: {challenge_type}")


def custom_bingo_draw(players_list, n_individual_hard, n_individual, n_team_hard, n_team):
    (
        df_team_filtered,
        df_team_hard_filtered,
        df_ind_filtered,
        df_ind_hard_filtered
    ) = apply_player_availability_filters(
        df_team,
        df_team_hard,
        df_ind,
        df_ind_hard,
        players_list
    )

    challenges = []

    challenges.extend(individual_hard_draw(df_ind_hard_filtered, n_individual_hard))
    challenges.extend(individual_draw(df_ind_filtered, n_individual))
    challenges.extend(team_hard_draw(df_team_hard_filtered, n_team_hard))
    challenges.extend(team_draw(df_team_filtered, n_team))
    
    return challenges


