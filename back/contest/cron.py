import datetime
from django.db.models import Q
from comment.models import Comment
from contest.models import Contest
from expert.models import Expert_projects, Expert_contests
from util.util import send_invation__


def send_to_all_expert_in_time():
    cons = Contest.objects.filter(Q(expire_date__gte=datetime.datetime.now() + datetime.timedelta(days=7)) & Q(expire_date__lte=datetime.datetime.now() + datetime.timedelta(days=8)))
    content1 = """
    {}老师，你好
    距离您负责评审的比赛{} 结束还有一个星期，请尽快评审作品， 或者将您未提交的作品提交
    """
    for con in cons:
        exps = Expert_contests.objects.filter(Q(contest_id=con.id))
        for i in exps:
            needs = False
            projs = Expert_projects.objects.filter(expert_id=i.expert_id, contest_id=con.id)
            for p in projs:
                if Comment.objects.filter(project_id=p.id, expert_id=i.expert_id).count() < 1 or Comment.objects.get(project_id=p.id, expert_id=i.expert_id).state == 0:
                    needs = True
                    break
            if needs:
                send_invation__(i.expert.email,content1.format(i.expert.name, con.name))

    cons = Contest.objects.filter(Q(expire_date__gte=datetime.datetime.now() + datetime.timedelta(days=1)) & Q(expire_date__lte=datetime.datetime.now() + datetime.timedelta(days=2)))
    content1 = """
       {}老师，你好
       距离您负责评审的比赛{} 结束还有一天，请尽快评审作品， 或者将您未提交的作品提交
       """
    for con in cons:
        exps = Expert_contests.objects.filter(Q(contest_id=con.id))
        for i in exps:
            needs = False
            projs = Expert_projects.objects.filter(expert_id=i.expert_id, contest_id=con.id)
            for p in projs:
                if Comment.objects.filter(project_id=p.id, expert_id=i.expert_id).count() < 1 or Comment.objects.get(
                        project_id=p.id, expert_id=i.expert_id).state == 0:
                    needs = True
                    break
            if needs:
                send_invation__(i.expert.email, content1.format(i.expert.name, con.name))



