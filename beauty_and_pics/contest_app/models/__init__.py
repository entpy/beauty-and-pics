from django.contrib import admin
from contest_app.models.contest_types import Contest_Type
from contest_app.models.contests import Contest
from contest_app.models.metrics import Metric
from contest_app.models.votes import Vote
from contest_app.models.points import Point

admin.site.register(Contest_Type)
admin.site.register(Contest)
admin.site.register(Metric)
admin.site.register(Vote)
admin.site.register(Point)
