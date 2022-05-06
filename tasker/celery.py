from celery import Celery

app = Celery('tasker',
             include=['tasker.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600*24,
)

if __name__ == '__main__':
    app.start()
