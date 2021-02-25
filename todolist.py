import peewee
import datetime

db = peewee.SqliteDatabase('test.db')


class DB(peewee.Model):

    task = peewee.CharField()
    date = peewee.DateField(default=datetime.date.today)
    protected = peewee.BooleanField(default=False)

    class Meta:
        database = db
        db_table = 'notes'


DB.create_table()


class ToDoList:
    def __init__(self):
        print('MY TO-DO LIST')
        print('====================================', '\n' * 2)

        print(datetime.datetime.now().strftime('%A, %B %d, %Y'), '\n', '===============')
        for row in DB.select():
            print('{}'.format(row.task))


class Commands:

    def __init__(self):

        print('Previous/Next: p/n')
        print('a) Add a new task \n',
              'm) Modify selected entry \n',
              'c) Cleanup: delete completed, non-protected entries older than a week \n',
              'q) Quit')
        print('\n')

        self.switchCase()

    def switchCase(self):
        while True:
            command = input('Action: ')
            if command == 'a':
                self.add()
            elif command == 'm':
                self.modify()
            elif command == 'c':
                self.cleanup()
            elif command == 'q':
                self.quit()
            elif command == 'p':
                self.next()
            elif command == 'n':
                self.prev()
            else:
                print('Please enter a valid command from the list above.')

    def add(self):

        action = input("To do: ")
        while True:
            protect = input('Protect this task? [y/N]')
            if protect.strip().upper() == 'Y':
                DB.create(task=action, protect=True).save()
                break
            elif protect.strip().upper() == 'N':
                DB.create(task=action).save()
                break
            else:
                print('Please enter a valid command [y/N]')

    def modify(self):
        pass

    def cleanup(self):
        pass

    def quit(self):
        pass

    def next(self):
        pass

    def prev(self):
        pass


if __name__ == '__main__':
    tasks = ToDoList()
    comm = Commands()

