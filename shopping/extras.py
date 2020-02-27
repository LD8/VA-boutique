# imports for ref_number_generator
from random import choice
from string import digits, ascii_uppercase
from datetime import date
from django.core.mail import send_mass_mail
from VA import settings


def anonymous_ref_number_generator():
    date_str = date.today().strftime('%d%m%y')
    random_str = "".join([choice(digits) for x in range(2)]) + \
        "".join([choice(ascii_uppercase) for x in range(2)])
    return "UN{}-{}".format(date_str, random_str)


def ref_number_generator():
    date_str = date.today().strftime('%d%m%y')
    random_str = "".join([choice(ascii_uppercase) for x in range(2)]) + \
        "".join([choice(digits) for x in range(2)])
    return "VA{}-{}".format(date_str, random_str)


def mail_order_detail(new_order_username, new_order_ref_number, new_order_link, new_order_item_names, customer_email):
    va_email = settings.DEFAULT_FROM_EMAIL
    # msg_to_customer = 'Hi {username},\n\nThank you for the order. We will contact you shortly.\nYour order number is: {ref}\nCheckout your order: {order_link}\n\nYours, VA-Boutique\n'
    msg_to_customer = 'Здравствуйте {username},\n\nСпасибо за заказ! Наш менеджер свяжется с Вами в течении 24 часов.\nНомер Вашего заказа {ref}\nПосмотреть Ваш заказ: {order_link}\n\nВаш VA-Boutique\n'.format(
        username=new_order_username,
        ref=new_order_ref_number,
        order_link=new_order_link,
    )
    msg_to_va = 'Order No.: {ref}\nUser: {username}\nOrdered Item: {itemname}\nOrder Link: {order_link}\n'.format(
        ref=new_order_ref_number,
        username=new_order_username,
        itemname=new_order_item_names,
        order_link=new_order_link,
    )

    email_to_customer = (
        'VA BOUTIQUE - НОВЫЙ ЗАКАЗ {}'.format(new_order_ref_number),
        msg_to_customer,
        va_email,
        [customer_email]
    )
    email_to_va = (
        'НОВЫЙ ЗАКАЗ {}'.format(new_order_ref_number),
        msg_to_va,
        va_email,
        ['va@va-boutique.com']
    )

    send_mass_mail((email_to_customer, email_to_va), fail_silently=False)
