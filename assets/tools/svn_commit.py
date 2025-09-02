# -*- coding: utf-8 -*-
#########################################
#注意，需要依赖python命令和svn命令，请确认安装正确
#1,安装python3.7，配置环境变量，在命令行执行 python --version能返回正常即可
#2，安装svn，配置环境变量，在命令行执行 svn --version 能放回正常即可
#3,post返回code=200，text=“OK”即为成功，否则 tex是错误提示信息
#########################################
import os
import subprocess
from flask import Flask, request,jsonify
import shutil
import compileall
import json

app = Flask(__name__)
# 文件目录,修改为自己本地目录
svn_folder = 'E:/projects/code/xf/trunk/'   
root_folder = 'Dev/Server/kbeLinux/kbengine/assets/scripts/'
target_folder = 'Dev/Server/kbeLinux/kbengine/assets/scripts.dist/'

@app.route('/update', methods=['POST'])
def update():
    print("request...")

    #检测是否有数据
    if not request.data:  
      return ('fail')
    
    #获取到POST过来的数据，
    params= request.data.decode('utf-8')
    prams = json.loads(params)
    version = prams.get("ver")
    files = prams.get("files")
    print("param version:%d"%version)
    print("param files:")
    print(files)
    if version<=0:
        return ('fail,version err')
    if len(files)==0:
        return ("fail,files is null")


    # 切换到代码仓库目录
    svn_path = os.path.join(svn_folder,root_folder)
    cwd =os.chdir(svn_path)
    print("change to svn_path:%s"%cwd)
    cwd1 = os.getcwd()
    print("cwd :%s"%cwd1)

    # 更新代码到指定版本
    print("change svn version to %d",version)
    b = subprocess.run(['svn', 'up', '-r', str(version)])
    print("subprocess returncode:%d "%b.returncode)
    if b.returncode!=0 :
        print("fail,svn up err!")
        return ("fail,svn up err!")

    # 编译Python文件，并将编译结果移动到指定目录
    print("process py files...")
    compile_and_move_files(root_folder, target_folder, files)

    # 拷贝其他文件到指定目录
    print("copy other files...")
    for file_path in files:
        if not file_path.endswith('.py'):
            source_path = os.path.join(svn_folder,root_folder, file_path)
            print("copy : %s"%source_path)
            target_path = os.path.join(svn_folder,target_folder, file_path)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            shutil.copy(source_path, target_path)
            print("copy suc :%s"%target_path)

    # 切换到dist目录
    dist_path = os.path.join(svn_folder,target_folder)
    os.chdir(dist_path)
    print("commit dist_path:%s"%dist_path)

    # 提交改动到SVN
    cwd2 = os.getcwd()
    print("cwd :%s"%cwd2)

    # ADD目标目录
    b = subprocess.run(['svn', 'add', dist_path, '--force'])
    if b.returncode!=0 :
        print("fail,svn add err!")
        return ("fail,svn add err!")

    # 清理目标目录
    b = subprocess.run(['svn', 'cleanup'])
    if b.returncode!=0 :
        print("fail,svn cleanup err!")
        return ("fail,svn cleanup err!")

    # b = subprocess.run(['svn', 'commit', '-m', '#1000 Update scripts.dist '])
    # if output.returncode!=0 :
    cmd = 'svn commit %s -m "#1000 Update scripts.dist"' %dist_path
    print(cmd)
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,cwd=dist_path)
    (result, error) = output.communicate()
    result = result.decode(encoding="gbk")
    error = error.decode(encoding="gbk")
    print("commit result:%s",result)  
    print("commit error:%s",error)       
    if error.strip() != "" and error.startswith("svn: E165001:") and  error.find("http:") :
            print("commit success,please review ")     
    else :
        print("fail,svn commit err!")
        return ("fail,svn commit err!")

    # 切换到source目录
    source_path = os.path.join(svn_folder,root_folder)
    os.chdir(source_path)
    print("change to  source_path:%s"%source_path)

    # 还原到原有版本
    print("change svn version back!")
    subprocess.run(['svn', 'up'])

    print("success!")
    return 'OK'

def compile_and_move_files(source_dir, target_dir, files):
    for file_path in files:
        if file_path.endswith('.py'):
            source_path = os.path.join(svn_folder,source_dir, file_path)
            print("pro: %s"%source_path)
            target_path = os.path.join(svn_folder,target_dir, file_path)
            target_path = os.path.splitext(target_path)[0] + '.pyc'
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            subprocess.run(['python', '-m', 'compileall', '-x.*\.svn.*', '-b', '-q', source_path])
            shutil.move(source_path + 'c', target_path)
            print("pro suc :%s"%target_path)


if __name__ == '__main__':
  app.run(host='127.0.0.1',port=8234)