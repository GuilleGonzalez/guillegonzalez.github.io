from itertools import combinations, product
from collections import Counter
import matplotlib.pyplot as plt

def main():
    print("DUTCH BLITZ --------------------------------------------------")
    dutch_blitz()
    print("\nRISK --------------------------------------------------")
    risk()
    print("\n\nYAHTZEE! --------------------------------------------------")
    yahtzee()
    print("\nCARD HOUSES --------------------------------------------------")
    card_houses()


def dutch_blitz(plot: bool = False):
    sums, cards = [0] * 37, [i for i in range(1, 11)] * 4
    for c1, c2, c3, c4 in combinations(cards, 4):
        sums[c1 + c2 + c3 + c4 - 4] += 1

    accumulator, total = 0, sum(sums)
    for s, n in enumerate(sums):
        print(f'Starting Sum of {s+4:2}: {n:5,} in {total:,} ({n/total:.3%})  -  Probability Under {s+4:2}: {accumulator:6,} in {total:,} ({accumulator/total:.3%})')
        accumulator += n

    if plot:
        starting_sums = list(range(4, 41))
        percentages = [n / total * 100 for n in sums]
        _, axes = plt.subplots(figsize=(10, 6))
        axes.bar(starting_sums, percentages, edgecolor='black')
        axes.set_xlabel('Starting Sum')
        axes.set_ylabel('Percentage (%)')
        axes.set_title('Percentage Distribution of Starting Sums in Dutch Blitz')
        axes.set_xticks(starting_sums)
        axes.set_yticks([i * 0.5 for i in range(0, 15)])
        axes.set_xlim(min(starting_sums) - 0.5, max(starting_sums) + 0.5)
        axes.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig('Dutch-Blitz.png')
        plt.close()


def risk():
    DIE = range(1, 7)
    def attacker1_vs_defender1():
        a_wins, d_wins = 0, 0
        for a, d in product(DIE, repeat=2):
            if a > d: a_wins += 1
            else: d_wins += 1
        print_data(1, 1, a_wins, d_wins, 6*6)
        

    def attacker2_vs_defender1():
        a_wins, d_wins = 0, 0
        for a1, a2, d in product(DIE, repeat=3):
            if max(a1, a2) > d: a_wins += 1
            else: d_wins += 1
        print_data(2, 1, a_wins, d_wins, 6*6*6)


    def attacker3_vs_defender1():
        a_wins, d_wins = 0, 0
        for a1, a2, a3, d in product(DIE, repeat=4):
            if max(a1, a2, a3) > d: a_wins += 1
            else: d_wins += 1
        print_data(3, 1, a_wins, d_wins, 6*6*6*6)


    def attacker1_vs_defender2():
        a_wins, d_wins = 0, 0
        for a, d1, d2 in product(DIE, repeat=3):
            if a > max(d1, d2): a_wins += 1
            else: d_wins += 1
        print_data(1, 2, a_wins, d_wins, 6*6*6)

    def attacker2_vs_defender2():
        a_both, each_win, d_both = 0, 0, 0
        for a1, a2, d1, d2 in product(DIE, repeat=4):
            a, d = sorted([a1, a2]), sorted([d1, d2])
            if a[1] > d[1] and a[0] > d[0]: a_both += 1
            elif a[1] <= d[1] and a[0] <= d[0]: d_both += 1
            else: each_win += 1
        print_data(2, 2, a_both, d_both, 6*6*6*6, each_win)


    def attacker3_vs_defender2():
        a_both, each_win, d_both = 0, 0, 0
        for a1, a2, a3, d1, d2 in product(DIE, repeat=5):
            a, d = sorted([a1, a2, a3]), sorted([d1, d2])
            if a[2] > d[1] and a[1] > d[0]: a_both += 1
            elif a[2] <= d[1] and a[1] <= d[0]: d_both += 1
            else: each_win += 1
        print_data(3, 2, a_both, d_both, 6*6*6*6*6, each_win)


    def print_data(a: int, d: int, a_wins: int, d_wins: int, total: int, each_win=0):
        print(f"\n{a} Attacker{'s' if a > 1 else ''} vs. {d} Defender{'s' if d > 1 else ''}")
        if a > 1 and d > 1:
            print(f'Attacker Wins Both: {a_wins}/{total} ({a_wins/total:.4%})')
            print(f'Each Lose One: {each_win}/{total} ({each_win/total:.4%})')
            print(f'Defender Wins Both: {d_wins}/{total} ({d_wins/total:.4%})')
        else: 
            print(f'Attacker Wins: {a_wins}/{total} ({a_wins/total:.4%})')
            print(f'Defender Wins: {d_wins}/{total} ({d_wins/total:.4%})')


    attacker1_vs_defender1()
    attacker2_vs_defender1()
    attacker3_vs_defender1()
    attacker1_vs_defender2()
    attacker2_vs_defender2()
    attacker3_vs_defender2()


def yahtzee():
    fillable, sections = [0]*13,  ['Aces', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes', '3 of a Kind', '4 of a Kind', 'Full House', 'SM Straight', 'LG Straight', 'YAHTZEE', 'Chance']
    for d1, d2, d3, d4, d5 in product(range(1, 7), repeat=5):
        dice_rolls = [d1, d2, d3, d4, d5]
        sorted_unique_dice = sorted(set(dice_rolls))
        dice_counts = sorted(Counter(dice_rolls).values())

        for n in range(1, 7):
            if n in sorted_unique_dice: 
                fillable[n-1] += 1

        if max(dice_counts) >= 3: fillable[6] += 1
        if max(dice_counts) >= 4: fillable[7] += 1
        if dice_counts == [2, 3]: fillable[8] += 1

        if sorted_unique_dice in ([1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]):
            fillable[9] += 1
        if sorted_unique_dice in ([1, 2, 3, 4, 5], [2, 3, 4, 5, 6]):
            fillable[10] += 1
        
        if dice_counts == [5]: fillable[11] += 1
        fillable[12] += 1

    for section, filled in zip(sections, fillable):
        print(f'{section:11}: {filled:4}/7776 ({filled/7776:.3%})')


def card_houses():
    for n in range(1, 101):
        card_count = int(n * (3 * n + 1) // 2)
        print(f'{n} Level{'' if n == 1 else 's'} | {card_count} Cards Needed | {(card_count / 54):.2f} Decks Needed')


if __name__ == '__main__':
    main()
