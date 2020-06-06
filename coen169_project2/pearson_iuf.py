import rec

def get_r(movie_id, cur_user_rated):

    num_ratings = cur_user_rated
    for user in TRAINER:
        if user[movie_id - 1] != 0:
            num_ratings += 1
    return num_ratings

def get_iuf(movie_id, cur_user_rated):
    m = 201 
    m_j = get_r(movie_id, cur_user_rated)
    if m_j != 0:
        iuf = math.log((float(m)/float(m_j)), 2)
    else:
        iuf = 0
    return iuf

def pearson_iuf_sim(current_u=None, test_user=None):
    num = 0.0
    a = 0.0
    b = 0.0
    for i in range(len(current_u.co_m_r)):
        if current_u.co_m_r[i] != 0 and test_user.co_m_r[i] != 0:
            iuf1 = get_iuf(current_u.co_m_r[i], 1)
            iuf2 = get_iuf(test_user.co_m_r[i], 1)
            d1 = (iuf1 * current_u.co_m_r[i] - current_u.avg)
            d2 = (iuf2 * test_user.co_m_r[i] - test_user.avg)
            num += (float(d1) * float(d2))
            a += float(d1 * d1)
            b += float(d2 * d2)

    denom = (math.sqrt(a) * math.sqrt(b))

    if denom == 0:
        return 0

    return float(num) / float(denom)

def p_iuf(user_id=None, movie_id=None):
    num_similar = 50
    rating = 0
    rel_users = []
    current_u_r = []
    current_u_r_m = []

   
    n_rm = 0
    for recs in RATINGS:
        if recs[0] == user_id and recs[2] != 0 and n_rm < HIGH:
            current_u_r.append(recs[2])
            n_rm += 1
            current_u_r_m.append(recs[1])
    current_u = User(0, current_u_r, 0)

    for i, user in enumerate(TRAINER):
        sim_user_ratings = []

        for movie in current_u_r_m:
            user_rating = TRAINER[i][movie - 1]
            sim_user_ratings.append(user_rating)

        new_r = TRAINER[i][movie_id - 1]
        sim_user = User(0, sim_user_ratings, new_r)

        w_a_u = pearson_iuf_sim(current_u, sim_user)
        sim_user.set_similarity(w_a_u)
        
        if len(rel_users) < num_similar:
            rel_users.append(sim_user)
        else:
            saved_i = -1
            for idx in range(len(rel_users)):
                if sim_user.similarity > rel_users[idx].similarity:
                    saved_i = idx

            if saved_i !=-1:
                rel_users[saved_i] = sim_user

    num = 0.0
    denom = 0.0
    for user in rel_users:
     
        w_a_u = user.similarity
        r_a_i = user.new_r
        num += (float(w_a_u) * float((r_a_i - user.avg)))
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

