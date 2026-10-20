from profiles import radio, roulette

ALL = [roulette, radio]


def next_after(profile):
    return ALL[(ALL.index(profile) + 1) % len(ALL)]
