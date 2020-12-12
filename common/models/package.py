# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


from application import app,db
from common.models.member import Member

class Package(db.Model):
    __tablename__ = 'package'

    packageid = db.Column(db.String(20, 'utf8mb4_0900_as_ci'), primary_key=True, server_default=db.FetchedValue(), info='????')
    mid = db.Column(db.ForeignKey('member.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, info='???')
    fromaddress = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue(), info='????')
    toaddress = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue(), info='????')
    frommobile = db.Column(db.String(11, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='????')
    price = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='??')
    insurance = db.Column(db.Integer, server_default=db.FetchedValue(), info='??')
    weight = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='????')
    remark = db.Column(db.String(200), server_default=db.FetchedValue(), info='??')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='????')
    tomobile = db.Column(db.String(11), nullable=False)
    fromname = db.Column(db.String(10), nullable=False)
    toname = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(1), nullable=False)
    member = db.relationship('Member', primaryjoin='Package.mid == Member.id', backref='packages')

    @property
    def id_nickname(self):
        nickname = Member.query.filter_by(id=str(self.mid)).first().nickname
        # print("+++++++++++++++++++++++++++")
        # print(nickname)
        return nickname