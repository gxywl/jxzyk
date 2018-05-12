# _*_ encoding: utf-8 _*_

'''
pip freeze > requirements.txt

'''

from fabric.api import local, env, run ,sudo ,cd

env.hosts=['deploy@192.168.1.9']
env.password='pub'

def test():
    local('python -m unittest discover')

def upgrade_libs():
    sudo("apt update")
    sudo("apt upgrade")

def setup():
    #test()
    #upgrade_libs()


    # sudo('apt install -y nginx')
    # sudo("apt install -y git")

    # sudo("apt install -y python")

    # sudo("apt install -y build-essential")
    # sudo("apt install -y python-dev")
    # sudo("apt install -y python-pip")
    #
    #
    #
    #
     # sudo("pip install virtualenv")
    # sudo("apt install -y supervisor")

    #
    #
    # sudo("useradd -d /home/deploy/ deploy")
    # sudo("gpasswd -a deploy sudo")
    #
    # #sudo("chown -R deploy /usr/local/")
    # #sudo("chown -R deploy /usr/lib/pthon2.7")
    #
    # run("git config --global credential.helper store")

    with cd("/home/deploy/websites/"):
        sudo("git clone https://github.com/gxywl/jxzyk.git")

    with cd("/home/deploy/websites/jxzyk"):
        # sudo("virtualenv venv")
        # sudo("source venv/bin/active")
        sudo("virtualenv /home/deploy/websites/jxzyk/venv")
        sudo(". /home/deploy/websites/jxzyk/venv/bin/activate")
        '''
        #sudo('nano /home/deploy/websites/jxzyk/venv/lib/python2.7/site.py')
        # _*_ encoding: utf-8 _*_
        # encoding = "ascii" ==> "utf8"
        '''


        # run("/home/deploy/jxzyk/venv/bin/pip install -r requirements.txt")
        sudo("/home/deploy/websites/jxzyk/venv/bin/pip install -r /home/deploy/websites/jxzyk/requirements.txt -i https://pypi.douban.com/simple")  #及uwsgi

    #     run("python manage.py createdb")
        sudo("/home/deploy/websites/jxzyk/venv/bin/python manage.py db upgrade")

        sudo("/home/deploy/websites/jxzyk/venv/bin/pip  install  uwsgi")
        sudo("/home/deploy/websites/jxzyk/venv/bin/uwsgi --ini /home/deploy/websites/jxzyk/uwsgi.ini")

        sudo ("cp superivsord.conf /etc/supervisor/conf.d/jxzyk.conf")

        sudo("cp nginx.conf /etc/nginx/sites-available/jx.conf")
        sudo("ln -s /etc/nginx/sites-available/j.conf /etc/nginx/sites-enabled/jx.conf ")

    sudo('chown -R www-data:www-data /home/deploy/websites/jxzyk')
    sudo('chmod -R 755 /home/deploy/websites/jxzyk')

    sudo(('service supervisor restart'))
    sudo(('service nginx restart'))

def deploy():
    # test()
    # upgrade_libs()

    with cd('/home/deploy/websites/jxzyk'):
        sudo("git pull")
        sudo("/home/deploy/websites/jxzyk/venv/bipip install -r requirements.txt")
        sudo("/home/deploy/websites/jxzyk/venv/bipython manage.py db upgrade")