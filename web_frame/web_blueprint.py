# -*- coding: utf-8 -*-

from flask import Blueprint
from web_frame.web_logger import Log


web_frame = Blueprint('web_frame', __name__, template_folder='../templates', static_folder='../static')

Log.info('static folder: %s' % web_frame.static_folder)
Log.info('template folder: %s' % web_frame.template_folder)