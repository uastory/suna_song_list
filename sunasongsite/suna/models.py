from django.db import models


'''
매일 매일의 플레이 리스트가 있음
리스트 안에는 가수 - 노래 제목 표시
노래는 고음곡이 있음

알고 싶은 통계
어느 노래가 많이 불렸을까?
부른 노래 평균 수?

가수별 통계, 필터링
제목별? 오더?
'''

class Song(models.Model):
    title = models.CharField(
            "제목",
            max_length=200)
    singer = models.CharField(
            "가수",
            max_length=200)
    is_high = models.BooleanField(
            "고음여부",
            default=False)
    ctime = models.DateField(
            "최초 추가 일시",
            null=True, blank=True)

    def __str__(self):
        return f"{self.dp_high}{self.singer} - {self.title}"

    @property
    def dp_high(self):
        if self.is_high:
            return "*"
        return ''


class PlayList(models.Model):
    play_date = models.DateField()
    songs = models.ManyToManyField(Song)
