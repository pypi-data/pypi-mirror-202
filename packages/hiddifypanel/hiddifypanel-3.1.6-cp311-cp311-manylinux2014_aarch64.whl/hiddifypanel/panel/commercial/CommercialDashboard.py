from flask_admin.base import AdminIndexView,expose
from hiddifypanel.panel.hiddify  import admin
from flask import render_template,url_for,Markup,request
from flask_babelex import lazy_gettext as _
from hiddifypanel.panel import hiddify
import datetime
from flask_classful import FlaskView,route
from hiddifypanel.models import *
from hiddifypanel.panel.database import db
from hiddifypanel.panel.hiddify import flash
class CommercialDashboard(FlaskView):
    def index(self):
        return  ""
        bot=None
        # if hconfig(ConfigEnum.license):
        from hiddifypanel.panel.telegrambot import bot
            
        if hconfig(ConfigEnum.is_parent):
            childs=Child.query.filter(Child.id!=0).all()
            for c in childs:
                c.is_active=False
                for d in c.domains:
                    if d.mode==DomainType.fake:continue
                    remote=f"https://{d.domain}/{hconfig(ConfigEnum.proxy_path,c.id)}/{hconfig(ConfigEnum.admin_secret,c.id)}"
                    d.is_active= hiddify.check_connection_to_remote(remote)
                    if d.is_active:
                        c.is_active=True
            
            return render_template('parent_dash.html',childs=childs,bot=bot)
    # try:
        def_user=None if len(User.query.all())>1 else User.query.filter(User.name=='default').first()
        domains=get_panel_domains()
        sslip_domains=[d.domain for d in domains if "sslip.io" in d.domain]

        if def_user and sslip_domains:
            quick_setup=url_for("admin.QuickSetup:index")
            flash((_('It seems that you have not setup the system completely. <a class="btn btn-success" href="%(quick_setup)s">Click here</a> to complete setup.',quick_setup=quick_setup)),'warning')
        elif len(sslip_domains):
            flash((_('It seems that you are using default domain (%(domain)s) which is not recommended.',domain=sslip_domains[0])),'warning')
        elif def_user:
            d=domains[0]
            u=def_user.uuid
            flash((_('It seems that you have not created any users yet. Default user link: %(default_link)s',default_link=hiddify.get_user_link(u,d))),'secondary')
        
    # except:
    #     flash((_('Error!!!')),'info')
        h24=datetime.datetime.now()-datetime.timedelta(days=1)
        onlines=User.query.filter(User.last_online>h24).count()
        total=User.query.count()
        return render_template('index.html',onlines=onlines,total_users=total,bot=bot)

    @route('remove_child', methods=['POST'])
    def remove_child(self):
        child_id=request.form['child_id']
        child=Child.query.filter(Child.id==child_id).first()
        db.session.delete(child)
        db.session.commit()
        flash(_("child has been removed!"), "success")
        return self.index()#واقعا برای 5 دلار میخوای کرک میکنی؟ حاجی ارزش وقت خودت بیشتره
#Email hiddify@gmail.com for free permium version. Do not crack this cheap product
