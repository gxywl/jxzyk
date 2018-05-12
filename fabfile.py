from fabric.api import local, env, run ,sudo ,cd

env.hosts=['ubuntu@192.168.1.14']

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

    with cd("/home/deploy/"):
        run("git clone https://github.com/gxywl/jxzyk.git")

    with cd("/home/deploy/jxzyk"):
        sudo("virtualenv venv")
        sudo("source venv/bin/active")


        run("/home/deploy/jxzyk/venv/bin/pip install -r requirements.txt")
    #     run("python manage.py createdb")
        run("/home/deploy/jxzyk/venv/bin/python manage.py db upgrade")

        sudo("/home/deploy/jxzyk/venv/bin/pip  install  uwsgi")
        sudo("/home/deploy/jxzyk/venv/bin/uwsgi --ini /home/deploy/jxzyk/uwsgi.ini")

        sudo ("cp superivsord.conf /etc/supervisor/conf.d/jxzyk.conf")

        sudo("cp nginx.conf /etc/nginx/sites-available/j.conf")
        sudo("ln -s /etc/nginx/sites-available/j.conf /etc/nginx/sites-enabled/j.conf ")


    sudo(('service supervisor restart'))
    sudo(('service nginx restart'))

def deploy():
    # test()
    # upgrade_libs()

    with cd('/home/deploy/jxzyk'):
        run("git pull")
        run("pip install -r requirements.txt")
        run("python manage.py db upgrade")