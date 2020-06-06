import rec

def adjusted_cos(movie1=None, movie2=None, r_u_avgs=None, r_a_avg=None):
    num = 0.0
    a = 0.0
    b = 0.0
    for i in range(len(movie1.ratings)):
        if(movie1.ratings[i]!=0 and movie2.ratings[i]!=0):
            d1 = movie1.ratings[i] - r_a_avg
            d2 = movie2.ratings[i] - r_u_avgs[i]
            num += d1 * d2
            a += d1 * d1
            b += d2 * d2
    a = math.sqrt(a)
    b = math.sqrt(b)

    if a == 0 or b == 0:
        return 0
    return float(num) / float(a * b)

def item_based_c(user_id=None, movie_id=None):

    rating = 0
    current_u_r = []
    current_u_r_m = []
    r_movies = []

    ur_avgs = [0 for x in range(200)]

    nr_m = 0
    for recs in RATINGS:
        if recs[0] == user_id and recs[2] != 0 and nr_m < HIGH:
            current_u_r.append(recs[2])
            nr_m += 1
            current_u_r_m.append(recs[1])
            r_movies.append(Movie(recs[1], 0, [], recs[2]))
    current_u = User(0, current_u_r, 0)

    new_m = Movie(movie_id, 0, [], 0)
    for user in TRAINER:
        for idx, movie in enumerate(r_movies):
            r_movies[idx].append_rating(user[movie.m_id - 1])
        new_m.append_rating(user[movie_id - 1])

   
    new_m.recalc()
    for i in range(len(r_movies)):
        r_movies[i].recalc()

    for i, user in enumerate(TRAINER):
        avg = numpy.average(user)
        ur_avgs[i] = avg

    for i, check_m in enumerate(r_movies):

        w_a_u = adjusted_cos(new_m, check_m, ur_avgs, current_u.average)
        r_movies[i].set_similarity(w_a_u)

    num = 0.0
    denom = 0.0
    for movie in r_movies:
        w_a_u = movie.similarity
        r_a_i = movie.new_r
        num += (float(w_a_u) * float(r_a_i))
        denom += abs(float(w_a_u))

    if denom != 0:
        rating = current_u.average + (float(num)/float(denom))
        rating = round(rating)

    if rating <= 0:
        rating = round(current_u.average)

    if rating > 5: 
        rating = 5

    return int(rating)
