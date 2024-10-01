import random
#import matplotlib.pyplot as plt
from collections import Counter
from statistics  import mean
from itertools   import combinations, permutations, product
from functools   import lru_cache
import math

two_card_probs = {'AAd': 0.849332, 'KKd': 0.821185, 'QQd': 0.79633, 'JJd': 0.771539, 'TTd': 0.74661,
'99d': 0.716662, '88d': 0.687178, 'AKs': 0.662206, '77d': 0.657255, 'AQs': 0.653146, 'KAd': 0.644704,
'AJs': 0.643984, 'QAd': 0.635098, 'ATs': 0.634895, '66d': 0.627001, 'JAd': 0.625361, 'QKs': 0.624092,
'TAd': 0.615689, 'A9s': 0.615102, 'JKs': 0.614773, 'TKs': 0.605876, 'A8s': 0.605083, 'KQd': 0.60433,
'55d': 0.5964, '9Ad': 0.594505, 'KJd': 0.59442, 'A7s': 0.593871, 'JQs': 0.590714, '9Ks': 0.586386,
'KTd': 0.58495, '8Ad': 0.583749, 'A6s': 0.581794, 'TQs': 0.58171, 'A5s': 0.580647, '7Ad': 0.571701,
'A4s': 0.571385, 'QJd': 0.569068, '8Ks': 0.567908, 'K9d': 0.564082, 'A3s': 0.563359, '44d': 0.562565,
'9Qs': 0.562231, 'TJs': 0.561549, 'QTd': 0.559479, '6Ad': 0.558709, '7Ks': 0.558467, '5Ad': 0.557428,
'A2s': 0.555072, '6Ks': 0.548051, '4Ad': 0.547334, 'K8d': 0.544322, '8Qs': 0.544172, '9Js': 0.54112,
'Q9d': 0.538624, '3Ad': 0.538559, '5Ks': 0.538343, 'JTd': 0.538263, 'K7d': 0.534179, '2Ad': 0.52948,
'4Ks': 0.528894, '33d': 0.528393, '7Qs': 0.525237, '9Ts': 0.523766, '8Js': 0.523116, 'K6d': 0.522976,
'3Ks': 0.520709, 'Q8d': 0.519309, '6Qs': 0.516795, 'J9d': 0.516396, 'K5d': 0.512544, '2Ks': 0.512408, 
'5Qs': 0.507138, '8Ts': 0.505088, '7Js': 0.504545, 'K4d': 0.502257, 'Q7d': 0.499046, 'T9d': 0.498157, 
'4Qs': 0.497635, 'J8d': 0.497138, '22d': 0.493853, 'K3d': 0.493318, 'Q6d': 0.489969, '3Qs': 0.48939, 
'89s': 0.488556, '7Ts': 0.486509, '6Js': 0.485744, 'K2d': 0.484234, '2Qs': 0.481025, 'Q5d': 0.479594, 
'5Js': 0.478211, 'T8d': 0.478181, 'J7d': 0.477262, '79s': 0.469897, 'Q4d': 0.469252, '4Js': 0.468689, 
'6Ts': 0.468, '98d': 0.460681, '3Js': 0.460422, 'Q3d': 0.460254, 'T7d': 0.458297, 'J6d': 0.457135, 
'78s': 0.456832, '2Js': 0.45203, '69s': 0.451506, 'Q2d': 0.451104, '5Ts': 0.44939, 'J5d': 0.449049, 
'4Ts': 0.442042, '97d': 0.440718, 'J4d': 0.438691, 'T6d': 0.43848, '68s': 0.438176, '3Ts': 0.433787, 
'59s': 0.433124, 'J3d': 0.429671, '67s': 0.428282, '87d': 0.426928, '2Ts': 0.425406, '96d': 0.42103, 
'J2d': 0.420497, '58s': 0.419898, 'T5d': 0.418572, '49s': 0.414071, 'T4d': 0.410556, '57s': 0.409779, 
'39s': 0.408069, '86d': 0.406961, '56s': 0.403467, 'T3d': 0.401555, '95d': 0.401363, '48s': 0.401024, 
'29s': 0.399732, '76d': 0.396531, 'T2d': 0.392394, '47s': 0.391082, '85d': 0.387407, '45s': 0.38531, 
'46s': 0.384798, '38s': 0.382826, '94d': 0.380853, '28s': 0.376793, '75d': 0.37674, '93d': 0.374281, 
'37s': 0.373032, '65d': 0.37012, '35s': 0.367575, '84d': 0.367087, '36s': 0.366846, '92d': 0.365172, 
'34s': 0.357262, '74d': 0.356611, '27s': 0.354398, '54d': 0.350747, '64d': 0.350023, '25s': 0.349287, 
'26s': 0.348371, '83d': 0.347492, '82d': 0.34087, '24s': 0.339172, '73d': 0.337173, '53d': 0.331649, 
'23s': 0.330913, '63d': 0.330691, '43d': 0.320662, '72d': 0.317095, '52d': 0.311937, '62d': 0.310778, 
'42d': 0.301174, '32d': 0.292395}


