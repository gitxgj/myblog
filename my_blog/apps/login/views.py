from django.http import HttpResponse
from django.shortcuts import render, redirect
from QQLoginTool.QQtool import OAuthQQ
from django.views import View
# Create your views here.

app_id = "101853453"
client_id = "7b4d2f3ca899b12db236952b9818c497"
redirect_uri = "http://www.ccmsy.com:8000/auth_callback"

class QQAutoView(View):
    def get(self, request):


        auth = OAuthQQ(
            client_id=app_id, client_secret=client_id, redirect_uri=redirect_uri,
        )
        login_url = auth.get_qq_url()
        print(login_url)

        return redirect(login_url)




