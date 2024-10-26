import logging
import sys

class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.correlation_id = getattr(record, 'correlation_id', 'N/A')
        return super().format(record)

logger = logging.getLogger("app")
handler = logging.StreamHandler(sys.stdout)
formatter = CustomFormatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(correlation_id)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