class Card:
    def __init__(self, number, suit):
        self.suit = suit
        self.number = number
        rankstr = '23456789TJQKA'
        self.rank = rankstr.index(self.number) + 2

    def __ge__(self, other):
        return self.rank >= other.rank

    def __repr__(self):
        return "{0}{1}".format(self.number, self.suit)

    def __eq__(self, other):
        return (isinstance(other, Card) and self.suit == other.suit and
        self.number == other.number)


c1 = Card("A", "s")
c2 = Card("7", "h")
c3 = Card("6", "d")
c4 = Card("A", "d")
c5 = Card("7", "s")

hand = [c1, c2, c3, c4, c5]

def is_flush(hand):
    ranks = []
    for c in hand:
        ranks.append(c.rank)
    ranks.sort()

    most = 0
    count = 0
    suit = hand[0].suit
    for c in hand:
        if c.suit == suit:
            count += 1
            if c.rank > most:
                most = c.rank

    if count == 5:
        return tuple(sorted(ranks, reverse=True))
    else:
        return False

def is_straight(hand):
    ranks = []
    for c in hand:
        ranks.append(c.rank)

    ranks.sort()
    if ranks == [2, 3, 4, 5, 14]:
        ranks = (1, 2, 3, 4, 5)

    else:
        ranks = tuple(ranks)

    for i in range(len(ranks)):
        if i == len(ranks) - 1:
            return tuple(sorted(ranks, reverse = True))
        elif ranks[i] + 1 != ranks[i + 1]:
            return False

c1 = Card("3", "s")
c2 = Card("4", "s")
c3 = Card("5", "h")
c4 = Card("6", "s")
c5 = Card("7", "d")

hand2 = [c1, c2, c3, c4, c5]
#print(is_flush(hand))



def ranking0(hand):
    count = Counter(map(lambda crd: crd.rank, hand))
    ordered = sorted(((count[r], r) for r in count), reverse=True)
    rank = tuple(zip(*ordered))
    return(rank)

def ranking_final(hand):
    f = is_flush(hand)
    s = is_straight(hand)
    if f != False and s != False:
        rank = ((4, 2), s)

    elif f != False:
        rank = ((3, 1, 3), f)

    elif s != False:
        rank = ((3, 1, 2), s)

    else:
        rank = ranking0(hand)

    return rank

#print(ranking_final(hand))
#print(ranking_final(hand2))
#print(ranking_final(hand) > ranking_final(hand2))
#print(Counter(map(lambda crd: crd.rank, hand)))

