from src.dash_client.app import app
from src.dash_client.core.settings import settings

if __name__ == '__main__':
    app.run_server(debug=True,
                   host=settings.host_dash,
                   port=settings.port_dash)