from locust import HttpUser, TaskSet, task, between

"""
Run locus with:
locust -f ./4.TextSimilarity/tests/load_test.py
"""


class TextLocusTasks(TaskSet):
    @task
    def token_test(self):
        self.client.post('/detect', json=dict(username="myuser", password="123f",
                                         text1="This can't be the same sentence",
                                         text2="for this sentence, I Don't use the same sintax"))


class TextLoadTest(HttpUser):
    tasks = [TextLocusTasks]
    host = 'http://127.0.0.1:5000'
    wait_time = between(0.5, 2)
    stop_timeout = 20
