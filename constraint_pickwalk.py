from pymel import all as pm

def constraint_pick_walking(pick_direction):
    """
    With an object selected and "up":
        if is a constrained (Driven) node, it will select the Constraint node.
        if is a Constraint node, it will select the Driver node.
        if is a Driver node, it will do nothing.
    With an object selected and "down":
        if is a constrained (Driven) node, it will do nothing.
        if is a Constraint node, it will select the constrained (Driven) node.
        if is a Driver node, it will select the Constraint node.
    :arg pick_direction str:
        "up" will pick-walk up.
        "down" will pick-walk down.
    """
    items = pm.selected()
    found_parents = []
    # Pick UP
    if pick_direction == 'up':
        for item in items:
            if 'constraint' in item.type().lower():
                for c in set(item.target.listConnections()):
                    if c != item:
                        found_parents += [c]
            else:
                all_constraints = item.parentInverseMatrix.listConnections()
                for constraint in all_constraints:
                    for c in set(constraint.target.listConnections()):
                        if 'constraint' in c.type().lower():
                            found_parents += [c]

    # Pick DOWN
    if pick_direction == 'down':
        for item in items:
            if 'constraint' in item.type().lower():
                for c in set(item.outputs()):
                    if c != item:
                        found_parents += [c]
            else:
                for c in set(item.outputs()):
                    if 'constraint' in c.type().lower():
                        found_parents += [c]
    if found_parents:
        pm.select(found_parents)
        return found_parents
    else:
        pm.warning('No constraints found on selection.')
        pm.select(items)

# constraint_pick_walking('up')
# constraint_pick_walking('down')
