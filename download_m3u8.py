#!/bin/python
import os, time, sys, threading,random


def thre(myurl):
    global count,number,current_number,hls_output
    mynumber=number
    current_ts=tmp_videos_dir+pre_random+str(mynumber)+".ts"
    os.popen("wget -c --tries=1000 --wait=5 --waitretry=5 --timeout=60 '" + str(myurl) + "' -O "+current_ts).read()
    count -= 1
    while 1:
        if mynumber==current_number:
            os.popen("cat "+current_ts+" >> "+hls_output).read()
            os.remove(current_ts)
            current_number+=1
            # recode = url0 + "\t" + root_dir + "\t" + tmp_videos_dir + "\t" + pre_random + "\t"+str(current_number)
            # os.popen("echo "+recode+" > "+tmp_videos_dir+pre_random+".log")
            break
        time.sleep(0.1)


def print_number():
    wc = False
    global count,thread_stack
    times=0
    while 1:
        # print("begin")
        # print(os.popen("ps -ef|grep -i wget|wc -l").read())
        # print("end")
        # time.sleep(3)
        # break
        times+=1
        if times%60==0 and len(thread_stack)>30:
            print('do join')
            for i in thread_stack[0:len(thread_stack)-30]:
                i.join()
        if int(os.popen("ps -ef|grep -i wget|wc -l").read()[0]) > 2:
            # print('wget:'+ str(os.popen("ps -ef|grep -i wget").read()))
            time.sleep(1)
            print('number:'+str(count))
            continue
        print('sleep 5s and check again')
        time.sleep(5)
        if int(os.popen("ps -ef|grep -i wget|wc -l").read()) <= 2:
            print('print number done')
            if os.path.exists(tmp_videos_dir):
                # os.remove(tmp_videos_dir+pre_random+".log")
                time.sleep(15)
                os.removedirs(tmp_videos_dir)
            break
        print('print number again')


def do_create_thread(url):
    global count,number,thread_stack
    while 1:
        if count < 10:
            time.sleep(0.1+random.random()/10)
            print('url: '+url)
            thread = threading.Thread(target=thre, args=(url,))
            thread.start()
            thread_stack.append(thread)
            return


thread_stack=[]
pre_random=''.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 8))
try:
    url0=sys.argv[1]
    if url0.find('http')<0:
        print('error url')
        exit()
except Exception:
    print('no url')
    exit()
root_dir=os.getcwd()+'/'
tmp_videos_dir=root_dir+".hls/"
if not os.path.exists(tmp_videos_dir):
    os.makedirs(tmp_videos_dir)
try:
    hls_output=sys.argv[2]
except Exception:
    hls_output="output.ts"
if hls_output.find('/')>0:
    print('err name')
    exit()
hls_output=root_dir+hls_output
if os.path.exists(hls_output):
    if input('file already exists, continue?').lower().find('y')<0:
        print('got it ,exit')
        exit()
    else:
        print('got it ,continue')
# current_log=tmp_videos_dir+pre_random+".log"
# exit()
# output = os.popen('curl "' + str(sys.argv[1]) + '" |grep "ts$"|head -20')
output = os.popen('curl "' + str(sys.argv[1]) + '" |grep "\\.ts"')
# print(output.read().split('\n')[0])
urls = output.read().split('\n')
print(urls)
number = 0
current_number=0
count = 0
thread0 = threading.Thread(target=print_number)
thread0.start()

# time.sleep(5)
# exit()
for url in urls:
    if url!='':
        if url.find("http")==0:
            url=url
        elif url.find('/')<0:
            url=url0[0:url0.rfind('/')+1]+url
        elif url.find('/')>=0:
            url=url0[0:url0.find('/',9)]+url
        else:
            print('dont know url')
            exit()
        do_create_thread(url)
        number+=1
        count+=1
        # time.sleep(5)
        # exit()
print(output)
