from web.models import CoreGadget, Gadget
from web.variables import *


def generate_gadget(gadget):
	core = CoreGadget.objects.get(id=gadget.config['core'])
	values = {
		'{prefix}': gadget.name.replace(' ', '') + '_' + str(gadget.id),
		'{subgadget}': '',
		'{title}': gadget.config['display'],
		'{subtitle}': gadget.config['subtitle'],
		'{url}': gadget.config['url'],
		'{html}': gadget.html,
		'{js}': gadget.js,
		'{css}': gadget.css
	}

	if gadget.config['subgadget'] > 0:
		subgadget = Gadget.objects.get(id=gadget.config['subgadget'])
		values['{subgadget}'] = subgadget.name.replace(' ', '') + '_' + str(subgadget.id)

	for k, v in values.items():
		values['{html}'] = values['{html}'].replace(k, v)
		values['{js}'] = values['{js}'].replace(k, v)
		values['{css}'] = values['{css}'].replace(k, v)

	for k, v in values.items():
		core.html = core.html.replace(k, v)
		core.js = core.js.replace(k, v)
		core.css = core.css.replace(k, v)

	data = {
		'html': core.html,
		'js': core.js,
		'css': core.css
	}

	return data


def format_date(date):
	day = date.split(' ')[0]
	month = str(months_to_number[date.split(' ')[1]])
	year = date.split(' ')[2]
	return '%s-%s-%s' % (year, month, day)


def display_format_date(date):
	date = date.strftime('%d %m %Y')
	day = date.split(' ')[0]
	month = number_to_months[int(date.split(' ')[1])]
	year = date.split(' ')[2]
	return '%s %s %s' % (day, month, year)


def default_date_format(date):
	return date.strftime('%m-%d-%Y')