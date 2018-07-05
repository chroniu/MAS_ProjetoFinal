from  database import db


class LogFileControl():

    def __init__(self):

        self.table = 'LogFileControl'


    """
    returns a set of all files
    """
    def get_all_files(self):
        results = []
        for row in db[self.table].find(downloaded=True):
            results.append(row['file_name'])
        return set(results)


    def get_unprocessed_files(self):
        results = []
        for row in db[self.table].find(processed=False):
            results.append(row['file_name'])
        return set(results)

    def insert_file(self, file_dict):
        db[self.table].insert(
            dict(
                file_name=file_dict['name'],
                downloaded=file_dict['downloaded'],
                processed=file_dict['processed'],
                correct=file_dict['correct'],
                coments=file_dict['comments'],
                imported=False))

    def update_file(self, file_dict):
        print("updading key=",file_dict['name'])

        db[self.table].update(
            dict(
                file_name=file_dict['name'],
                downloaded=file_dict['downloaded'],
                processed=file_dict['processed'],
                correct=file_dict['correct'],
                coments=file_dict['comments'],
                imported=False),
            ['file_name'])

    def get_not_imported_files(self):
        results = []
        for row in db[self.table].find(imported=False, correct=True):
            results.append(row['file_name'])
        return set(results)

    def check_as_imported(self, file_name):
         db[self.table].update(dict(file_name=file_name, imported=True), ['file_name'])



log_control = LogFileControl()