#print(hand_type(hand))
def cards(h):
    c1 = h[0:2]
    c2 = h[3:5]
    c3 = h[6:8]
    c4 = h[9:11]
    c5 = h[12:14]

    hand = [c1, c2, c3, c4, c5]

    for i in range(len(hand)):
        hand[i] = Card(hand[i][0], hand[i][1])

    return hand
hands = [cards(h) for h in (           
    'As Ac Ah Ad Ad', 'Kh Kd Ks Kc Kh', '3h 3s 3d 3c 3c', '2s 2c 2d 2h 2h', # 5 of a kind     
    'As Ks Qs Ts Js', 'Kc Qc Jc Tc 9c', '6d 5d 4d 3d 2d', '5h 4h 3h 2h Ah', # straight flush  
    'As Ac Ad Ah 2s', '7s 7c 7d 2d 7h', '6s 6c 6d 6h 9s', 'As 5h 5c 5d 5s', # four of a kind 
    'Th Tc Td 5h 5c', '9h 9c 9d 8c 8h', '6h 6c 6d Tc Th', '5c 5d 5s As Ah', # full house
    'As 2s 3s 4s 6s', 'Kc Qc Jc Tc 2c', 'Qc Jc Tc 9c 7c', '4h 5h 6h 7h 9h', # flush
    'As Kd Qc Td Jh', 'Kc Qh Jd Th 9c', '6c 5d 4h 3s 2s', 'As 2d 3c 4h 5s', # straight
    'As Ac Ad 2h 3h', 'Ts Tc Th 9s 8c', 'Ts Tc Th 9s 7c', '9h 9s 9d Ah Kh', # three of a kind
    'Ts Tc 5s 5c 8h', 'Ts Tc 5s 5c 7h', '9s 9c 8s 8c As', '3s 3c 2s 2d Ah', # two pair 
    'As Ac 4c 5s 6s', '4s 4c As Ks Qs', '4h 4d Kh Qd Jd', '2d 2c Ad Kd Qd', # pair 
    'Ah 3s 4s 5s 6s', 'Kh Qh Jh Th 8d', '7d 2s 4s 5s 6s', '7h 6s 5d 3s 2d', # high card
         )]

def the_same(things) -> bool: 
    """Are all the things actually the same?"""
    return len(set(things)) <= 1

def test(ranking, hands=hands) -> bool:
    """Test that `ranking` preserves order of `hands`, and that permuting cards is irrelevant."""
    assert hands == sorted(hands, key=ranking, reverse=True)
    #trans = str.maketrans('shdc', 'hscd')
    for hand in hands: 
        print(the_same(ranking(h) for h in permutations(hand)))
        #assert the_same([ranking(hand), ranking([c.suit.translate(trans) for c in hand])])
    return len(hands)

def winner(hands):
    return max(hands, key=ranking_final)

def winners(hands):
    best = ranking_final(winner(hands))
    winners = tuple(filter(lambda c: ranking_final(c) == best, hands))
    return winners

def texas_best(hole, table):
    return winner(combinations(hole + table, 5))

def hand_type(hand):
    rank = ranking_final(hand)
    rank_to_number = {1: "Ace", 2: "Twos", 3: "Threes", 4: "Fours", 5: "Fives", 6: "Sixes", 7: "Sevens", 8: "Eights", 9: "Nines", 
    10: "Tens", 11: "Jacks", 12: "Queens", 13: "Kings", 14: "Aces"}

    d = {(4, 2): f"Straight flush with {rank_to_number[rank[1][0]][:-1] if rank[1][0] != 6 else 'Six'} high", (4, 1): f"Four {rank_to_number[rank[1][0]]}", 
    (3, 2): f"Full house with three {rank_to_number[rank[1][0]]}", (3, 1, 3): f"Flush with {rank_to_number[rank[1][0]][:-1]} high", 
    (3, 1, 2): f"Straight with {rank_to_number[rank[1][0]][:-1] if rank[1][0] != 6 else 'Six'} high",
    (3, 1, 1): f"Three {rank_to_number[rank[1][0]]}", (2, 2, 1): f"Pair of {rank_to_number[rank[1][0]]} and Pair of {rank_to_number[rank[1][1]]}", 
    (2, 1, 1, 1): f"One pair of {rank_to_number[rank[1][0]]}", (1, 1, 1, 1, 1): f"{rank_to_number[rank[1][0]][:-1]} high"}
    if d[rank[0]].startswith("Straight flush") and rank[1][0] == 14:
        return "Royal Flush"

    else:
        return d[rank[0]]

