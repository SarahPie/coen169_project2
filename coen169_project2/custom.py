def custom(user_id=None, movie_id=None):
    cos_sim_rating = cosine_similarity(user_id, movie_id)
    cos_item_rating = item_based_c(user_id, movie_id)
    rating = round((cos_item_rating + cos_sim_rating) / 2.0)
    return int(rating)
