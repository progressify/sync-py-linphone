
class DatabaseException(Exception):
    exit_code = 2
    message = "I can't find your Linphone installation.\n"\
              "Insert manually your installation path with `--db_path` flag.\n"\
              "Bye.\n"
