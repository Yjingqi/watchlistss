import os
import unittest


from blog import db,app
from blog.models import Movie,User


class WatchlistTestCase(unittest.TestCase):
    def setUp(self):
   
        app.config.update(
            TESTING=True, 
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
        )
      
        db.create_all()
      
        user = User(name='Test',username='test')
        user.set_password('123456')
        movie = Movie(title='测试电影名称',year='2020')
        db.session.add_all([user,movie])
        db.session.commit()

        self.client = app.test_client()  
        self.runner = app.test_cli_runner()  


    def tearDown(self):
        db.session.remove()  
        db.drop_all()  


    
    def test_app_exist(self):
        self.assertIsNotNone(app)
    
   
    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])

    
    def test_404_page(self):
        response = self.client.get('/lalala') 
        data = response.get_data(as_text=True) 
        self.assertIn('404 - 页面跑丢了',data)
        self.assertIn('返回首页',data)
        self.assertEqual(response.status_code,404)  
    
    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('Test\'s 博客',data)
        self.assertIn('测试电影名称',data)
        self.assertEqual(response.status_code,200)
    

    def login(self):
        self.client.post('/login',data=dict(
            username = 'test',
            password = '123456'
        ),follow_redirects=True)
    

    def test_delete_item(self):
        self.login()

        response = self.client.post('/movie/delete/1',follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('删除数据成功',data)

    
if __name__ == "__main__":
    unittest.main()