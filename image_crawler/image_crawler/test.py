from scheduler import tasks

r = tasks.add.delay(1, 1)

print r.get()