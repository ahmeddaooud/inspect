from inspector import config
import os

from inspector import app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', config.PORT_NUMBER))
    app.run(host='127.0.0.1', port=port, debug=config.DEBUG)