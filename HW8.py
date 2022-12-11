import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def get_restaurant_data(db_filename):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT r.name, c.category, b.building, r.rating
        FROM restaurants r
        INNER JOIN categories c ON r.category_id = c.id
        INNER JOIN buildings b ON r.building_id = b.id
    ''')
    data = [{'name': row[0], 'category': row[1], 'building': row[2], 'rating': row[3]} for row in cursor.fetchall()]
    conn.close()
    return data

def barchart_restaurant_categories(db_filename):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.category, COUNT(r.id)
        FROM restaurants r
        INNER JOIN categories c ON r.category_id = c.id
        GROUP BY c.category
    ''')
    data = {row[0]: row[1] for row in cursor.fetchall()}
    sorted_data = sorted(data.items(), key=lambda item: item[1], reverse=False)
    conn.close()
    plt.barh(*zip(*sorted_data))
    plt.xlabel('Count')
    plt.ylabel('Category')
    plt.title('Number of Restaurants by Category')
    plt.show()
    return data

def highest_rated_category(db_filename):
    data = get_restaurant_data(db_filename)
    category_ratings = {}
    for restaurant in data:
        if restaurant['category'] not in category_ratings:
            category_ratings[restaurant['category']] = []
        category_ratings[restaurant['category']].append(restaurant['rating'])
    for category, ratings in category_ratings.items():
        category_ratings[category] = sum(ratings) / len(ratings)
    highest_rated_category = None
    highest_rating = 0
    for category, rating in category_ratings.items():
        if rating > highest_rating:
            highest_rated_category = category
            highest_rating = rating
    sorted_data = sorted([(category, round(rating, 1)) for category, rating in category_ratings.items()], key=lambda item: item[1], reverse=False)
    plt.barh(*zip(*sorted_data))
    plt.xlabel('Average Rating')
    plt.ylabel('Category')
    plt.title('Average Rating by Category')
    plt.show()
    return highest_rated_category, highest_rating

def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'name': 'M-36 Coffee Roasters Cafe',
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.best_category = ('Deli', 4.6)

    def test_get_restaurant_data(self):
        rest_data = get_restaurant_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, list)
        self.assertEqual(rest_data[0], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_barchart_restaurant_categories(self):
        cat_data = barchart_restaurant_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_highest_rated_category(self):
        best_category = highest_rated_category('South_U_Restaurants.db')
        self.assertIsInstance(best_category, tuple)
        self.assertEqual(best_category, self.best_category)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
