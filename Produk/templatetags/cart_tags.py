from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()


@register.simple_tag
def cart_total(cart):
    total = sum(item.product.harga_produk * item.quantity for item in cart)
    return '{:.2f}'.format(total)
