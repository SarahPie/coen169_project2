import rec

def p_sim(current_u=None, test_user=None):
    num = 0.0
    a = 0.0
    b = 0.0
    for i in range(len(current_u.co_m_r)):
        if current_u.co_m_r[i] != 0 and test_user.co_m_r[i] != 0:
            d1 = (current_u.co_m_r[i] - current_u.average)
            d2 = (test_user.co_m_r[i] - test_user.average)
            num += (float(d1) * float(d2))
            a += float(d1 * d1)
            b += float(d2 * d2)

    denom = (math.sqrt(a) * math.sqrt(b))

    if denom == 0:
        return 0

    return float(num) / float(denom)


def pearson(user_id=None, movie_id=None):
    sim = 30
    rating = 0
    rel_users = []
    current_u_r = []
    current_u_r_m = []

    rated_m = 0
    current_u_avg = 0.0
    for recs in RATINGS:
        # [U, M, R] -> [0, 1, 2]
        if recs[0] == user_id and recs[2] != 0 and rated_m < HIGH:
            current_u_avg += recs[2]
            current_u_r.append(recs[2])
            rated_m += 1
            current_u_r_m.append(recs[1])
    current_u_avg = float(current_u_avg)/float(rated_m)
    current_u = User(0, current_u_r, 0)

    for i, user in enumerate(TRAINER):
        sim_user_ratings = []

        for movie in current_u_r_m:
            sim_user_ratings.append(TRAINER[i][movie - 1])

        needed_rating = TRAINER[i][movie_id - 1]
        sim_user = User(0, sim_user_ratings, needed_rating)

        w_a_u = p_sim(current_u, sim_user)
        sim_user.set_similarity(w_a_u)
        if len(rel_users) < sim:
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
