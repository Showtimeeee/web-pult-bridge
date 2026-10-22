from profiles import lights, radio, roulette

ALL = [roulette, radio, lights]


def next_after(profile):
    return ALL[(ALL.index(profile) + 1) % len(ALL)]
