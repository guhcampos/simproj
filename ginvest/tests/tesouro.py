import datetime
from simproj.util import tesouro


def test_date_range():

    startdate = datetime.datetime.today()
    enddate = startdate + datetime.timedelta(days=18*30)
    value = 1000.00

    for period in tesouro.profitability(value, startdate, enddate, 5.0, None):
        print(len(period))


def test_all():
    test_date_range()


if __name__ == "__main__":

    test_all()