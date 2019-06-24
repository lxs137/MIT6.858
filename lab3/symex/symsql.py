## This module wraps SQLalchemy's methods to be friendly to
## symbolic / concolic execution.

import fuzzy
import sqlalchemy.orm

oldget = sqlalchemy.orm.query.Query.get
def newget(query, primary_key):
  ## Exercise 5: your code here.
  ##z
  ## Find the object with the primary key "primary_key" in SQLalchemy
  ## query object "query", and do so in a symbolic-friendly way.
  ##
  ## Hint: given a SQLalchemy row object r, you can find the name of
  ## its primary key using r.__table__.primary_key.columns.keys()[0]

  rows = sqlalchemy.orm.query.Query.all(query)
  if len(rows) == 0:
  	return None
  key = rows[0].__table__.primary_key.columns.keys()[0]

  for row in rows:
  	if primary_key == vars(row)[key]:
  		return row

  return None

sqlalchemy.orm.query.Query.get = newget
