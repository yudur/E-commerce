from django.shortcuts import render
from django.views import View
from django.http import HttpResponse


class Pay(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Pay')


class SaveOrder(View):
    def get(self, *args, **kwargs):
        return HttpResponse('CloseOrder')


class Details(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Details')
