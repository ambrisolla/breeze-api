from __main__ import app
from lib.budget import Budget
from flask import request


@app.route('/api/v1/budget/category', methods=['GET'])
def budget_category():
  budget_category = Budget().Category()
  res = budget_category.get()
  return res

@app.route('/api/v1/budget/category/add', methods=['POST'])
def budget_category_add():
  budget_category = Budget().Category()
  res = budget_category.add()
  return res

@app.route('/api/v1/budget/category/delete', methods=['POST'])
def budget_category_delete():
  budget_category = Budget().Category()
  res = budget_category.delete()
  return res


@app.route('/api/v1/budget', methods=['GET'])
def budget():
  budget = Budget()
  res = budget.get()
  return res

@app.route('/api/v1/budget/add', methods=['POST'])
def budget_add():
  budget = Budget()
  res = budget.add()
  return res

