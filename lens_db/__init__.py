import logging

logging.basicConfig(
    # filename=Path(__file__).parent.parent / 'flask-app.log',
    level=logging.DEBUG,
    format='%(asctime)s] %(levelname)s - %(module)s:%(lineno)s - %(message)s')
