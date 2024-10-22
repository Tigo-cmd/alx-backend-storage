#!/usr/bin/env python3
""" this module implements mongobd searching"""


def list_all(mongo_collection):
  """a Python function that lists all documents in a collection
  """
  return [item for item in mongo_collection.find()]