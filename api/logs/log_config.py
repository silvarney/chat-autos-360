import os
import logging

def setup_logging():
    log_dir = '/tmp/logs'
    log_file = os.path.join(log_dir, 'history.log')
    os.makedirs(log_dir, exist_ok=True)
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            pass
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s'
    )
