from .models import class_cnt

def GET_PK(param):
    cur = class_cnt.objects.first()
    if param == "problem":
        result = format(cur.problem_cnt, "012X")
        cur.problem_cnt += 1

    cur.save()
    return result
