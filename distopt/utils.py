def get_read_cols(plan):
    try: return [o.text.split('.')[-1] for o in plan['Output'].getchildren()]
    except: return []