def chance_of_win(hand):
    possible_opponent_hands = 2598959
    hands_we_win = 0
    hands_we_tie = 0
    hands_we_lose = 0
    if hand_type(hand) == "royal flush":
        hands_we_tie = 3
        hands_we_lose = 0
        hands_we_win = (possible_opponent_hands - hands_we_tie - hands_we_lose)

        return "Prob of win: {0}, Prob of tie: {1}, Prob of loss: {2}".format(
            hands_we_win/possible_opponent_hands, hands_we_tie/possible_opponent_hands, hands_we_lose/possible_opponent_hands
        )

    hands_we_lose += 4

    if hand_type(hand) == "straight flush":
        rank = ranking_final(hand)
        highest_rank = rank[1][0]
        cards_higher = 4*(13 - highest_rank)
        cards_same = 3
        hands_we_lose += cards_higher
        hands_we_tie = cards_same
        hands_we_win = (possible_opponent_hands - hands_we_tie - hands_we_lose)

        return "Prob of win: {0}, Prob of tie: {1}, Prob of loss: {2}".format(
            hands_we_win/possible_opponent_hands, hands_we_tie/possible_opponent_hands, hands_we_lose/possible_opponent_hands
        )

    hands_we_lose += 36
    if hand_type(hand) == "four of a kind":
        rank = ranking_final(hand)
        fours_rank = rank[1][0]
        off_card_rank = rank[1][1]
        if off_card_rank > fours_rank:
            fours_higher = (14 - highest_rank - 1)*(52-9)
        else:
            fours_higher = 14 - highest_rank*(52-9)
        hands_we_lose += fours_higher
        hands_we_tie = 0
        hands_we_win = (possible_opponent_hands - hands_we_tie - hands_we_lose)

        return "Prob of win: {0}, Prob of tie: {1}, Prob of loss: {2}".format(
            hands_we_win/possible_opponent_hands, hands_we_tie/possible_opponent_hands, hands_we_lose/possible_opponent_hands
        )

    hands_we_lose += 624

    if hand_type(hand) == "full house":
        rank = ranking_final(hand)
        house_rank = rank[1][0]
        houses_higher = ((14-house_rank) / (14-3)) * 3744 

        hands_we_lose += houses_higher
        hands_we_win = (possible_opponent_hands - hands_we_lose)

        return "Prob of win: {0} Prob of loss: {1}".format(
            hands_we_win/possible_opponent_hands, hands_we_lose/possible_opponent_hands)

    hands_we_lose += 3744

    if hand_type(hand) == "flush":
        rank = ranking_final(hand)
        flush_rank = rank[1][0]
        flushes_higher = ((14 - flush_rank)/(14-6)) * 5106
        hands_we_lose += flushes_higher
        hands_we_win = possible_opponent_hands - hands_we_lose
        return "Prob of win: {0} Prob of loss: {1}".format(
            hands_we_win/possible_opponent_hands, hands_we_lose/possible_opponent_hands)

    hands_we_lose += 5106

    if hand_type(hand) == "straight":
        rank = ranking_final(hand)
        straight_rank = rank[1][0]
        14 - 5
        straights_higher = ((14 - straight_rank)/(14-5)) * 10200
        hands_we_lose += straights_higher
        hands_we_win = possible_opponent_hands - hands_we_lose
        return "Prob of win: {0} Prob of loss: {1}".format(
            hands_we_win/possible_opponent_hands, hands_we_lose/possible_opponent_hands)

    hands_we_lose += 10200

    if hand_type(hand) == "three of a kind":
        rank = ranking_final(hand)
        threes_rank = rank[1][0]
        threes_higher = ((14 - threes_rank)/(14-2)) * 54912
        hands_we_lose += threes_higher
        hands_we_win = possible_opponent_hands - hands_we_lose
        return "Prob of win: {0} Prob of loss: {1}".format(
            hands_we_win/possible_opponent_hands, hands_we_lose/possible_opponent_hands)

    hands_we_lose += 54912

    if hand_type(hand) == "two pair":
        rank = ranking_final(hand)
        two_pairs_rank = rank[1][0]
        two_pairs_higher = ((14 - two_pairs_rank)/(14-3)) * 123552
        hands_we_lose += two_pairs_higher
        hands_we_win = possible_opponent_hands - hands_we_lose
        return "Prob of win: {0} Prob of loss: {1}".format(
            hands_we_win/possible_opponent_hands, hands_we_lose/possible_opponent_hands)

    hands_we_lose += 123552

    if hand_type(hand) == "one pair":
        rank = ranking_final(hand)
        pair_rank = rank[1][0]
        pairs_higher = ((14 - pair_rank)/(14-2)) * 1098240
        hands_we_lose += pairs_higher
        hands_we_win = possible_opponent_hands - hands_we_lose
        return "Prob of win: {0} Prob of loss: {1}".format(
            hands_we_win/possible_opponent_hands, hands_we_lose/possible_opponent_hands)

    hands_we_lose += 1098240

    if hand_type(hand) == "high card":
        rank = ranking_final(hand)
        card_rank = rank[1][0]
        cards_higher = ((14 - card_rank)/(14-2)) * 1302540
        hands_we_lose += cards_higher
        hands_we_win = possible_opponent_hands - hands_we_lose
        return "Prob of win: {0} Prob of loss: {1}".format(
            hands_we_win/possible_opponent_hands, hands_we_lose/possible_opponent_hands)



