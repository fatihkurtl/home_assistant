from pywebostv.discovery import discover

def discover_tvs():
    print("🔍 Searching for LG WebOS TVs...")
    tvs = []

    for tv in discover(service='webostv', timeout=10):
        tvs.append(tv)
    
    return tvs
