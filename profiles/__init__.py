from profiles import radio, roulette

ALL = [roulette, radio]


def next_after(profile):
    return ALL[(ALL.index(profile) + 1) % len(ALL)]


def by_name(name):
    for profile in ALL:
        if profile.NAME == name:
            return profile
    return None
