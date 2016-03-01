from utils import get_read_cols
from plan import DistPlan

def cost(plan, config, rootserver):
    if not plan.children:   # leaf
        if not set(get_read_cols(plan)) <= set(rootserver['plain']):
            return DistPlan(plan, rootserver, float('+inf'))

    seconds = plan.time / 1000.0
    dist = DistPlan(plan, rootserver, seconds * rootserver['costs']['cpu'])

    for subplan in plan.children:
        dist.children.append(best(subplan, config))
    return dist

def best(plan, config):
    if plan.best is None:
        plan.best = min((cost(plan, config, server) for server in config.nodes),
                        key=lambda distplan: distplan.cost())
    return plan.best
