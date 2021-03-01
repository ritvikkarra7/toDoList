import peewee
import datetime
import os
import time

db = peewee.SqliteDatabase('test.db')


class DB(peewee.Model):
    task = peewee.CharField()
    date = peewee.DateField(default=datetime.date.today())
    protected = peewee.BooleanField(default=False)
    complete = peewee.BooleanField(default=False)

    class Meta:
        database = db
        db_table = 'notes'


DB.create_table()

class Commands:

    def __init__(self):
        self.index = 0
        self.mainMenu()

    def clear(self):
        """Clear the display"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def mainMenu(self):
        while True:
            self.clear()
            print('MY TO-DO LIST')
            print('====================================', '\n' * 2)
            print(datetime.datetime.now().strftime('%A, %B %d, %Y'), '\n', '=======================')
            for i in range(len(DB.select())):
                if i == self.index:
                    if DB.select()[i].protected and DB.select()[i].complete:
                        print('>', '{}'.format(DB.select()[i].task), ' <p>', '<Done>')
                    elif DB.select()[i].protected and DB.select()[i].complete == False:
                        print('>', '{}'.format(DB.select()[i].task), '<p>')
                    elif DB.select()[i].protected == False and DB.select()[i].complete:
                        print('>', '{}'.format(DB.select()[i].task), '<Done>')
                    else:
                        print('>', '{}'.format(DB.select()[i].task))
                else:
                    if DB.select()[i].protected and DB.select()[i].complete:
                        print(' ', '{}'.format(DB.select()[i].task), ' <p>', '<Done>')
                    elif DB.select()[i].protected and DB.select()[i].complete == False:
                        print(' ', '{}'.format(DB.select()[i].task), '<p>')
                    elif DB.select()[i].protected == False and DB.select()[i].complete:
                        print(' ', '{}'.format(DB.select()[i].task), '<Done>')
                    else:
                        print(' ', '{}'.format(DB.select()[i].task))

            print('\n')
            print('Previous/Next: p/n\n')
            print('a) Add a new task \n',
                  'm) Modify selected entry \n',
                  'c) Cleanup: delete completed, non-protected entries older than a week \n',
                  'q) Quit')
            print('\n')

            command = input('Action: ')
            if command == 'a':
                self.add()
            elif command == 'm':
                self.subMenu(DB.select()[self.index])
            elif command == 'c':
                self.cleanup()
            elif command == 'q':
                self.quit()
            elif command == 'n':
                self.next()
            elif command == 'p':
                self.prev()
            else:
                print('Please enter a valid command!')
                time.sleep(1)

    def subMenu(self, entry):
        while True:
            self.clear()
            print(datetime.datetime.now().strftime('%A, %B %d, %Y'), '\n', '===============')
            print('>', entry.task)
            print('\n' * 2)
            print('m) Modify task \n',
                  'd) Toggle \'DONE\' \n',
                  'p) Toggle \'protected\' \n',
                  'e) Erase entry \n',
                  'q) Back to main menu')

            command = input('Action: ')
            if command.strip() == 'm':
                self.modify(entry)
            elif command.strip() == 'd':
                self.done(entry)
            elif command.strip() == 'p':
                self.protect(entry)
            elif command.strip() == 'e':
                self.erase(entry)
            elif command.strip() == 'q':
                self.mainMenu()
            else:
                'Please enter a valid command!'
                time.sleep(1)

    def add(self):

        action = input("To do: ")
        while True:
            protect = input('Protect this task? [y/N]')
            if protect.strip().upper() == 'Y':
                DB.create(task=action, protected=True).save()
                break
            elif protect.strip().upper() == 'N':
                DB.create(task=action).save()
                break
            else:
                print('Please enter a valid command [y/N]')

    def protect(self, task):

        if task.protected == False:
            DB.update(protected=True).where(DB.id == task.id).execute()
            print("Task protected!")
        else:
            DB.update(protected=False).where(DB.id == task.id).execute()
            print("Task unprotected!")

        time.sleep(1)

    def modify(self, task):

        new = input('Enter new updated task: ')
        if input('Confirm update? [y/N]').strip().upper() == 'Y':
            DB.update(task=new).where(DB.id == task.id).execute()

    def done(self, task):
        if task.complete == False:
            DB.update(complete=True).where(DB.id == task.id).execute()
            print("Task completed!")
        else:
            DB.update(complete=False).where(DB.id == task.id).execute()
            print("Task marked as incomplete!")
        time.sleep(1)

    def erase(self, task):
        confirm = input("Are you sure you want to delete this task? [y/N]")
        if confirm.strip().upper() == 'Y':
            DB.delete().where(DB.id == task.id).execute()
        self.index = 0

    def cleanup(self):
        DB.delete().where((DB.protected == False) &
                          (DB.complete == True) &
                          (datetime.datetime.utcnow() - DB.date) > 7).execute()
        print("Cleanup complete!")
        time.sleep(1)

    def quit(self):
        exit()

    def next(self):
        if self.index < len(DB.select()) - 1:
            self.index += 1

    def prev(self):
        if self.index > 0:
            self.index -= 1


if __name__ == '__main__':
    comm = Commands()
