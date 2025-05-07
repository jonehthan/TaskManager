import unittest
from src.database.db_manager import DatabaseManager
from src.database.db_config import init_db
from datetime import date

class DatabaseTest(unittest.TestCase):


    def setUp(self):
        init_db()
        self.db = DatabaseManager()
        self.db.delete_all_users()
        self.db.delete_all_tasks()
        self.today = date.today()
        self.user = self.db.add_user("Eric", "Jonathan")
        self.task = self.db.add_task(self.user.id, "Finish homework", self.today, "General", "HIGH", "Pending" )


    def test_create_user(self):
        self.user = self.db.add_user("yoyo", "hi123")
        self.assertEqual(self.user.username, "yoyo")
        self.assertEqual(self.user.password, "hi123")
        self.assertEqual(self.db.get_user_by_username("yoyo"), self.user)
        self.assertEqual(self.db.get_user_by_id(self.user.id), self.user)

    def test_delete_user(self):
        self.db.delete_user(self.user.id)
        self.assertNotEqual(self.db.get_user_by_username("Eric"), self.user)

    def test_create_task(self):
        self.assertEqual(self.db.get_task_by_id(self.user.id), self.task)
        self.assertEqual(self.db.get_task_by_id(self.user.id).description, "Finish homework")

    def test_update_task(self):
        self.db.update_task(self.task.id, "Do dishes", self.today, "General", "LOW", "Completed")
        self.assertEqual(self.db.get_task_by_id(self.user.id).description, "Do dishes")
        self.assertEqual(self.db.get_task_by_id(self.user.id).priority, "LOW")
        self.assertEqual(self.db.get_task_by_id(self.user.id).status, "Completed")
        self.assertNotEqual(self.db.get_task_by_id(self.user.id).status, "Pending")

    def test_delete_task(self):
        task_id = self.task.id
        self.db.delete_task(self.task.id)
        self.assertEqual(self.db.get_tasks_by_user_id(self.user.id), [])
        self.assertEqual(self.db.get_task_by_id(task_id), None)

    def test_user_tasks(self):
        self.db.add_task(self.user.id, "Do dishes", self.today, "General", "LOW", "Completed")
        self.assertEqual(len(self.db.get_tasks_by_user_id(self.user.id)), 2)