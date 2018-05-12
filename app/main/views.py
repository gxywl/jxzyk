# _*_ encoding: utf-8 _*_
import hashlib
import os
import time
import datetime

from flask import redirect, url_for, render_template, flash, send_from_directory, request, abort
from flask_login import current_user, login_required
from sqlalchemy import func, engine

from app.models import User, Zytype, Jxsource
from .. import db
from .forms import NameForm
from . import main


# @main.route('/download/<filename>', methods=['GET'])
# @login_required
# def download(filename):
#     if request.method == "GET":
#         # if os.path.isfile(os.path.join('upload', filename)):
#         return send_from_directory('upload', filename, as_attachment=True)
#         # abort(404)


@main.route('/download/<int:zyid>', methods=['GET'])
@login_required
def download(zyid):

    jxsource = Jxsource.query.get_or_404(zyid)
    filename = jxsource.filename

    # 是记录下载次数.. # # jxsource.countd=int(jxsource.countd) + 1
    jxsource.countd += 1
    # cc = int(jxsource.countd)
    # cc += 1
    # db.session.query(Jxsource).get(zyid).update({'countd': cc})
    # #
    # # jxsource.countd = 8
    #
    # # Jxsource.query.filter_by(id=zyid).update({'countd': cc})
    #
    #
    db.session.add(jxsource)
    #
    # db.session.commit()

    #
    # # return jxsource.countd
    #
    # # if os.path.isfile(os.path.join('upload', filename)):
    return send_from_directory('uploadb', filename, as_attachment=True) #
    # abort(404)


@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = NameForm()
    # bujuan=None
    # jxsources = Jxsource.query.filter_by(user=current_user._get_current_object()).order_by(Jxsource.outtime.desc())
    jxsources = Jxsource.query.order_by(Jxsource.uptime.desc())
    user = current_user._get_current_object()
    if form.validate_on_submit():
        zytype = Zytype.query.get(form.zytype.data)
        zyname = form.zyname.data

        uploaded_file = form.uploadfile.data

        # filename = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # filename = os.path.join('upload', uploaded_file.filename)

        # uploaddir = os.path.join(os.path.dirname(__file__), 'static', 'upload')
        pdir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        # uploaddir = os.path.join(os.path.dirname(__file__), 'static', 'upload')
        uploaddir = os.path.join(pdir, 'upload')

        # filename = os.path.join(uploaddir, 'tmpabc.txt')

        ext = os.path.splitext(uploaded_file.filename)[1]

        t = time.time()
        nowTime = lambda: int(round(t * 1000))

        tmpstr = current_user.username + str(nowTime())

        #tmpstr = tmpstr.encode("utf-8")
        md5filename = hashlib.md5()
        #md5filename.update(tmpstr)

        md5filename.update(tmpstr.encode('utf-8'))


        #savefilename = md5filename[:15] + ext  # uploaded_file.filename
        savefilename = '%s%s' % (md5filename.hexdigest()[:15], ext)

        fullsavefilename = os.path.join(uploaddir, savefilename)
        uploaded_file.save(fullsavefilename)

        jxsource = Jxsource(user=user, zytype=zytype, zyname=zyname, filename=savefilename, ext=ext)

        # jxsource = Jxsource(user=user, zytype=zytype, zyname=zyname, filename='temp')

        db.session.add(jxsource)
        db.session.commit()

        flash('上传成功')
        return redirect(url_for('.index'))
    else:
        return render_template('upload.html', form=form, jxsources=jxsources)


@main.route('/delete/<int:zyid>', methods=['GET'])
@login_required
def delete(zyid):
    # jxsources = Jxsource.query.filter_by(user=current_user._get_current_object()).order_by(Jxsource.outtime.desc())

    jxsource = Jxsource.query.get_or_404(zyid)

    user = current_user._get_current_object()
    if user == jxsource.user or user.isadm:

        filename = jxsource.filename


        user = current_user._get_current_object()

        # filename = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # filename = os.path.join('upload', uploaded_file.filename)

        # uploaddir = os.path.join(os.path.dirname(__file__), 'static', 'upload')
        pdir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        # uploaddir = os.path.join(os.path.dirname(__file__), 'static', 'upload')
        uploaddir = os.path.join(pdir, 'upload')

        fullsavefilename = os.path.join(uploaddir, filename)

        if os.path.exists(fullsavefilename):
            # 删除文件，可使用以下两种方法。
            os.remove(fullsavefilename)

        #uploaded_file.save(fullsavefilename)

        db.session.delete(jxsource)
        #db.session.add(jxsource)
        flash('删除成功')
        return redirect(url_for('.index'))
    else:
        flash('你没有删除权限')
        return redirect(url_for('.index'))

@main.route('/', methods=['GET'])
@login_required
def index():
    # form = NameForm()
    # bujuan=None
    # jxsources = Jxsource.query.filter_by(user=current_user._get_current_object()).order_by(Jxsource.outtime.desc())
    jxsources = Jxsource.query.order_by(Jxsource.uptime.desc())
    user = current_user._get_current_object()
    # if form.validate_on_submit():
    #     zytype = Zytype.query.get(form.zytype.data)
    #
    #     jxsource = Jxsource(user=user, zytype=zytype, zyname=form.zyname.data)
    #     db.session.add(jxsource)
    #     flash('添加成功')
    #     return redirect(url_for('.index'))

    # 管理账号转到管理页
    if user.isadm:
        return redirect(url_for('main.count'))
    else:
        # 一般用户转转到首页..
        # return render_template('index.html', form=form, jxsources=jxsources)
        return render_template('index.html', jxsources=jxsources)

#
# @main.route('/list')
# def list():
#     bujuans=Bujuan.query.order_by(Bujuan.outtime.desc())
#     return render_template('list.html', bujuans=bujuans)

# @main.route('/user/<username>')
# def user(username):

@main.route('/count')
@login_required
def count():

    # countbujuans = db.session.query(Xiangmu.xiangmu, db.func.sum(Bujuan.jine),Xiangmu.id).join(Bujuan).group_by(
    #     Xiangmu.xiangmu).all()
    #
    #
    # alls = db.session.query(db.func.sum(Bujuan.jine)).all()
    #
    #
    # countbujuanbyusers = db.session.query(Xiangmu.xiangmu, User.username,db.func.sum(Bujuan.jine)).join(Bujuan).join(User).group_by(
    #     Xiangmu.xiangmu, Bujuan.user).all()
    #
    # return render_template('count.html', bujuans=countbujuans, alls=alls,countbujuanbyusers=countbujuanbyusers)

    jxsources = Jxsource.query.order_by(Jxsource.uptime.desc())
    user = current_user._get_current_object()

    return render_template('count.html', jxsources=jxsources)

# @main.route('/countlist/<int:xiangmuid>')
# @login_required
# def countlist(xiangmuid):
#
#     alls = db.session.query(db.func.sum(Bujuan.jine)).all()
#
#
#     countbujuanbyusers = db.session.query(Xiangmu.xiangmu, User.username,db.func.sum(Bujuan.jine)).join(Bujuan).join(User).group_by(
#         Xiangmu.xiangmu, User.id).having(Bujuan.xiangmu_id==xiangmuid).all()
#
#     return render_template('countlist.html', alls=alls,countbujuanbyusers=countbujuanbyusers)