card_deck = (Card("A", "h"), Card("2", "h"), Card("3", "h"), Card("4", "h"), Card("5", "h"), Card("6", "h"), Card("7", "h"),
             Card("8", "h"), Card("9", "h"), Card("T", "h"), Card("J", "h"), Card("Q", "h"), Card("K", "h"), 

             Card("A", "s"), Card("2", "s"), Card("3", "s"), Card("4", "s"), Card("5", "s"), Card("6", "s"), Card("7", "s"),
             Card("8", "s"), Card("9", "s"), Card("T", "s"), Card("J", "s"), Card("Q", "s"), Card("K", "s"),
             
             Card("A", "c"), Card("2", "c"), Card("3", "c"), Card("4", "c"), Card("5", "c"), Card("6", "c"), Card("7", "c"),
             Card("8", "c"), Card("9", "c"), Card("T", "c"), Card("J", "c"), Card("Q", "c"), Card("K", "c"),
             
             Card("A", "d"), Card("2", "d"), Card("3", "d"), Card("4", "d"), Card("5", "d"), Card("6", "d"), Card("7", "d"),
             Card("8", "d"), Card("9", "d"), Card("T", "d"), Card("J", "d"), Card("Q", "d"), Card("K", "d"))


def probs_of_win(hand1, hand2, table):
    if len(table) == 5:
        p1_best_hand = texas_best(hand1, table)
        p2_best_hand = texas_best(hand2, table)
        if ranking_final(p1_best_hand) > ranking_final(p2_best_hand):
            return "P1 win prob: {0}, P2 win prob: {1}, Tie prob: {2}".format(100.00, 0.00, 0.00)
        elif ranking_final(p1_best_hand) == ranking_final(p2_best_hand):
            return "P1 win prob: {0}, P2 win prob: {1}, Tie prob: {2}".format(0.00, 0.00, 100.00)
        else:
            return "P1 win prob: {0}, P2 win prob: {1}, Tie prob: {2}".format(0.00, 100.00, 0.00)

    elif len(table) == 4:
        P1_wins = 0
        P2_wins = 0
        ties = 0
        for card in list(random.sample(card_deck, 15)):
            #print(card)
            if card not in table + hand1 + hand2:
                p1_best_hand = texas_best(hand1, table + [card])
                p2_best_hand = texas_best(hand2, table + [card])

                if ranking_final(p1_best_hand) > ranking_final(p2_best_hand):
                    P1_wins += 1
                elif ranking_final(p1_best_hand) == ranking_final(p2_best_hand):
                    ties += 1
                else:
                    P2_wins += 1

        total = P1_wins + P2_wins + ties
        P1_win_prob = P1_wins / total
        P2_win_prob = P2_wins / total
        tie_prob = ties / total
        return "P1 win prob: {0}, P2 win prob: {1}, Tie prob: {2}".format(P1_win_prob, P2_win_prob, tie_prob)

    elif len(table) == 3:
        P1_wins = 0
        P2_wins = 0
        ties = 0

        for card1 in list(random.sample(card_deck, 15)):
            #print(card)
            if card1 not in table + hand1 + hand2:
                for card2 in list(random.sample(card_deck, 15)):
                    if card2 not in table + hand1 + hand2 and card2 != card1:
                        p1_best_hand = texas_best(hand1, table + [card1, card2])
                        p2_best_hand = texas_best(hand2, table + [card1, card2])

                        if ranking_final(p1_best_hand) > ranking_final(p2_best_hand):
                            P1_wins += 1
                        elif ranking_final(p1_best_hand) == ranking_final(p2_best_hand):
                            ties += 1
                        else:
                            P2_wins += 1

        total = P1_wins + P2_wins + ties
        P1_win_prob = P1_wins / total
        P2_win_prob = P2_wins / total
        tie_prob = ties / total
        return "P1 win prob: {0}, P2 win prob: {1}, Tie prob: {2}".format(P1_win_prob, P2_win_prob, tie_prob)



