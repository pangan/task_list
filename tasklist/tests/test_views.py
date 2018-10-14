from datetime import datetime
import pytz

from django.contrib.auth.models import User
from django.test import TestCase
from django.test import mock
from django.utils import timezone

from tasklist.views import _get_categorised_tasks
from tasklist.models import Tasks


class TaskListViewsTestCase(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])

    def _get_actual_tasks(self):
        actual_tasks = []
        for task in Tasks.objects.all():
            actual_tasks.append((task.id, task.assignee))
        return actual_tasks

    def test_if_get_categorised_tasks_works_correctly(self):
        task_object = type('task_object', (object,), {})

        todo_1 = task_object()
        todo_2 = task_object()
        doing_1 = task_object()
        done_1 = task_object()

        todo_1.status = 0
        todo_2.status = 0
        doing_1.status = 1
        done_1.status = 2
        sample_task_data = [todo_1, done_1, doing_1, todo_2]
        expected_todo_tasks = [todo_1, todo_2]
        expected_doing_tasks = [doing_1]
        expected_done_tasks = [done_1]

        todo_tasks, doing_tasks, done_tasks = _get_categorised_tasks(sample_task_data)

        self.assertEqual(expected_todo_tasks, todo_tasks)
        self.assertEqual(expected_doing_tasks, doing_tasks)
        self.assertEqual(expected_done_tasks, done_tasks)

    def test_filter_cookie_setting_works_correctly(self):
        response = self.client.get('/?f=1')
        cookies =response.client.cookies
        self.assertEqual(cookies['tasklist_filter'].value, 'True')
        response = self.client.get('/?f=0')
        cookies = response.client.cookies
        self.assertEqual(cookies['tasklist_filter'].value, 'False')

    def test_if_move_task_changes_status(self):

        sample_tests_list = [(0, 1, 1), (1, 1, 2), (2, 1, 2), (0, 0, 0), (1, 0, 0), (2, 0, 1)]
        for status, move, expected_status in sample_tests_list:
            task_object = Tasks(id=1, assignee='testuser',
                                status=status,
                                created=timezone.now())
            task_object.save()
            self.client.get('/tasklist/move/?id=1&status={}&move={}'.format(status, move))
            actual_task = Tasks.objects.get(id=1)
            self.assertEqual(actual_task.status, expected_status)

    def test_if_move_task_not_change_other_assignees_tasks(self):
        task_object = Tasks(id=1, assignee='admin', status=0, created=timezone.now())
        task_object.save()
        self.client.get('/tasklist/move/?id=1&status=0&move=1')
        actual_task = Tasks.objects.get(id=1)
        self.assertEqual(actual_task.status, 0)

    def test_if_move_task_updates_time_stamps(self):
        task_object = Tasks(id=1, assignee='testuser', status=0, created=timezone.now())
        task_object.save()
        with mock.patch('tasklist.views.timezone') as mocked_timezone:
            mocked_timezone.now.return_value = timezone.datetime(2018, 11, 11, 12, 12, 13,
                                                                 tzinfo=pytz.UTC)
            self.client.get('/tasklist/move/?id=1&status=0&move=1')
            actual_task = Tasks.objects.get(id=1)
            self.assertEqual(actual_task.started, datetime(2018, 11, 11, 12, 12, 13,
                                                           tzinfo=pytz.UTC))
            self.client.get('/tasklist/move/?id=1&status=1&move=1')
            actual_task = Tasks.objects.get(id=1)
            self.assertEqual(actual_task.completed, datetime(2018, 11, 11, 12, 12, 13,
                                                           tzinfo=pytz.UTC))

        self.client.get('/tasklist/move/?id=1&status=2&move=0')
        actual_task = Tasks.objects.get(id=1)
        self.assertEqual(actual_task.completed, None)
        self.client.get('/tasklist/move/?id=1&status=1&move=0')
        actual_task = Tasks.objects.get(id=1)
        self.assertEqual(actual_task.started, None)

    def test_if_delete_task_works_correctly(self):
        sample_tasks = [(1, 'admin'), (2, 'testuser'), (3, 'testuser')]
        for task_id, assignee in sample_tasks:
            task_object = Tasks(id=task_id, assignee=assignee)
            task_object.save()

        expected_tasks_list = [(1, sample_tasks),
                               (2, [(1, 'admin'), (3, 'testuser')]),
                               (3, [(1, 'admin')])]
        for id, expected_tasks in expected_tasks_list:
            self.client.get('/tasklist/delete/?id={}'.format(id))
            self.assertListEqual(expected_tasks, self._get_actual_tasks())

