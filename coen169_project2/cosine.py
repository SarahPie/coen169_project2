import rec

def calc_cos(user1=None, user2=None):
    dotp = 0.0
    a = 0.0
    b = 0.0
   
    for i in range(len(user2.co_m_r)):
        if user1.co_m_r[i] != 0 and user2.co_m_r[i] != 0:
            d1 = user1.co_m_r[i] - user1.avg
            d2 = user2.co_m_r[i] - user2.avg
            dotp += (d1 * d2)
            a += (d1 * d1)
            b += (d2 * d2)

    a = math.sqrt(float(a))
    b = math.sqrt(float(b))

    if a == 0 or b == 0:
        return 0

    return float(dotp) / float((a * b))

def cosine_similarity(user_id=None, movie_id=None):

    sim = 30
    rating = 0
    rel_users = []
    current_u_r = []
    current_u_r_m = []

    n_r_m = 0
    current_u_avg = 0.0
    for recs in RATINGS:
        if recs[0] == user_id and recs[2] != 0 and n_r_m < HIGH:
            current_u_avg += recs[2]
            current_u_r.append(recs[2])
            n_r_m += 1
            current_u_r_m.append(recs[1])
    current_u_avg = float(current_u_avg)/float(n_r_m)
    current_u = User(0, current_u_r, 0)

    for index, user in enumerate(TRAINER):
        sim_user_ratings = []

        for movie in current_u_r_m:
            sim_user_ratings.append(TRAINER[index][movie - 1])

        needed_rating = TRAINER[index][movie_id - 1]
        sim_user = User(0, sim_user_ratings, needed_rating)

        w_a_u = calc_cos(current_u, sim_user)
        sim_user.set_similarity(w_a_u)

        if len(rel_users) < sim:
            rel_users.append(sim_user)
        else:
            save_i = -1
            for i in range(len(rel_users)):
                if sim_user.similarity > rel_users[i].similarity:
                    save_i = i

            if save_i !=-1:
                rel_users[save_i] = sim_user

    num = 0.0
    denom = 0.0
    for user in rel_users:
        w_a_u = user.similarity
        r_a_i = user.needed_rating
        num += (float(w_a_u) * float(r_a_i))
        denom += abs(float(w_a_u))

    if denom != 0:
        rating = current_u.avg + (float(num)/float(denom))
        rating = round(rating)

    
    if rating == 0:
        rating = round(current_u.avg)

    if rating > 5:
        rating = 5
   
    del rel_users[:]
    del current_u_r[:]
    del current_u_r_m[:]

    return int(rating)

