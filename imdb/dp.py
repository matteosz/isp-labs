# dp.py

import csv
import attr
import numpy as np

class BudgetDepletedError(Exception):
    pass

@attr.s
class Rating:
    """Movie rating."""
    user = attr.ib()
    movie = attr.ib()
    date = attr.ib()
    stars = attr.ib()

class DpQuerySession:
    """
    Respond to database queries with differential privacy.

    Args:
        db (str): Path to the ratings database csv-file.
        privacy_budget (float): Total differential privacy epsilon for the session.
    """

    def __init__(self, db, privacy_budget):
        self.db = db
        self.privacy_budget = privacy_budget
        self.old_queries = {}
        self._load_db()

    def _load_db(self):
        """Load the rating database from a csv-file."""
        self._entries = []
        with open(self.db) as f:
            reader = csv.reader(f, quotechar='"', delimiter=",")
            for email, movie, date, stars in reader:
                self._entries.append(
                    Rating(user=email, movie=movie, date=date, stars=int(stars))
                )

    @property
    def remaining_budget(self):
        """
        Calculate the remaining privacy budget.

        Returns:
            float: The remaining privacy budget.
        """
        return self.privacy_budget

    def get_count(self, movie_name, rating_threshold, epsilon):
        """
        Get the number of ratings where a given movie is rated at least as high as the threshold.

        Args:
            movie_name (str): Movie name.
            rating_threshold (int): Rating threshold (number between 1 and 5).
            epsilon: Differential privacy epsilon to use for this query.

        Returns:
            float: The count with differentially private noise added.

        Raises:
            BudgetDepletedError: When query would exceed the total privacy budget.
        """
        # WARNING: Do not convert the response to positive integers. Leave as a
        # possibly negative float. This is a requirement for our verification.
        if self.old_queries.get(movie_name) is not None:
            if self.old_queries[movie_name].get(rating_threshold) is not None:
                return self.old_queries[movie_name][rating_threshold]
            else:
                self.old_queries[movie_name] = {}

        
        if epsilon > self.remaining_budget:
            raise BudgetDepletedError
        
        count = 0
        for line in self._entries:
            if line.movie == movie_name and line.stars >= rating_threshold:
                count += 1
        
        ans = np.random.laplace(loc=0, scale=1. / epsilon)
        self.old_queries[movie_name][rating_threshold] = ans
        self.privacy_budget -= epsilon

        return ans