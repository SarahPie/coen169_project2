import csv
   
class User:
    def calc_avg(self, ratings):
        if len(ratings) > 0:
            if self.needed_rating != 0:
                return float(sum(ratings) + self.needed_rating) / float(len(ratings) + 1)
            else:
                return float(sum(ratings)) / float(len(ratings))
        else:
            if self.needed_rating != 0:
                return self.needed_rating
            else:
                return 0

    def calc_std_dev(self, ratings):
        variance = map(lambda x: (x - self.average)**2, ratings)
        avg_variance = (float(sum(variance)) / len(variance))
        return math.sqrt(avg_variance)

    def set_similarity(self, similarity):
        self.similarity = similarity

    def __init__(self, similarity, corated_movie_ratings, needed_rating):
        self.similarity = similarity
        self.corated_movie_ratings = corated_movie_ratings
        self.needed_rating = needed_rating
        self.average = self.calc_avg(corated_movie_ratings)
        self.std_dev = self.calc_std_dev(corated_movie_ratings)

class Movie:
    def calc_avg(self, ratings):
        if len(ratings) > 0:
            if self.needed_rating != 0:
                return float(sum(ratings) + self.needed_rating) / float(len(ratings) + 1)
            else:
                return float(sum(ratings)) / float(len(ratings))
        else:
            if self.needed_rating != 0:
                return self.needed_rating
            else:
                return 0

    def __init__(self, m_id, sim, u_r, new_r):
        self.m_id = m_id
        self.similarity = sim
        self.ratings = u_r
        self.needed_rating = new_r
        self.average = self.calc_avg(self.ratings)

    def set_similarity(self, similarity):
        self.similarity = similarity

    def append_rating(self, new_rating):
        self.ratings.append(new_rating)

    def recalc(self):
        self.average = self.calc_avg(self.ratings)

class Methods:
    cosine_similarity, pearson, p_iuf, p_case_mod, item_based_c, custom = range 6
 
def clear():
    print("\n" * 180)


def write_file(file_out, data, delim):
    with open(file_out, "wb") as out_file:
        writer = csv.writer(out_file, delimiter=delim)
        for item in data:
            writer.writerow(item)

def int_wrapper(reader):
    for v in reader:
        yield map(int, v)

def reader(file_to_read, delim):
    data = []
    with open(file_to_read, "rU") as in_file:
        reader = csv.reader(in_file, delimiter=delim)
        reader = int_wrapper(reader)
        data = list(reader)
    return data