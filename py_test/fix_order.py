from ast import Or
import time
from datetime import datetime, timezone
from peewee import Model, MySQLDatabase, PrimaryKeyField, CharField, BigIntegerField, IntegerField, DoubleField, TimestampField, DateTimeField, TextField, FloatField, SQL
from multiprocessing import Pool
import json
import redis


# host = '10.0.1.50'
# user = 'mahjong'
# password = 'Mahjong#2021'
# db = 'game_test'
# charset = 'utf8mb4'

host = '172.16.1.208'
user = 'mahjong'
password = 'Mahjong2022'
db = 'game'
charset = 'utf8mb4'


# 定义数据库连接
database = MySQLDatabase(db, user=user, password=password, host=host, port=3306)


# 定义模型
class BaseModel(Model):
    class Meta:
        database = database
# 定义模型


class PurchaseOrder(BaseModel):
    database_id = BigIntegerField(primary_key=True)
    created_time = DateTimeField()
    cluster_id = IntegerField()
    account_id = BigIntegerField()
    character_id = BigIntegerField()
    platform_id = CharField()
    order_id = CharField()
    product_id = CharField()
    product_type = IntegerField()
    product_quantity = IntegerField()
    purchase_time = DateTimeField()
    purchase_time_ms = BigIntegerField()
    region_code = CharField()

    class Meta:
        db_table = 'purchase_order'


class Order(BaseModel):
    id = IntegerField(primary_key=True)
    transaction_id = CharField(max_length=36, default='', null=False, constraints=[SQL("COMMENT '事务id,来自支付服务'")])
    event_id = CharField(max_length=36, default='', null=False, constraints=[SQL("COMMENT '事件id,服务器生成'")])
    order_id = CharField(max_length=64, default='', null=False, constraints=[SQL("COMMENT '订单id,来自第三方'")])
    receipt = TextField(null=False, constraints=[SQL("COMMENT '支付凭证,客户端上传'")])
    signature = TextField(null=False, constraints=[SQL("COMMENT 'google凭证签名,客户端上传'")])
    product_id = CharField(max_length=128, null=False, constraints=[SQL("COMMENT '商品id'")])
    product = CharField(max_length=255, default='', null=False, constraints=[SQL("COMMENT '商品 做了转换的product_id'")])
    character_id = BigIntegerField(null=False, constraints=[SQL("COMMENT '角色id'")])
    real_price = IntegerField(null=False, constraints=[SQL("COMMENT '实付金额 分'")])
    show_price = IntegerField(null=False, constraints=[SQL("COMMENT '显示金额 分'")])
    currency = CharField(max_length=64, default='', null=False, constraints=[SQL("COMMENT '货币: USD/JPY/TWD/CNY'")])
    region = CharField(max_length=8, default='', null=False, constraints=[SQL("COMMENT '货币代码: US/JP/TW/CN'")])
    usd_price = IntegerField(null=False, constraints=[SQL("COMMENT '美元计价金额 分'")])
    vendor = CharField(max_length=10, default='', null=False, constraints=[SQL("COMMENT '支付渠道 google/apple'")])
    status = IntegerField(default=0, null=False, constraints=[SQL("COMMENT '订单状态 -1: 用户放弃支付 0: 未支付 1: 已支付 2: 已发货'")])
    created_at = BigIntegerField(null=False, constraints=[SQL("COMMENT '创建时间(秒)'")])
    updated_at = BigIntegerField(null=False, constraints=[SQL("COMMENT '更新时间(秒)'")])
    client_paid_at = BigIntegerField(default=0, null=False, constraints=[SQL("COMMENT '客户端通知支付的时间(秒) 还需验证'")])
    paid_at = BigIntegerField(default=0, null=False, constraints=[SQL("COMMENT '支付服务通知支付的时间(秒) 已验证'")])
    callback_ctx = TextField(default='{}', null=False, constraints=[SQL("COMMENT '回调上下文'")])
    os = CharField(max_length=64, default='', null=False, constraints=[SQL("COMMENT '客户端系统'")])
    version = CharField(max_length=64, default='', null=False, constraints=[SQL("COMMENT '客户端系统版本'")])
    ip = CharField(max_length=64, default='', null=False, constraints=[SQL("COMMENT '客户端ip'")])
    lang = CharField(max_length=64, default='', null=False, constraints=[SQL("COMMENT '客户端语言'")])
    item = CharField(max_length=255, default='', null=False, constraints=[SQL("COMMENT '商品 id1,1;id2,2'")])
    first_recharge_giveaway = IntegerField(default=0, null=False, constraints=[SQL("COMMENT '首充赠品的数量'")])
    normal_giveaway = IntegerField(default=0, null=False, constraints=[SQL("COMMENT '普通赠品的数量'")])
    sandbox = IntegerField(default=0, null=False, constraints=[SQL("COMMENT '是否是沙盒订单 0: 正式订单 1: 沙盒订单'")])
    adid = CharField(max_length=255, default='', null=False, constraints=[SQL("COMMENT '广告id'")])
    app_instance_id = CharField(max_length=255, default='', null=False, constraints=[SQL("COMMENT '应用实例id'")])
    cancel_reason = TextField(null=True, constraints=[SQL("COMMENT '取消订单原因'")])
    verify_times = IntegerField(default=0, null=True, constraints=[SQL("COMMENT '验证次数,默认0次'")])
    last_verify_time = BigIntegerField(default=0, null=True, constraints=[SQL("COMMENT '最后验证时间,默认0'")])
    steam_id = CharField(max_length=128, default='', null=True, constraints=[SQL("COMMENT 'steam id'")])
    triad_recharge_giveaway = FloatField(default=0, null=False, constraints=[SQL("COMMENT '赠品 第三方充值 赠送对应商品的数量'")])
    extra = TextField(null=True, constraints=[SQL("COMMENT '额外信息,用于存储购买类型和得到的物品'")])
    steam_lang = CharField(max_length=32, default='', null=True, constraints=[SQL("COMMENT 'steam language'")])
    steam_pay_type = IntegerField(default=0, null=True, constraints=[SQL("COMMENT '0: 应用支付, 1: web支付'")])

    class Meta:
        db_table = 'order'


class Character(BaseModel):
    database_id = PrimaryKeyField()
    parent_id = BigIntegerField()

    class Meta:
        db_table = 'character'


def fix():
    # select * from `order` where id>=58486 and id <= 62476  and status=2 and vendor='Steam' order by id asc;

    # query = Order.select().where(Order.id.between(3001, 3002) & (Order.status == 2) & (Order.vendor == 'Steam')).order_by(Order.id.asc())
    query = Order.select().where(Order.id.between(58486, 62476) & (Order.status == 2) & (Order.vendor == 'Steam')).order_by(Order.id.asc())
    for order in query:
        c = Character.get_or_none(Character.database_id == order.character_id)
        if not c:
            print(f"未找到 database_id={order.character_id} 的数据")
            continue

        PurchaseOrder.create(
            created_time=datetime.fromtimestamp(order.created_at, tz=timezone.utc),
            cluster_id=1,
            account_id=c.parent_id,
            character_id=order.character_id,
            platform_id=order.vendor,
            order_id=order.order_id,
            product_id=order.product_id,
            product_type=0,
            product_quantity=1,
            purchase_time=datetime.fromtimestamp(order.paid_at, tz=timezone.utc),
            purchase_time_ms=order.paid_at * 1000,
            region_code=order.region
        )


if __name__ == '__main__':
    fix()
