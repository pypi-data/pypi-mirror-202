def qcreate(db_name):
  return "Create database {}".format(db_name)
def qread(table_name,filed_name="*"):
  return "Select {} from {}".format(table_name,filed_name)
