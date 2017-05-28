def td_format(delta_time):
    if delta_time is None:
        return "-"

    seconds = int(delta_time.total_seconds())
    periods = [
        ('year', 60 * 60 * 24 * 365),
        ('month', 60 * 60 * 24 * 30),
        ('day', 60 * 60 * 24),
        ('hour', 60 * 60),
        ('minute', 60),
        ('second', 1)
    ]

    strings = []
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            if period_value == 1:
                strings.append("%s %s" % (period_value, period_name))
            else:
                strings.append("%s %ss" % (period_value, period_name))

    return ", ".join(strings)


def td_format_short(delta_time):
    if delta_time is None:
        return "-"

    seconds = int(delta_time.total_seconds())
    periods = [
        ('_', 60 * 60 * 24),
        (':', 60 * 60),
        (':', 60),
        ('', 1)
    ]

    string = ""
    for separator, period_seconds in periods:
        if string or seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            string += str(period_value) + separator

    return string


def td_format_shortest(delta_time):
    if not delta_time or delta_time.total_seconds() < 0:
        return "-"

    seconds = int(delta_time.total_seconds())

    periods = [
        ('d', 60 * 60 * 24),
        ('h', 60 * 60),
        ('m', 60),
        ('s', 1)
    ]

    for unit, period_seconds in periods:
        if seconds >= period_seconds:
            return str(divmod(seconds, period_seconds)[0]) + unit

    return "0s"
