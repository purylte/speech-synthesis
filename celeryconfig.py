result_backend = 'redis://localhost:6379'
broker_url = 'amqp://guest:guest@localhost:5672//'
task_ignore_result = False
task_track_started = True
imports = ['worker']
