# _*_ encoding: utf-8 _*_
from flask import Blueprint


main=Blueprint('main',__name__)

# @main.app_context_processor
# def inject_permissions():
#     return  dict(Permission=Permission)

from . import views