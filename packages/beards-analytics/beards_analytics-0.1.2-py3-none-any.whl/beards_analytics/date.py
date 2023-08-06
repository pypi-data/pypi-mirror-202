from datetime import date, timedelta


def daterange(start_date: date, end_date: date, delta_days: int = 1):
    if start_date >= end_date:
        raise ValueError('end_date must be after start_date')
    
    if int(delta_days) < 1:
        raise ValueError('delta_days must be an integer >= 1')
    
    tmp = start_date
    last_yield = tmp

    while tmp <= end_date:
        last_yield = tmp
        yield tmp
        tmp += timedelta(int(delta_days))

    if last_yield != end_date:
        yield end_date

def datepairs(start_date: date, end_date: date, delta_days: int = 1, intersect: bool = False):
    dates = [d for d in daterange(start_date, end_date, delta_days)]
    has_prev = False
    
    for i in range(0, len(dates) - 1):
        yield dates[i] + timedelta(int(has_prev and not intersect)), dates[i+1]
        has_prev = True
