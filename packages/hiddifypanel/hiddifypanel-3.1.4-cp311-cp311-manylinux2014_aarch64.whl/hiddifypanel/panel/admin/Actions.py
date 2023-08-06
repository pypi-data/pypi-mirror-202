#!/usr/bin/env python3
import pprint
from flask_babelex import gettext as _
import pathlib
from hiddifypanel.models import  *

from datetime import datetime,timedelta,date
import os,sys
import json
import urllib.request
import subprocess
import re
from hiddifypanel.panel import hiddify,usage
from hiddifypanel.panel import hiddify_api
from flask import current_app,render_template,request,Response,Markup,url_for
from hiddifypanel.panel.hiddify import flash

from flask_classful import FlaskView,route

class Actions(FlaskView):

    def index(self):
        return render_template('index.html')
    
    def reverselog(self,logfile):
        if logfile==None:return self.viewlogs()
        config_dir=current_app.config['HIDDIFY_CONFIG_PATH']
        
        with open(f'{config_dir}/log/system/{logfile}') as f:
            lines=[line for line in f]
            logs="".join(lines[::-1])
        # resp= Response()
        # resp.mimetype="text/plain"
        out=f'<pre style="background-color:black; color:white;padding:10px">{logs}</pre>'
        if len(lines)>5 and "----Finished!---" in "".join(lines[-min(10,len(lines)):]):
            out=f"<a href='#' target='_blank'><div style='background-color:#b1eab1; padding: 10px;border: solid;'>Finished! For scrolling the log click here.</div></a>{out}"


            
        return out
            
            

    
    def viewlogs(self):
        config_dir=current_app.config['HIDDIFY_CONFIG_PATH']
        res=[]
        for filename in sorted(os.listdir(f'{config_dir}/log/system/')):
            res.append(f"<a href='{url_for('admin.Actions:reverselog',logfile=filename)}'>{filename}</a>") 
        return Markup("<br>".join(res))
        
    @route('apply_configs', methods=['POST'])
    def apply_configs(self):
        return self.reinstall(False)

    @route('reset', methods=['POST'])
    def reset(self):
        status=self.status()
        flash(_("rebooting system may takes time please wait"),'info')
        subprocess.Popen(f"reboot",start_new_session=True)
        return status
    
    @route('reinstall', methods=['POST'])
    def reinstall(self,complete_install=True,domain_changed=False):
        if int(hconfig(ConfigEnum.db_version))<9:
            return ("Please update your panel before this action.")
        if hconfig(ConfigEnum.parent_panel):
            try:
                hiddify_api.sync_child_to_parent()
            except e as Exception:
                flash (_('can not sync child with parent panel')+" "+e)


        domain_changed=request.args.get("domain_changed",str(domain_changed)).lower()=="true"
        complete_install=request.args.get("complete_install",str(complete_install)).lower()=="true"
        if domain_changed:
            flash((_('Your domains changed. Please do not forget to copy admin links, otherwise you can not access to the panel anymore.')),'info')
        # flash(f'complete_install={complete_install} domain_changed={domain_changed} ', 'info')
        # return render_template("result.html")
        config=current_app.config
        hiddify.add_temporary_access()
        file="install.sh" if complete_install else "apply_configs.sh"
        try:
            server_ip=urllib.request.urlopen('https://v4.ident.me/').read().decode('utf8')
        except:
            server_ip="server_ip"

        # subprocess.Popen(f"{config_dir}/update.sh",env=my_env,cwd=f"{config_dir}")
        # os.system(f'cd {config_dir};{env} ./install.sh &')
        # rc = subprocess.call(f"cd {config_dir};./{file} & disown",shell=True)
        
        admin_secret=hconfig(ConfigEnum.admin_secret)
        proxy_path=hconfig(ConfigEnum.proxy_path)
        admin_links=f"<h5 >{_('Admin Links')}</h5><ul>"
        admin_links+=f"<li><span class='badge badge-danger'>{_('Not Secure')}</span>: <a class='badge ltr share-link' href='http://{server_ip}/{proxy_path}/{admin_secret}/admin/'>http://{server_ip}/{proxy_path}/{admin_secret}/admin/</a></li>"
        domains=get_panel_domains()
        # domains=[*domains,f'{server_ip}.sslip.io']
        for d in domains:
                link=f'https://{d}/{proxy_path}/{admin_secret}/admin/'
                admin_links+=f"<li><a target='_blank' class='badge ltr' href='{link}'>{link}</a></li>"

        resp= render_template("result.html",
                            out_type="info",
                            out_msg=_("Success! Please wait around 4 minutes to make sure everything is updated. During this time, please save your proxy links which are:")+
                                    admin_links,
                            log_path=(f"https://{domains[0]}" if domain_changed else "")+f"/{proxy_path}/{admin_secret}/admin/actions/reverselog/0-install.log/"
                            
        )

        subprocess.Popen(f"{config['HIDDIFY_CONFIG_PATH']}/{file}",cwd=f"{config['HIDDIFY_CONFIG_PATH']}",start_new_session=True)
        import time
        time.sleep(1)
        return resp


    
    def status(self):
        # hiddify.add_temporary_access()
        config=current_app.config
        # configs=read_configs()
        # subprocess.Popen(f"{config_dir}/update.sh",env=my_env,cwd=f"{config_dir}")
        # os.system(f'cd {config_dir};{env} ./install.sh &')
        # rc = subprocess.call(f"cd {config_dir};./{file} & disown",shell=True)
        from urllib.parse import urlparse
        admin_secret=hconfig(ConfigEnum.admin_secret)
        o = urlparse(request.base_url)
        domain=o.hostname
        subprocess.Popen(f"{config['HIDDIFY_CONFIG_PATH']}/status.sh",cwd=f"{config['HIDDIFY_CONFIG_PATH']}",start_new_session=True)
        
        return render_template("result.html",
                            out_type="info",
                            out_msg=_("see the log in the bellow screen"),
                            log_path=url_for("admin.Actions:reverselog",logfile=f"status.log")
        )



    @route('update', methods=['POST'])
    def update(self):
        hiddify.add_temporary_access()
        config=current_app.config
        cwd = os.getcwd()
        
        # os.chdir(config_dir)
        # rc = subprocess.call(f"./install.sh &",shell=True)
        # rc = subprocess.call(f"cd {config_dir};./update.sh & disown",shell=True)
        # os.system(f'cd {config_dir};./update.sh &')

        
        subprocess.Popen(f"{config['HIDDIFY_CONFIG_PATH']}/update.sh",cwd=f"{config['HIDDIFY_CONFIG_PATH']}",start_new_session=True)
        return render_template("result.html",
                            out_type="success",
                            out_msg=_("Success! Please wait around 5 minutes to make sure everything is updated."),
                            log_path=url_for("admin.Actions:reverselog",logfile=f"update.log")
        )

        



    def update_usage(self):
        
        
        import json

        return render_template("result.html",
                            out_type="info",
                            out_msg=f'<pre class="ltr">{json.dumps(usage.update_local_usage(),indent=2)}</pre>',
                            log_path=None
        )
#واقعا برای 5 دلار میخوای کرک میکنی؟ حاجی ارزش وقت خودت بیشتره
#Email hiddify@gmail.com for free permium version. Do not crack this cheap product
