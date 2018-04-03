# -*- coding: utf-8 -*-

from web_frame import create_app


application = create_app()

print('Starting server...')
application.run(host='0.0.0.0', port=2000, debug=True)