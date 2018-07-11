import calendar

from flask import g
from flask_appbuilder import ModelView
from flask_appbuilder import expose, has_access
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_appbuilder.models.mongoengine.interface import MongoEngineInterface

from app import appbuilder
from app.Sequences.models import ContactGroup, Sequences, Tags
import json
import datetime

def get_user():
    return g.user.id


class SequencesModelView(ModelView):
    datamodel = MongoEngineInterface(Sequences)
    list_columns = ['name', 'personal_celphone', 'birthday', 'contact_group.name']

    @expose('/add', methods=['GET', 'POST'])
    @has_access
    def add(self):

        defaults = {

            "name": "Code",
            "creator": "Nick Edgington",
            "date":  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        widget = self._add()
        if not widget:
            return self.post_add_redirect()
        else:
            return self.render_template("general/model/add.html",  # self.add_template,
                                        title=self.add_title,
                                        time=datetime.datetime.now().strftime("%B"),
                                        widgets=widget,
                                        defaults= defaults)


class GroupModelView(ModelView):
    datamodel = MongoEngineInterface(ContactGroup)
    related_views = [SequencesModelView]
    search_columns = ['name']


class TagsModelView(ModelView):
    datamodel = MongoEngineInterface(Tags)


class SequencesChartView(GroupByChartView):
    datamodel = MongoEngineInterface(Sequences)
    chart_title = 'Grouped contacts'
    label_columns = SequencesModelView.label_columns
    chart_type = 'PieChart'

    definitions = [
        {
            'group': 'contact_group',
            'series': [(aggregate_count, 'contact_group')]
        },
        {
            'group': 'gender',
            'series': [(aggregate_count, 'gender')]
        }
    ]


def pretty_month_year(value):
    return calendar.month_name[value.month] + ' ' + str(value.year)


def pretty_year(value):
    return str(value.year)


class SequencesTimeChartView(GroupByChartView):
    datamodel = MongoEngineInterface(Sequences)

    chart_title = 'Grouped Birth contacts'
    chart_type = 'AreaChart'
    label_columns = SequencesModelView.label_columns
    definitions = [
        {
            'group': 'month_year',
            'formatter': pretty_month_year,
            'series': [(aggregate_count, 'contact_group')]
        },
        {
            'group': 'year',
            'formatter': pretty_year,
            'series': [(aggregate_count, 'contact_group')]
        }
    ]


appbuilder.add_view(GroupModelView, "List Groups", icon="fa-folder-open-o", category="Sequences",
                    category_icon='fa-envelope')
appbuilder.add_view(SequencesModelView, "List Contacts", icon="fa-folder-open-o", category="Sequences",
                    category_icon='fa-envelope')
appbuilder.add_view(TagsModelView, "List Tags", icon="fa-folder-open-o", category="Sequences",
                    category_icon='fa-envelope')
appbuilder.add_separator("Sequences")
appbuilder.add_view(SequencesChartView, "Contacts Chart", icon="fa-dashboard", category="Sequences")
appbuilder.add_view(SequencesTimeChartView, "Contacts Birth Chart", icon="fa-dashboard", category="Sequences")

appbuilder.security_cleanup()
