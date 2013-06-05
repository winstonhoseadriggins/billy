from billy.models.base import Base, JSONDict
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from pytz import UTC
from datetime import datetime
from dateutil.relativedelta import relativedelta
from billy.errors import BadIntervalError
from billy.customer.models import Customer


class Payout(Base):
    __tablename__ = 'payouts'

    payout_id = Column(String, primary_key=True)
    marketplace = Column(String)
    name = Column(String)
    payout_amount_cents = Column(Integer)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=UTC), default=datetime.now(UTC))
    deleted_at = Column(DateTime(timezone=UTC))
    updated_at = Column(DateTime(timezone=UTC), default=datetime.now(UTC))
    payout_interval = Column(JSONDict)
    customers = relationship(Customer.__name__, backref='payouts')
    #Payout by percentage
    __table_args__ = (
    UniqueConstraint('payout_id', 'marketplace', name='payoutid_marketplace'),
    )


    def __init__(self, id, marketplace, name, payout_amount_cents,
                 payout_interval):
        self.payout_id = id
        self.name = name
        self.payout_amount_cents = payout_amount_cents
        if not isinstance(payout_interval, relativedelta):
            raise BadIntervalError(
                "payout_interval must be a relativedelta type.")
        else:
            self.payout_interval = self.from_relativedelta(payout_interval)
        self.marketplace = marketplace

    def from_relativedelta(self, inter):
        return {
            'years': inter.years,
            'months': inter.months,
            'days': inter.days,
            'hours': inter.hours,
            'minutes': inter.minutes
        }

    def to_relativedelta(self, param):
        return relativedelta(years=param['years'], months=param['months'],
                             days=param['days'], hours=param['hours'],
                             minutes=param['minutes'])

