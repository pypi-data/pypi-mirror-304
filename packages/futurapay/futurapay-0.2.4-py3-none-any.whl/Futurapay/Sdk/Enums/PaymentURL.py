from enum import Enum

class PaymentURL(Enum):
    LIVE_URL = 'https://payment-widget.futurapay.com/widget/deposit/?'
    STAGE_URL = 'https://stage-payment-widget.futurapay.com/widget/deposit/?'