def winning_hand(hand, table, num_players):
    P1_wins = 0
    P2_wins = 0
    ties = 0
    if len(table) == 5:
        for opp_card1 in random.sample(card_deck, 15):
            if opp_card1 not in hand + table:
                for opp_card2 in random.sample(card_deck, 15):
                    if opp_card2 not in hand + table and opp_card2 != opp_card1:
                        p1_best_hand = texas_best(hand, table)
                        p2_best_hand = texas_best([opp_card1, opp_card2], table)
                        if ranking_final(p1_best_hand) > ranking_final(p2_best_hand):
                            P1_wins += 1
                        elif ranking_final(p1_best_hand) == ranking_final(p2_best_hand):
                            ties += 1
                        else:
                            P2_wins += 1

        total = P1_wins + P2_wins + ties
        P1_win_prob = P1_wins / total
        P2_win_prob = P2_wins / total
        tie_prob = ties / total

        group_win_prob = P1_win_prob ** (num_players-1)
        group_tie_prob = 1 - ((1-tie_prob)**(num_players-1))
        group_lose_prob = 1 - group_win_prob - group_tie_prob
        
        return "Win prob: {0:.2f}".format(group_win_prob) #, group_lose_prob, group_tie_prob)

    if len(table) == 4:
        for opp_card1 in random.sample(card_deck, 10):
            if opp_card1 not in hand + table:
                for opp_card2 in random.sample(card_deck, 10):
                    if opp_card2 not in hand + table and opp_card2 != opp_card1:
                        for draw_card in random.sample(card_deck, 10):
                            if draw_card not in hand + table and opp_card2 != draw_card != opp_card1:
                                p1_best_hand = texas_best(hand, table + [draw_card])
                                p2_best_hand = texas_best([opp_card1, opp_card2], table + [draw_card])
                                if ranking_final(p1_best_hand) > ranking_final(p2_best_hand):
                                    P1_wins += 1
                                elif ranking_final(p1_best_hand) == ranking_final(p2_best_hand):
                                    ties += 1
                                else:
                                    P2_wins += 1

        total = P1_wins + P2_wins + ties
        P1_win_prob = P1_wins / total
        P2_win_prob = P2_wins / total
        tie_prob = ties / total

        group_win_prob = P1_win_prob ** (num_players-1)
        group_tie_prob = 1 - ((1-tie_prob)**(num_players-1))
        group_lose_prob = 1 - group_win_prob - group_tie_prob
        
        return "Win prob: {0:.2f}".format(group_win_prob) #, group_lose_prob, group_tie_prob)


    if len(table) == 3:
        for opp_card1 in random.sample(card_deck, 10):
            if opp_card1 not in hand + table:
                for opp_card2 in random.sample(card_deck, 10):
                    if opp_card2 not in hand + table and opp_card2 != opp_card1:
                        for draw_card in random.sample(card_deck, 10):
                            if draw_card not in hand + table and opp_card2 != draw_card != opp_card1:
                                for draw_card2 in random.sample(card_deck, 10):
                                    if draw_card2 not in hand + table and opp_card2 != draw_card2 != opp_card1 and draw_card2 != draw_card:
                                        p1_best_hand = texas_best(hand, table + [draw_card, draw_card2])
                                        p2_best_hand = texas_best([opp_card1, opp_card2], table + [draw_card, draw_card2])
                                        if ranking_final(p1_best_hand) > ranking_final(p2_best_hand):
                                            P1_wins += 1
                                        elif ranking_final(p1_best_hand) == ranking_final(p2_best_hand):
                                            ties += 1
                                        else:
                                            P2_wins += 1

        total = P1_wins + P2_wins + ties
        P1_win_prob = P1_wins / total
        P2_win_prob = P2_wins / total
        tie_prob = ties / total

        group_win_prob = P1_win_prob ** (num_players-1)
        group_tie_prob = 1 - ((1-tie_prob)**(num_players-1))
        group_lose_prob = 1 - group_win_prob - group_tie_prob
        
        return "Win prob: {0}".format(group_win_prob, ".2f") #, group_lose_prob, group_tie_prob)
    
    
    if len(table) == 2:
        #print(list(random.sample(card_deck, 15)))
        for opp_card1 in random.sample(card_deck, 4):
            if opp_card1 not in hand + table:
                for opp_card2 in random.sample(card_deck, 4):
                    if opp_card2 not in hand + table and opp_card2 != opp_card1:
                        for draw_card in random.sample(card_deck, 4):
                            if draw_card not in hand + table and opp_card2 != draw_card != opp_card1:
                                for draw_card2 in random.sample(card_deck, 4):
                                    if draw_card2 not in hand + table and opp_card2 != draw_card2 != opp_card1 and draw_card2 != draw_card:
                                        for draw_card3 in random.sample(card_deck, 4):
                                            if draw_card3 not in hand + table and opp_card2 != draw_card3 != opp_card1 and draw_card3 != draw_card and draw_card3 != draw_card2:
                                                p1_best_hand = texas_best(hand, table + [draw_card, draw_card2, draw_card3])
                                                p2_best_hand = texas_best([opp_card1, opp_card2], table + [draw_card, draw_card2, draw_card3])
                                                if ranking_final(p1_best_hand) > ranking_final(p2_best_hand):
                                                    P1_wins += 1
                                                elif ranking_final(p1_best_hand) == ranking_final(p2_best_hand):
                                                    ties += 1
                                                else:
                                                    P2_wins += 1

        total = P1_wins + P2_wins + ties
        P1_win_prob = P1_wins / total
        P2_win_prob = P2_wins / total
        tie_prob = ties / total

        group_win_prob = P1_win_prob ** (num_players-1)
        group_tie_prob = 1 - ((1-tie_prob)**(num_players-1))
        group_lose_prob = 1 - group_win_prob - group_tie_prob
        
        return "Win prob: {0}".format(group_win_prob, ".2f") #, group_lose_prob, group_tie_prob)
    
    
    if len(table) == 1:
        #print(list(random.sample(card_deck, 15)))
        for opp_card1 in random.sample(card_deck, 2):
            if opp_card1 not in hand + table:
                for opp_card2 in random.sample(card_deck, 2):
                    if opp_card2 not in hand + table and opp_card2 != opp_card1:
                        for draw_card in random.sample(card_deck, 2):
                            if draw_card not in hand + table and opp_card2 != draw_card != opp_card1:
                                for draw_card2 in random.sample(card_deck, 2):
                                    if draw_card2 not in hand + table and opp_card2 != draw_card2 != opp_card1 and draw_card2 != draw_card:
                                        for draw_card3 in random.sample(card_deck, 2):
                                            if draw_card3 not in hand + table and opp_card2 != draw_card3 != opp_card1 and draw_card3 != draw_card and draw_card3 != draw_card2:
                                                for draw_card4 in random.sample(card_deck, 2):
                                                    if draw_card4 not in hand + table and opp_card2 != draw_card4 != opp_card1 and draw_card4 != draw_card and draw_card4 != draw_card2 and draw_card4 != draw_card3:
                                                        p1_best_hand = texas_best(hand, table + [draw_card, draw_card2, draw_card3, draw_card4])
                                                        p2_best_hand = texas_best([opp_card1, opp_card2], table + [draw_card, draw_card2, draw_card3, draw_card4])
                                                        if ranking_final(p1_best_hand) > ranking_final(p2_best_hand):
                                                            P1_wins += 1
                                                        elif ranking_final(p1_best_hand) == ranking_final(p2_best_hand):
                                                            ties += 1
                                                        else:
                                                            P2_wins += 1

        total = P1_wins + P2_wins + ties
        P1_win_prob = P1_wins / total
        P2_win_prob = P2_wins / total
        tie_prob = ties / total

        group_win_prob = P1_win_prob ** (num_players-1)
        group_tie_prob = 1 - ((1-tie_prob)**(num_players-1))
        group_lose_prob = 1 - group_win_prob - group_tie_prob
        
        return "Win prob: {0}".format(group_win_prob, ".2f") #, group_lose_prob, group_tie_prob)
    
    

    elif len(table) == 0:
        first_number = hand[0].number
        second_number = hand[1].number
        first_suit = hand[0].suit
        second_suit = hand[1].suit

        if first_suit == second_suit:
            if first_number + second_number + "s" in two_card_probs:
                P1_win_prob = two_card_probs[first_number + second_number + "s"]
            else:
               P1_win_prob = two_card_probs[second_number + first_number + "s"]

        else:
            if first_number + second_number + "d" in two_card_probs:
                P1_win_prob = two_card_probs[first_number + second_number + "d"]
            else:
               P1_win_prob = two_card_probs[second_number + first_number + "d"]

        group_win_prob = round(P1_win_prob ** (num_players-1), 3)

        return "Win prob: {0}".format(group_win_prob, ".2f")

#print("A" + "2" + "d" in two_card_probs)

table = []#Card("K", "h"), Card("J", "h"), Card("T", "h")]#, Card("T", "s")]#, Card("4", "h")]


c1 = Card("Q", "h")
c2 = Card("A", "h")


hand1 = [c1, c2]

c3 = Card("A", "d")
c4 = Card("A", "c")

hand2 = [c3, c4]

#print(probs_of_win(hand1, hand2, table))

#print(winning_hand(hand2, table, 5))

#print(probs_of_win(hand1, hand2, table))





