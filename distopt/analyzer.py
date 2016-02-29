from plan import DistPlan

def cost(plan, config, rootserver):
    if not plan.children:     # leaf
        plains = set(rootserver['plain'])
        read = set(o.text.split('.')[-1] for o in plan['Output'].getchildren())
        if not read <= plains:
            return DistPlan(plan, rootserver, float('+inf'))

    dist = DistPlan(plan, rootserver, plan.time * rootserver['costs']['cpu'])
    for subplan in plan.children:
        dist.children.append(best(subplan, config))
    return dist

def best(plan, config):
    return min((cost(plan, config, server) for server in config.nodes),
               key=lambda distplan: distplan.cost())
