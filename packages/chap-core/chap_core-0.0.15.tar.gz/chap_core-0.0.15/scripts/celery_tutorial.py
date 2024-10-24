from celery import Celery

app = Celery('tasks', broker='redis://localhost')

@app.task
def add(x, y):
    return x + y

#print(add.delay(2, 2))
