from django.shortcuts import render, redirect
from pred_app.lstm_prediction import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import json

from pandas_datareader import data as pdr
import datetime
import yfinance as yf
yf.pdr_override()
import pandas as pd

# --------------- MAIN WEB PAGES -----------------------------
@login_required(login_url="login")
def redirect_root(request):

    return redirect('/pred_app/index')


@login_required(login_url="login")
def index(request):
	pop_stocks = PopularStock.objects.values()
	tickers_list = [p['symbol'] for p in pop_stocks]
	today = datetime.date.today()
	yesterday = today - datetime.timedelta(days=1)

	for i in range(len(tickers_list)):
		datass = pdr.get_data_yahoo(tickers_list[i], start=yesterday, end=yesterday)
		print(datass)
		price = round(datass.iloc[0]['Close'], 2)
		pop_stocks[i]['price'] = price

	if request.method == "POST":
		form = popularStockForm(request.POST)
		if form.is_valid():
			instance = form.save()
			return redirect('index')
		else:
			print(form.errors)

	context = {}
	context['pop_stocks'] = pop_stocks

	return render(request, 'pred_app/index.html', context)

@login_required(login_url="login")
def remove_pop(request, id):
	instance = PopularStock.objects.get(id=id)
	instance.delete()
	return redirect('index')

@login_required(login_url="login")
def pred(request):
    return render(request, 'pred_app/prediction.html')

@login_required(login_url="login")
def contact(request):
	return render(request, 'pred_app/contact.html')

@login_required(login_url="login")
def search(request, se, stock_symbol):
	import json
	predicted_result_df = lstm_prediction(se, stock_symbol)
	return render(request, 'pred_app/search.html', {"predicted_result_df": predicted_result_df})
# -----------------------------------------------------------
#-------- stock market simulator ---------------

def login_view(request):
	logout(request)
	form = LoginForm(request.POST or None)

	msg = None

	if request.method == "POST":

		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect("dashboard")
			else:
				msg = 'Invalid credentials'
		else:
			msg = 'Error validating the form'

	return render(request, "pred_app/login.html", {"form": form, "msg": msg})


def signup(request):
	logout(request)
	msg     = None
	success = False

	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get("username")
			raw_password = form.cleaned_data.get("password1")
			user = authenticate(username=username, password=raw_password)

			msg     = 'User created - please <a href="/login">login</a>.'
			success = True

			return redirect("login")

		else:
			msg = form.errors
	else:
		form = SignUpForm()

	return render(request, "pred_app/signup.html", {"form": form, "msg" : msg, "success" : success })

def logout_view(request):
	logout(request)
	return redirect('login')


@login_required(login_url="login")
def dashboard(request):
	portfolio = Portfolio.objects.get(user=request.user)
	context = {}
	if request.method == "POST":
		portfolio.balance += float(request.POST['balance'])
		portfolio.save()

	context['portfolio'] = portfolio

	return render(request, 'pred_app/dashboard.html', context)

@login_required(login_url="login")
def transactions(request):
	data = Transaction.objects.filter(user=request.user)
	context = {}

	context['data'] = data

	return render(request, 'pred_app/transactions.html', context)

@login_required(login_url="login")
def sell_stock(request):
	msg = None

	if request.method == "POST":
		portfolio = Portfolio.objects.get(user=request.user)
		b_before = round(portfolio.balance,2)
		remaining = round(portfolio.balance + float(request.POST['price']) * float(request.POST['quantity']),2)
		form = portfolioForm({'balance': remaining, 'user': request.user}, instance=portfolio)
		if form.is_valid():
			instance = form.save()
			postdata = request.POST.copy()
			postdata['user'] = request.user

			instance2 = holdings.objects.get(name=postdata['name'], user=postdata['user'])
			form = holdingsForm({'name': instance2.name, 'symbol': instance2.symbol,
								 'quantity': instance2.quantity - int(postdata['quantity']), 'user': instance2.user},
								instance=instance2)

			if form.is_valid():
				instance = form.save()
				postdata['type'] = 'Sell'
				postdata['balance_before'] = b_before
				postdata['balance_after'] = remaining
				form = transactionsForm(postdata)
				if form.is_valid():
					instance = form.save()
					msg = "You have sold the stock successfully"
				else:
					msg = form.errors

		else:
			msg = form.errors

	data = holdings.objects.filter(user=request.user, quantity__gt=0).values()
	context = {}
	tickers_list = [d['symbol'] for d in data]
	today = datetime.date.today()
	# yesterday = today - datetime.timedelta(days=1)

	for i in range(len(tickers_list)):
		datass = pdr.get_data_yahoo(tickers_list[i], start=today, end=today)
		price = round(datass.iloc[0]['Close'], 2)
		data[i]['price'] = price

	print(tickers_list)


	context['data'] = data
	context['msg'] = msg
	return render(request, 'pred_app/sell_stock.html', context)



@login_required(login_url="login")
def buy_stock(request):
	file = open("pred_app/static/pred_app/data/stock2.json")
	data = json.load(file)
	context = {}
	data = data [0:50:2]

	tickers_list = [d['slug'] for d in data ]
	today = datetime.date.today()
	yesterday = today - datetime.timedelta(days=1)

	for i in range(len(tickers_list)):
		datass = pdr.get_data_yahoo(tickers_list[i], start=yesterday, end=yesterday)
		price = round(datass.iloc[0]['Close'], 2)
		data[i]['price'] = price

	print(tickers_list)
	msg = None

	if request.method == "POST":
		portfolio = Portfolio.objects.get(user=request.user)
		b_before = portfolio.balance
		remaining = portfolio.balance - float(request.POST['price'])*float(request.POST['quantity'])
		form = portfolioForm({'balance':remaining, 'user':request.user},instance=portfolio)
		if form.is_valid():
			instance = form.save()
			postdata = request.POST.copy()
			postdata['user'] = request.user
			try:
				instance2 = holdings.objects.get(name=postdata['name'], user=postdata['user'])
				form = holdingsForm({'name':instance2.name, 'symbol':instance2.symbol,
									 'quantity':postdata['quantity']+instance2.quantity, 'user':instance2.user},instance=instance2)
			except Exception as e:
				form = holdingsForm(postdata)
			if form.is_valid():
				instance = form.save()
				postdata['type'] = 'buy'
				postdata['balance_before'] = b_before
				postdata['balance_after'] = remaining
				form = transactionsForm(postdata)
				if form.is_valid():
					instance = form.save()
					msg = "You have purchased the stock successfully"
				else:
					msg = form.errors

		else:
			msg = form.errors

	context['data'] = data
	context['msg'] = msg
	return render(request, 'pred_app/buy_stock.html', context)


