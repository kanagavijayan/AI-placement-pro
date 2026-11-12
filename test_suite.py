import unittest
import json
import os
from app import app
from database import init_db, get_db

class TestAIPlacementPro(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        cls.client = app.test_client()

    def test_01_auth_flow(self):
        # 1. Login with seeded demo user
        res = self.client.post('/api/login', json={'username': 'demo', 'password': 'demo123'})
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 'success')

        # 2. Verify current user profile
        res_me = self.client.get('/api/me')
        self.assertEqual(res_me.status_code, 200)
        user_data = res_me.get_json()['user']
        self.assertEqual(user_data['username'], 'demo')

    def test_02_dashboard_metrics(self):
        # Must return real database stats
        res = self.client.get('/api/dashboard')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('metrics', data)
        self.assertIn('weekly_chart', data)
        self.assertIn('recent_activities', data)
        self.assertGreater(data['metrics']['overall_readiness'], 0)
        self.assertGreater(data['metrics']['total_learning_hours'], 0)

    def test_03_four_ai_agents(self):
        agents = ['aptitude', 'coding', 'technical', 'hr']
        sample_queries = {
            'aptitude': 'Give me a practice problem on Time and Work.',
            'coding': 'How do I reverse a singly linked list?',
            'technical': 'What are ACID properties in database management?',
            'hr': 'How should I answer: Tell me about yourself?'
        }
        for agent in agents:
            res = self.client.post('/api/agent/chat', json={
                'agent_type': agent,
                'message': sample_queries[agent]
            })
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertEqual(data['status'], 'success')
            self.assertIn('reply', data)
            self.assertTrue(len(data['reply']) > 20)

    def test_04_track_me_system(self):
        # 1. Save a study session (simulate timer stop & save)
        res_session = self.client.post('/api/track/save', json={
            'subject': 'Operating Systems',
            'duration_seconds': 1800, # 30 mins
            'notes': 'Reviewed virtual memory and page replacement algorithms'
        })
        self.assertEqual(res_session.status_code, 200)
        data_session = res_session.get_json()
        self.assertEqual(data_session['status'], 'success')

        # 2. Add Progress manually
        res_prog = self.client.post('/api/track/progress', json={
            'subject': 'Data Structures',
            'topic': 'Segment Trees & Fenwick Trees',
            'difficulty': 'Hard',
            'questions_solved': 4,
            'notes': 'Implemented point updates and range query algorithms'
        })
        self.assertEqual(res_prog.status_code, 200)

        # 3. Verify stats
        res_stats = self.client.get('/api/track/stats')
        self.assertEqual(res_stats.status_code, 200)
        data_stats = res_stats.get_json()
        self.assertGreater(data_stats['total_study_minutes'], 0)
        self.assertGreater(len(data_stats['badges']), 0)

    def test_05_mock_test_system(self):
        # 1. Get test questions
        res_q = self.client.get('/api/mocktests/questions?type=aptitude&count=4')
        self.assertEqual(res_q.status_code, 200)
        questions = res_q.get_json()['questions']
        self.assertTrue(len(questions) > 0)

        # 2. Submit test answers
        answers = {questions[0]['id']: 1}
        res_sub = self.client.post('/api/mocktests/submit', json={
            'test_type': 'aptitude',
            'test_title': 'Unit Test Assessment',
            'answers': answers,
            'time_taken_seconds': 120
        })
        self.assertEqual(res_sub.status_code, 200)
        data_sub = res_sub.get_json()
        self.assertEqual(data_sub['status'], 'success')
        self.assertIn('score_pct', data_sub['result'])

    def test_06_company_preparation(self):
        res = self.client.get('/api/companies')
        self.assertEqual(res.status_code, 200)
        companies = res.get_json()['companies']
        self.assertGreaterEqual(len(companies), 9)

        # Verify Amazon details
        res_amazon = self.client.get('/api/companies/amazon')
        self.assertEqual(res_amazon.status_code, 200)
        self.assertEqual(res_amazon.get_json()['company']['name'], 'Amazon')

    def test_07_resume_builder(self):
        # Retrieve resume
        res = self.client.get('/api/resume')
        self.assertEqual(res.status_code, 200)
        resume_data = res.get_json()['resume']
        self.assertIn('full_name', resume_data)

        # AI Bullet optimization
        res_opt = self.client.post('/api/resume/optimize', json={
            'text': 'Built a web dashboard for tracking student study hours'
        })
        self.assertEqual(res_opt.status_code, 200)
        self.assertIn('optimized', res_opt.get_json())

    def test_08_personalized_study_planner(self):
        res = self.client.get('/api/planner/generate')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('plan_markdown', data['plan'])

if __name__ == '__main__':
    unittest.main()
