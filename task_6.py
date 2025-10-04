def greedy_algorithm(items, budget):
    # Обчислити коефіцієнт калорійності за одиницю вартості
    ranked = sorted(items.items(), key=lambda kv: (kv[1]['calories'] / kv[1]['cost']), reverse=True)

    chosen: List[str] = []
    total_cal = 0
    remaining = budget
    for name, info in ranked:
        cost = info['cost']
        cal = info['calories']
        if cost <= remaining:
            chosen.append(name)
            total_cal += cal
            remaining -= cost

    return chosen, total_cal


def dynamic_programming(items, budget):
    names = list(items.keys())
    n = len(names)

    # dp[i][w] = максимальна калорійність, використовуючи перші i предметів з бюджетом w
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        name = names[i - 1]
        cost = items[name]['cost']
        cal = items[name]['calories']
        for w in range(budget + 1):
            # не беремо предмет i
            dp[i][w] = dp[i - 1][w]
            # беремо, якщо вистачає бюджету
            if cost <= w:
                cand = dp[i - 1][w - cost] + cal
                if cand > dp[i][w]:
                    dp[i][w] = cand

    w = budget
    chosen = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            name = names[i - 1]
            chosen.append(name)
            w -= items[name]['cost']

    chosen.reverse()
    return chosen, dp[n][budget]


if __name__ == '__main__':
    items = {
        "pizza": {"cost": 50, "calories": 300},
        "hamburger": {"cost": 40, "calories": 250},
        "hot-dog": {"cost": 30, "calories": 200},
        "pepsi": {"cost": 10, "calories": 100},
        "cola": {"cost": 15, "calories": 220},
        "potato": {"cost": 25, "calories": 350}
    }

    try:
        budget = int(input("Введіть бюджет (наприклад 100): "))
    except Exception:
        budget = 100
        
    g_chosen, g_cal = greedy_algorithm(items, budget)
    dp_chosen, dp_cal = dynamic_programming(items, budget)

    print(f"Бюджет: {budget}")
    print("Жадібний вибір:", g_chosen, "калорії=", g_cal)
    print("ДП вибір:", dp_chosen, "калорії=", dp_cal)
