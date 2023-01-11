from django import template


register = template.Library()


@register.simple_tag(name='dict_value')
def dict_value(diction, key):
	return diction[key]


