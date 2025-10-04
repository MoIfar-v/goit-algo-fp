import random
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe


def simulate_two_dice(trials):
    counts = Counter()
    for _ in range(trials):
        a = random.randint(1, 6)
        b = random.randint(1, 6)
        counts[a + b] += 1

    for s in range(2, 13):
        counts.setdefault(s, 0)
    return dict(counts)


def probs_from_counts(counts, trials):
    return {s: counts[s] / trials for s in sorted(counts)}


def probs_table():
    table = {
        2: [2.78, 1],
        3: [5.56, 2],
        4: [8.33, 3],
        5: [11.11, 4],
        6: [13.89, 5],
        7: [16.67, 6],
        8: [13.89, 5],
        9: [11.11, 4],
        10: [8.33, 3],
        11: [5.56, 2],
        12: [2.78, 1],
    }
    denom = 36
    probs = {s: table[s][1] / denom for s in table}
    fracs = {s: (table[s][1], denom) for s in table}
    return probs, fracs


def plot_probs(probs, trials, save=None):
    sums = list(probs.keys())
    values = [probs[s] for s in sums]

    fig, ax1 = plt.subplots(figsize=(10, 6))


    bars = ax1.bar(sums, values, color='#1296F0', edgecolor='black', label='Empirical')
    ax1.set_xlabel('Сума на двох кубиках')
    ax1.set_ylabel('Імовірність')
    ax1.set_title(f'Розподіл ймовірностей сум двох кубиків (симуляція: {trials} разів)')
    ax1.set_xticks(sums)


    for bar, val in zip(bars, values):
        ax1.text(bar.get_x() + bar.get_width() / 2, val + 0.001, f"{val*100:.2f}%", ha='center', va='bottom')


    theo_probs, _ = probs_table()
    theo_values = [theo_probs[s] for s in sums]
    ax1.plot(sums, theo_values, marker='o', color='red', label='Theoretical')
    ax1.legend(loc='upper left')


    theo_probs, _ = probs_table()
    deviations_pp = [(probs[s] - theo_probs[s]) * 100 for s in sums]


    for bar, dev_pp in zip(bars, deviations_pp):
        y = 0.0136
        text = f"{dev_pp:+.2f} p.p."

        if dev_pp < 0:
            text_color = '#D62728'  
        elif dev_pp > 0:
            text_color = '#2CA02C'  
        else:
            text_color = '#888888'  

        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            y,
            text,
            ha='center',
            va='center',
            color=text_color,
            fontsize=7,
            fontweight='bold',
            path_effects=[pe.withStroke(linewidth=2, foreground='black')],
        )

    fig.tight_layout()
    if save:
        plt.savefig(save, dpi=200)
        print(f"Chart saved to {save}")
    plt.show()


if __name__ == '__main__':
    seed = random.seed()
    trials = 100000

    counts = simulate_two_dice(trials)
    probs = probs_from_counts(counts, trials)
    plot_probs(probs, trials)
