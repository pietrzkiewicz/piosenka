from django.views.generic import View
from django.shortcuts import render
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType


from blog.models import Post
from events.models import Event
from songs.models import Song


class IndexView(View):
    template_name = "frontpage/index.html"
    post_count = 3
    song_count = 20

    def get(self, request):
        song_type = ContentType.objects.get(app_label="songs", model="song")
        entries = LogEntry.objects.filter(content_type=song_type, action_flag=ADDITION).order_by("-action_time")[:IndexView.song_count]
        songs = [(x.action_time, Song.objects.get(pk=x.object_id)) for x in entries]
        return render(
            request,
            self.template_name,
            {
                'posts': Post.objects.all().order_by('-date')[0:IndexView.post_count],
                'events': Event.current.all(),
                'songs': songs,
            }
        )
