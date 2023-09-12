from numba import njit
from usecase.dvrp.utils.heuristics.local_search.single_relocate import m1_cost_inter, m1_cost_intra, do_m1_inter, \
    do_m1_intra, m1_lookup_intra_update, m1_lookup_inter_update
from usecase.dvrp.utils.route.repr import trip_lookup


@njit
def descend(trip, n, c, trip_dmd, q, w, lookup):
    # lookup = trip_lookup(trip, n)
    gain = -1

    for i in range(len(trip)):
        if trip[i, 0] == 0:
            for j in range(1, n + 1):
                r1 = lookup[j, 0]
                pos1 = lookup[j, 1]
                r2 = i
                pos2 = -1
                gain = m1_cost_inter(c, r1, r2, pos1, pos2, trip)
                if gain > 0:
                    m1_lookup_inter_update(trip, r1, r2, pos1, pos2, lookup)
                    do_m1_inter(r1, r2, pos1, pos2, trip)
                    return gain
            break

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i != j:
                r1 = lookup[i, 0]
                pos1 = lookup[i, 1]
                r2 = lookup[j, 0]
                pos2 = lookup[j, 1]
                u_dmd = q[i]
                if trip_dmd[r2] + u_dmd > w:
                    continue
                if r1 != r2:  # inter route case
                    gain = m1_cost_inter(c, r1, r2, pos1, pos2, trip)
                    if gain > 0:
                        m1_lookup_inter_update(trip, r1, r2, pos1, pos2, lookup)
                        do_m1_inter(r1, r2, pos1, pos2, trip)
                        trip_dmd[r1] -= u_dmd
                        trip_dmd[r2] += u_dmd
                        return gain
                else:  # intra route case
                    gain = m1_cost_intra(c, r1, pos1, pos2, trip)
                    if gain > 0:
                        m1_lookup_intra_update(trip, r1, pos1, pos2, lookup)
                        do_m1_intra(r1, pos1, pos2, trip)
                        return gain
    return gain
