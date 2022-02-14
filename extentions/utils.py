from . import jalali
from django.utils import timezone

def number_converter(mystr):
	number = {
		"0" : "۰",	
		"1" : "۱",	
		"2" : "۲",	
		"3" : "۳",	
		"4" : "۴",	
		"5" : "۵",	
		"6" : "۶",	
		"7" : "۷",	
		"8" : "۸",	
		"9" : "۹",	
	}
	for e, p in number.items():
		mystr = mystr.replace(e, p)
	return mystr


def time_converter (time):
	time = timezone.localtime(time)
	jmonth = ['حمل', 'ثوز', 'جوزا', 'سزطان', 'اسد', 'سنبله', 'میزان', 'عقرب', 'قوس', 'جدی', 'دلو', 'حوت']
	time = timezone.localtime(time)
	time_to_str = "{},{},{}".format(time.year, time.month, time.day)
	time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()

	time_to_list = list(time_to_tuple)

	for index, month in enumerate(jmonth):
		if time_to_list[1] == index + 1 :
			time_to_list[1] = month
			break

	out_put = " {} {} {} ساعت {}:{}".format(
		time_to_list[2],
		time_to_list[1],
		time_to_list[0],
		time.hour,
		time.minute
	)

	return number_converter(out_put)