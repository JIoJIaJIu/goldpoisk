from updater import Database, Updater, Updater, Updater, Updater

if __name__ == "__main__":
    with Database() as db:
        for info in db.get_infos():
            updater = Updater(db, info)
            updater.update_products()
