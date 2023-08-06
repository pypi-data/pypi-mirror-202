import os
import time
from obs import ObsClient
from urllib.parse import urlparse

AK = os.environ.get('HW_OBS_AK')
SK = os.environ.get('HW_OBS_SK')
server = os.environ.get('HW_OBS_SERVER')

_obsClient = None
_last_time = None


# 检查字符串是否为合法的obs路径
# obs路径格式为：obs://bucketname/objectname
def _is_obs_path(path):
    if path.startswith('obs://'):
        return True
    else:
        return False


def copy(src, dest):
    global _obsClient
    if _obsClient is None:
        _obsClient = ObsClient(access_key_id=AK, secret_access_key=SK, server=server)

    _download_folder(src, dest)


def download(obs_url):
    global _obsClient
    if _obsClient is None:
        _obsClient = ObsClient(access_key_id=AK, secret_access_key=SK, server=server)

    if not _is_obs_path(obs_url):
        raise Exception('obs url is invalid')

    url = urlparse(obs_url)
    bucket_name = url.hostname
    try:
        resp = _obsClient.getObject(bucket_name, url.path[1:], loadStreamInMemory=True)

        if resp.status < 300:
            print('requestId:', resp.requestId)
            # 获取对象内容
            print('size:', resp.body.size)
            return resp.body.buffer

        else:
            print('errorCode:', resp.errorCode)
            print('errorMessage:', resp.errorMessage)
    except:
        import traceback
        print(traceback.format_exc())


def _download_one_file(bucketName, src, dest):
    try:
        resp = _obsClient.getObject(bucketName, src, downloadPath=dest,
                                    progressCallback=download_progress_callback)
        if resp.status < 300:
            print('requestId:', resp.requestId)
            print('url:', resp.body.url)
        else:
            print('errorCode:', resp.errorCode)
            print('errorMessage:', resp.errorMessage)
    except:
        import traceback
        print(traceback.format_exc())


# 流式下载
def _download_one_file_stream(bucketName, src):
    try:
        resp = _obsClient.getObject(bucketName, src, loadStreamInMemory=False)

        if resp.status < 300:
            print('requestId:', resp.requestId)
            # 读取对象内容
            while True:
                chunk = resp.body.response.read(65536)
                if not chunk:
                    break
                yield chunk
            resp.body.response.close()
        else:
            print('errorCode:', resp.errorCode)
            print('errorMessage:', resp.errorMessage)
    except:
        import traceback
        print(traceback.format_exc())


def _download_folder(obs_url, dest_path):
    url = urlparse(obs_url)
    bucket_name = url.hostname
    try:
        max_num = 1000
        mark = None
        while True:
            resp = _obsClient.listObjects(bucket_name, url.path[1:], marker=mark, max_keys=max_num)
            if resp.status < 300:
                for one_key in resp.body.contents:
                    name = one_key['key']
                    if not name.endswith('/'):
                        _download_one_file(bucket_name, name,
                                           os.path.join(dest_path, os.path.relpath('/' + name, url.path)))
                if resp.body.is_truncated is True:
                    mark = resp.body.next_marker
                else:
                    break
            else:
                print('errorCode:', resp.errorCode)
                print('errorMessage:', resp.errorMessage)
    except:
        import traceback
        print(traceback.format_exc())


def download_progress_callback(transferred_amount, total_amount, total_seconds):
    global _last_time
    if _last_time is None:
        _last_time = time.time()
    if time.time() - _last_time > 3:
        print("正在下载中，平均速率： {} (KB/S), 进度： {}%".format(int(transferred_amount * 1.0 / total_seconds / 1024),
                                                                 int(transferred_amount * 100.0 / total_amount)))
        _last_time = time.time()
