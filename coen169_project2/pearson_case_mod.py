import rec

def p_case_mod(user_id=None, movie_id=None):
    x = 3.5
    sims = 30
    rating = 0
    rel_users = []
    current_u_r = []
    current_u_r_m = []

    n_r_m = 0
    for recs in RATINGS:
        if recs[0] == user_id and recs[2] != 0 and n_r_m < HIGH:
            current_u_r.append(recs[2])
            n_r_m += 1
            current_u_r_m.append(recs[1])
    current_u = User(0, current_u_r, 0)

    for index, user in enumerate(TRAINER):
        sim_user_ratings = []
        for movie in current_u_r_m:
            sim_user_ratings.append(TRAINER[index][movie - 1])
        needed_rating = TRAINER[index][movie_id - 1]
        sim_user = User(0, sim_user_ratings, needed_rating)
        w_a_u = pearson_sim(current_u, sim_user)
        w_mod = w_a_u * math.pow(abs(w_a_u), x - 1)
        sim_user.set_similarity(w_mod)
        if len(rel_users) < sims:
            rel_users.append(sim_user)
        else:
            saved_index = -1
            for idx in range(len(rel_users)):
                if sim_user.similarity > rel_users[idx].similarity:
                    saved_index = idx

            if saved_index !=-1:
                rel_users[saved_index] = sim_user

    num = 0.0
    denom = 0.0
    for user in rel_users:
        w_a_u = user.similarity
        r_a_i = user.needed_rating
        num += (float(w_a_u) * float(r_a_i - user.average))
        denom += abs(float(w_a_u))

    if denom != 0:
        rating = current_u.average + (float(num)/float(denom))
        rating = round(rating)
    
    if rating == 0:
        rating = round(current_u.average)

    if rating > 5: 
        rating = 5

    del rel_users[:]
    del current_u_r[:]
    del current_u_r_m[:]

    return int(rating)

