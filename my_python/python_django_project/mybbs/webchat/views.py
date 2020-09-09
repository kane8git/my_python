from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponse
from django.core.cache import cache

# Create your views here.
from webchat import models
import queue,json,time,os

GLOBAL_MSG_QUEUES ={

}


@login_required
def dashboard(request):

    return render(request,'webchat/dashboard.html')


@login_required
def send_msg(request):
    print(request.POST)
    print(request.POST.get("msg"))
    msg_data = request.POST.get('data')
    # 如果消息存在
    if msg_data:
        msg_data = json.loads(msg_data)
        # 消息增加时间戳
        msg_data['timestamp'] = time.time()
        # 如果消息类型是 'single'
        if msg_data['type'] == 'single':
            # 注意，这里要格式为int类型，否则无法接收消息
            if not GLOBAL_MSG_QUEUES.get(int(msg_data['to'])):
                GLOBAL_MSG_QUEUES[int(msg_data["to"])] = queue.Queue()
            GLOBAL_MSG_QUEUES[int(msg_data["to"])].put(msg_data)
        else:
            group_obj = models.WebGroup.objects.get(id=msg_data['to'])
            for member in group_obj.members.select_related():
                # 如果字典不存在这个用户的queue
                if not GLOBAL_MSG_QUEUES.get(member.id):
                    GLOBAL_MSG_QUEUES[int(member.id)] = queue.Queue()   # 创建一个队列 queue
                if member.id != request.user.userprofile.id:      # 如果不相等
                    GLOBAL_MSG_QUEUES[member.id].put(msg_data)   # 把消息放进去

    print(GLOBAL_MSG_QUEUES)
    return HttpResponse('---msg recevied---')


def get_new_msgs(request):

    if request.user.userprofile.id not in GLOBAL_MSG_QUEUES:
        print("no queue for user [%s]" % request.user.userprofile.id, request.user)
        GLOBAL_MSG_QUEUES[request.user.userprofile.id] = queue.Queue()
    msg_count = GLOBAL_MSG_QUEUES[request.user.userprofile.id].qsize()
    q_obj = GLOBAL_MSG_QUEUES[request.user.userprofile.id]
    msg_list = []
    if msg_count >0:

        for msg in range(msg_count):
            msg_list.append(q_obj.get())

        print("new msgs:",msg_list)
    else:   # 没消息,要挂起
        print("no new msg for ", request.user, request.user.userprofile.id)
        try:
            # 监听超时
            msg_list.append(q_obj.get(timeout=60))
        except queue.Empty:
            print("\033[41;1mno msg for [%s][%s] ,timeout\033[0m" % (request.user.userprofile.id,request.user))
    return HttpResponse(json.dumps(msg_list))


# 增加上传文件方法   增加上传进度条
# 上传文件，将上传的文件大小写入到一个cache里，另外的方法读取cache内容，来实现上传进度条
def file_upload(request):
    print(request.POST, request.FILES)
    file_obj = request.FILES.get('file')
    user_home_dir = "uploads/%s" % request.user.userprofile.id
    if not os.path.isdir(user_home_dir):
        os.mkdir(user_home_dir)
    new_file_name = "%s/%s" % (user_home_dir, file_obj.name)
    recv_size = 0
    cache.delete(file_obj.name)
    with open(new_file_name, 'wb') as new_file_obj:
        for chunk in file_obj.chunks():
            new_file_obj.write(chunk)
            recv_size += len(chunk)
            cache.set(file_obj.name, recv_size)
    print(cache.get(file_obj.name))
    return HttpResponse("-- upload success --")



# 读取cache里的内容
def file_upload_progress(request):
    print("------you meiy ----------")
    filename = request.GET.get("filename")
    print("this is a name : %s " % filename)
    progress = cache.get(filename)
    print("file[%s] uploading progress[%s]" % ( filename, progress))
    return HttpResponse(json.dumps({"recv_size": progress}))


# 清除cache_key 的方法
def delete_cache_key(request):
    cache_key = request.GET.get("cache_key")
    cache.delete(cache_key)
    return HttpResponse("cache key %s delete" % cache_key)







