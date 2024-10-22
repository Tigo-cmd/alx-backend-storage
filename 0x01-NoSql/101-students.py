#!/usr/bin/env python3
""" this module implements mongobd searching"""


def top_students(mongo_collection):
    """
    Python function that returns all students sorted by average score
    """
    student = mongo_collection.aggregate(
        [
            {
                '$project': {
                    '_id': 1,
                    'name': 1,
                    'averageScore': {
                        '$avg': {
                            '$avg': '$topics.score',
                        },
                    },
                    'topics': 1,
                },
            },
            {
                '$sort': {'averageScore': -1},
            },
        ]
    )
    return student