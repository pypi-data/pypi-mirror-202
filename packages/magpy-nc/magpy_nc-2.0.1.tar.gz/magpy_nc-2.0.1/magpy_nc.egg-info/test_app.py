import unittest
import json
from app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_create_project(self):
        response = self.app.post('/api/projects', data=json.dumps({
            'name': 'titan',
            'packages': [
                {'name': 'Django'},
                {'name': 'graphene', 'version': '2.0'}
            ]
        }), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['name'], 'titan')
        self.assertEqual(len(data['packages']), 2)
        self.assertEqual(data['packages'][0]['name'], 'Django')
        self.assertTrue('version' in data['packages'][0])
        self.assertEqual(data['packages'][1]['name'], 'graphene')
        self.assertEqual(data['packages'][1]['version'], '2.0')

    def test_create_project_invalid_package(self):
        response = self.app.post('/api/projects', data=json.dumps({
            'name': 'titan',
            'packages': [
                {'name': 'pypypypypypypypypypypy'},
                {'name': 'graphene', 'version': '1900'}
            ]
        }), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], "One or more packages doesn't exist")

    def test_get_project(self):
        response = self.app.get('/api/projects/titan')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'titan')
        self.assertEqual(len(data['packages']), 2)

    def test_delete_project(self):
        response = self.app.delete('/api/projects/titan')
        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()
