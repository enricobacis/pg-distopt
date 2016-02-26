def cost(plan, config, rootserver):
    if not plan.children:     # leaf
        visible = set(rootserver['plain'])
        require = set(rc.text.split('.')[1] for rc in plan['Output'].getchildren())

        if require <= visible:
            return plan.time * rootserver['costs']['cpu']
        else:
            return float('+inf')
    return plan.time * rootserver['costs']['cpu'] + sum(
            best(subplan, config) for subplan in plan.children)

def best(plan, config):
    return min(cost(plan, config, rootserver) for rootserver in config.nodes)
