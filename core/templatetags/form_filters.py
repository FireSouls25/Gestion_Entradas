from django import template

register = template.Library()

@register.filter(name='add_attr')
def add_attr(field, css):
    attrs = {}
    classes = []
    definition = css.split(',')

    for d in definition:
        if ':' not in d:
            classes.append(d.strip())
        else:
            key, val = d.split(':', 1)
            attrs[key.strip()] = val.strip()

    if classes:
        attrs['class'] = ' '.join(classes)

    return field.as_widget(attrs=attrs)
