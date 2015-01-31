from django import template
from django.db.models import Q

from gipsy.dashboard.models import GipsyDashboardMenu
from gipsy.dashboard.settings import GIPSY_DASHBOARD_URL,\
    GIPSY_VANILLA_INDEX_URL, GIPSY_THEME, GIPSY_DASHBOARD_TITLE


register = template.Library()
tag_func = register.inclusion_tag('gipsy/dashboard/widgets/base.html',
                                  takes_context=True)


@register.inclusion_tag('gipsy/dashboard/menu.html',
                        takes_context=True)
def gipsy_dashboard_menu(context, *args, **kwargs):
    """
    This tags manages the display of the admin menu.
    """
    context['items'] = GipsyDashboardMenu.objects.filter(parent__isnull=True)\
        .order_by('order')
    context['active'] = None
    if context['request'].path:
        request_formated = context['request'].get_full_path()[1:]
        active = GipsyDashboardMenu.objects\
            .filter(Q(url=request_formated) | Q(url=request_formated[:-1]))[:1]
    if len(active):
        context['active'] = active[0]
    context['dashboard_url'] = GIPSY_DASHBOARD_URL
    context['vanilla_index_url'] = GIPSY_VANILLA_INDEX_URL
    return context


@register.inclusion_tag('gipsy/dashboard/widgets/active_users.html')
def dashboard_active_users(count=0, title="CURRENTLY ACTIVE USERS",
                           label="CURRENT USERS"):
    return {'count': count, 'title': title, 'label': label}


@register.inclusion_tag('gipsy/dashboard/widgets/item_list.html')
def dashboard_item_list(items, title="MOST RECENT ITEMS"):
    return {'items': items, 'title': title}


@register.simple_tag
def gipsy_theme():
    """
    Returns the theme for the Admin-Interface.
    """
    return GIPSY_THEME


@register.simple_tag
def gipsy_title():
    """
    Returns the Title for the Admin-Interface.
    """
    return GIPSY_DASHBOARD_TITLE


def gipsy_dashboard_widget(context, widget, index=None):
    """
    Template tag that renders a given dashboard module
    """
    context.update({
        'template': widget.template,
        'widget': widget,
        'index': index,
    })
    return context
gipsy_dashboard_widget = tag_func(gipsy_dashboard_widget)
