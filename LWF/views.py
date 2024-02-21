
from django.shortcuts import render, redirect
from django.db import connection

from LWF import store1
import threading



# Create your views here.
conn = connection.cursor()

def dataCrawl(product):
    results = []
    store1.store().PC(product,results)
    store1.store().Carrefour (product,results)
    store1.store().momo(product,results)
    store1.store().Poya(product,results)

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





