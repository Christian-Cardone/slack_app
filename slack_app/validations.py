def validate_time(time: str) -> bool:
    if len(time) == 5:
        return ':' in time[2]
    else:
        return False


def validate_channel(user_channel: str) -> bool:
    if len(user_channel) > 0:
        return ('#' in user_channel[0]) | ('@' in user_channel[0])
    else:
        return False


def validate_days(days: list) -> bool:
    return days.__len__() > 0

