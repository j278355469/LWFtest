
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from django.http import HttpResponseRedirect
from django .contrib.auth.decorators import login_required
# from django.shortcuts import render_to_response
from bs4 import BeautifulSoup

import pandas as pd
import requests
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import auth
import io
from LWF import store1
import threading
import schedule


# Create your views here.
conn = connection.cursor()

def dataCrawl(product):
    results = []
    pc24_thread = threading.Thread(target=store1.store().PC,args = (product,results))
    cf_thread = threading.Thread(target=store1.store().Carrefour,args = (product,results))
    momo_thread = threading.Thread(target=store1.store().momo,args = (product,results))
    poya_thread = threading.Thread(target=store1.store().Poya,args = (product,results))

    pc24_thread.start()
    cf_thread.start()
    momo_thread.start()
    poya_thread.start()
    pc24_thread.join()
    cf_thread.join()
    momo_thread.join()
    poya_thread.join()
    results_df=pd.DataFrame(results)
        
    results_df.index = results_df.index + 1
        # results_df = results_df.head(3)
            
    sorted_results_df = results_df.sort_values(by="price")
    sorted_dict=sorted_results_df.to_dict("records")

    return sorted_dict


def search(request):
    product=request.GET['product']
    results=dataCrawl(product)

    return render(request, "search.html", {'product':product,'results': results})
#首頁
def ex_index(request):
    
    user = request.user
    return render(request, "index.html", {"user": user})





