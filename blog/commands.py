from blog.models import User,Ariticles
import click 
from blog import db,app

@app.cli.command()
def forge():
    db.create_all()
    name = "Bruce"
    movies = [
        {'title':'湖南农业大学','author':'Yyjingqi','content':'博文内容'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        Ariticle = Ariticles(title=m['title'],author=m['author'],content=m['content'])
        db.session.add(Ariticle
        )
    db.session.commit()
    click.echo('数据导入完成')

@app.cli.command()
@click.option('--drop',is_flag=True,help='删除之后再创建')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('初始化数据库')



@app.cli.command()
@click.option('--username',prompt=True,help="用来登录的用户名")
@click.option('--password',prompt=True,hide_input=True,confirmation_prompt=True,help="用来登录的密码")
def admin(username,password):
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('更新用户')
        user.username = username
        user.set_password(password)
    else:
        click.echo('创建用户')
        user = User(username=username,name="wj")
        user.set_password(password)
        db.session.add(user)
    
    db.session.commit()
    click.echo('创建管理员账号完成')



