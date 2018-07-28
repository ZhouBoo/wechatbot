#coding=utf-8

from sqlalchemy import Column, String, ForeignKey,\
    DateTime, Integer, BigInteger, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import and_, func, create_engine
import datetime

Base = declarative_base()

engine = create_engine('sqlite:///shit-email.sqlite', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    
    __tablename__ = 'user'

    name = Column(String(50), primary_key=True)
    email = Column(String(40), unique=True)
    password = Column(String(40))
    sender = Column(Boolean, default=False)

    @staticmethod
    def create_user(name, email=None, password=None):
        """创建一个 user 如果必要的话，如果当前 user 已经存在，那么会更新不为空的信息。
        
        Arguments:
            name {string} -- 需要更新或者创建的用户
        
        Keyword Arguments:
            email {[string]} -- 263邮箱 (default: {None})
            password {[string]} -- 263邮箱密码 (default: {None})
        """
        user = session.query(User).filter(User.name==name).first()
        msg = u'创建或者更新异常'
        if user:
            if email:
                user.email = email
            if password:
                user.password = password
            session.commit()
            msg = u'更新成功'
        else:
            if email == None or password == None:
                msg = u'邮箱和密码不能为空'
            else:
                user = User(name=name, email=email, password=password)    
                session.add(user)
                session.commit()
                if user in session:
                    msg = u'用户 %s 创建成功' % name
                else:
                    msg = u'用户 %s 创建失败' % name
        return msg

    @staticmethod
    def sender_set_to(sender):
        """设置当前的 sender 为

        Arguments:
            sender {[string]} -- 当前的发送者的名字，也是即将被设置为邮件发送者

        Returns:
            [string] -- 设置的相关信息返回
        """
        maybe_sender = session.query(User).filter(User.name==sender).first()
        if maybe_sender:
            current_sender = session.query(User).filter(User.sender==True).first()
            msg = u''
            if current_sender:
                if current_sender.name == maybe_sender.name:
                    return u'你他mb的设置个毛啊，本来就是你'
                else:
                    current_sender.sender = False
                    msg += u'发送者 %s 已经被取消\n' % current_sender.name
            maybe_sender.sender = True
            msg += u'发送者 %s 已经被设置' % maybe_sender.name
            session.commit()
            return msg
        else:
            return u'都没注册信息，发送 nmb'

    @staticmethod
    def show_sender():
        """ 查询当前的邮件发送者是谁
        
        Returns:
            [string] -- 返回发送者的名字信息
        """
        user = session.query(User).filter(User.sender==True).first()
        if user:
            return u'当前发送者为 %s' % user.name
        else:
            return u'当前未设置发送者'

    @staticmethod
    def delete_user(name):
        user = session.query(User).filter(User.name==name).first()
        if user:
            session.delete(user)
            session.commit()
            return u'删除 %s 的用户成功' % name
        else: 
            return u'瞎删你mb'

    @staticmethod
    def user_exist(name):
        """查询指定用户是否存在
        
        Arguments:
            name {[string]} -- 查询的用户名，用户名在数据库中是唯一的，并且为微信名
        """
        user = session.query(User).filter(User.name==name).first()
        return u'叫 %s 的用户存在，邮箱为 %s，%s' % \
            (name, user.email, u'是发送者' if user.sender else u'不是发送者') \
            if user else u'叫 %s 的用户不存在' % name

    def __repr__(self):
        return '%s(%s)' % (self.name, self.email)
        

class Message(Base):

    __tablename__ = 'message'

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    sender = Column(String(50), ForeignKey('user.name'))
    message = Column(String(200))
    date_create = Column(DateTime, default=datetime.datetime.utcnow)

    @staticmethod
    def add_message(sender, message):
        m = Message(sender=sender, message=message)
        session.add(m)
        session.commit()
        if m in session:
            return u'添加成功'
        else:
            return u'添加记录失败'

    @staticmethod
    def update_message(id, sender, message):
        m = session.query(Message) \
                .filter(and_(Message.sender == sender, Message.id == id)) \
                .first()
        if m is None:
            return u'id = %s 的记录不存在' % id
        else:
            m.message = message
            session.commit()
            return u'记录更新成功，id 为 %s' % m.id

    @staticmethod
    def show_message(sender):
        today = func.DATE(Message.date_create) == datetime.date.today()
        s = ''
        for m in session.query(Message) \
                .filter(and_(Message.sender == sender, today)):
            s += 'id = %s, message = %s\n' % (m.id, m.message)
        
        return  u'今日无%s的记录' % sender if len(s) <= 0 else s       
    

Base.metadata.create_all(engine)