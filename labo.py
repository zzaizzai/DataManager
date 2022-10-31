import pathlib
import datetime
import workdays

start_date = datetime.datetime(2022,11,1)
end_date = datetime.datetime(2022,11,7)


print(workdays.workday(start_date, days=4))
print(workdays.networkdays(start_date, end_date))