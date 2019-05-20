from django import forms
from django.contrib import auth

from user.models import User


# 注册验证
class RegisterForm(forms.Form):
    username = forms.CharField(required=True, max_length=20, min_length=5,
                               error_messages={
                                   'required': '参数必填',
                                   'max_length': '最长不超过20字符',
                                   'min_length': '最小不少于5字符',
                               })

    password = forms.CharField(required=True, max_length=20, min_length=8,
                               error_messages={
                                   'required': '参数必填',
                                   'max_length': '最长不超过20字符',
                                   'min_length': '最小不少于8字符',
                               })

    cpwd = forms.CharField(required=True, max_length=20, min_length=8,
                           error_messages={
                               'required': '参数必填',
                               'max_length': '最长不超过20字符',
                               'min_length': '最小不少于8字符',
                           })




    def clean(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError({'username': '注册账号已经存在'})
        print('1')

        password = self.cleaned_data.get('password')
        cpwd = self.cleaned_data.get('cpwd')
        if password != cpwd:
            raise forms.ValidationError({'cpwd': '两次密码不一致'})
            print('2')


        return self.cleaned_data



# 登录验证

class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=20, min_length=5,
                               error_messages={
                                   'required': '参数必填',
                                   'max_length': '最长不超过20字符',
                                   'min_length': '最小不少于5字符',
                               })

    password = forms.CharField(required=True, max_length=20, min_length=8,
                               error_messages={
                                   'required': '参数必填',
                                   'max_length': '最长不超过20字符',
                                   'min_length': '最小不少于8字符',
                               })

    def clean_username(self):
        # 校验某个字段，返回校验字段的值
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('登录账号不存在，请去注册')
        return self.cleaned_data.get('username')



class UserAddressForm(forms.Form):
    signer_name = forms.CharField(required=True,
                                  error_messages={
                                      'required': '收件人必填'
                                  })
    address = forms.CharField(required=True,
                              error_messages={
                                  'required': '必填'
                              })
    postcode = forms.CharField(required=True,
                               error_messages={
                                   'required': '邮编必填'
                               })
    mobile = forms.CharField(required=True,
                             error_messages={
                                 'required': '手机必填'
                             })