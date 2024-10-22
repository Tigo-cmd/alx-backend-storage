#!/usr/bin/env python3
""" this module implements mongobd searching"""


def schools_by_topic(mongo_collection, topic):
    '''
    a Python function that returns the list of school having a specific topic:

    mongo_collection: the pymongo collection object
    topic (string): will be topic searched

    '''
    topic_selector= {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
            },
        },
    }
    return [item for item in mongo_collection.find(topic_selector)]