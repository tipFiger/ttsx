# Generated by Django 2.0.7 on 2019-05-10 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='pay_status',
            field=models.CharField(choices=[('WAIT_BUYER_PAY', '交易创建'), ('TRADE_FINISHED', '交易结束'), ('paying', '待支付'), ('TRADE_SUCCESS', '成功'), ('TRADE_CLOSE', '交易关闭')], default='paying', max_length=20, verbose_name='交易状态'),
        ),
    ]
