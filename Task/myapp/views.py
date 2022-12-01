from django.shortcuts import render, get_list_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from datetime import datetime
import os
from django.conf import settings

from os import listdir
from os.path import isfile, join
import csv
import pandas as pd



info = {
    "workbook": None,
    "worksheets": None,
    "cursheetname": None,
    "cursheet": None,
    "columns": None,
    "rows": None,
    "files": None,
    "file": None
}
files = None

excel_file = None
workbook = None
worksheets = None
cursheet = None
cursheetname = None
columns = None

# Create your views here.
def index(request):
    global info
    info["files"] = [f for f in listdir("static") if isfile(join("static", f))]

    context = {}

    context["worksheets"] = info["worksheets"]
    context["cursheetname"] = info["cursheetname"]
    context["columns"] = info["columns"]
    context["rows"] = info["rows"]
    context["files"] = info["files"]

    template = loader.get_template("index.html")
    return HttpResponse(template.render(context, request))

def selectFile(request, filename):
    global info
    # info["file"] = filename
    # info["workbook"] = openpyxl.load_workbook("static/" + filename)
    # info["worksheets"] = info["workbook"].sheetnames
    # info["cursheetname"] = info["worksheets"][0]
    # info["cursheet"] = cursheet = info["workbook"][info["cursheetname"]]
    columns = list()
    rows = list()

    cursheet = pd.read_csv("static/" + filename)
    header = cursheet.head()
    index = 0
    cursheet = cursheet.values.tolist()
    

    rows.append(header)

    

    for row in cursheet:
        temp_row = []
        for cell in row:
            if cell is None:
                temp_row.append('')
            else:
                temp_row.append(str(cell))
        if temp_row.count('') == len(temp_row):
            break
        else:
            rows.append(temp_row)
        index += 1

    info["columns"] = columns
    info["rows"] = rows

    return HttpResponseRedirect("/")
def filter(request, pa):
    # print(param)
    filename = pa.split(':')[0]
    keyword = pa.split(':')[1]

    global info
    # info["file"] = filename
    # info["workbook"] = openpyxl.load_workbook("static/" + filename)
    # info["worksheets"] = info["workbook"].sheetnames
    # info["cursheetname"] = info["worksheets"][0]
    # info["cursheet"] = cursheet = info["workbook"][info["cursheetname"]]
    columns = list()
    rows = list()

    cursheet = pd.read_csv("static/" + filename)
    header = cursheet.head()
    cursheet = cursheet.values.tolist()
    

    index = 0


    filtered_sheet = []
    
    for row in cursheet:
        contains = False
        for cell in row:
            if keyword in str(cell):
                contains = True
        if contains ==True:
            filtered_sheet.append(row)


        

    
    rows.append(header)
    for row in filtered_sheet:
        temp_row = []
        for cell in row:
            if cell is None:
                temp_row.append('')
            else:
                temp_row.append(str(cell))
        if temp_row.count('') == len(temp_row):
            break
        else:
            rows.append(temp_row)
        index += 1

    info["columns"] = columns
    info["rows"] = rows

    return HttpResponseRedirect("/")
def sort(request, pa):
    # print(param)
    filename = pa.split(':')[0]
    keyword = pa.split(':')[1]


    global info
    # info["file"] = filename
    # info["workbook"] = openpyxl.load_workbook("static/" + filename)
    # info["worksheets"] = info["workbook"].sheetnames
    # info["cursheetname"] = info["worksheets"][0]
    # info["cursheet"] = cursheet = info["workbook"][info["cursheetname"]]
    columns = list()
    rows = list()

    cursheet = pd.read_csv("static/" + filename)
    for column in cursheet.head():
        if keyword in column:
            keyword = column
    newsheet = cursheet.sort_values(keyword)
    header = cursheet.head()
    newsheet = newsheet.values.tolist()
    

    index = 0


    
    rows.append(header)
    for row in newsheet:
        temp_row = []
        for cell in row:
            if cell is None:
                temp_row.append('')
            else:
                temp_row.append(str(cell))
        if temp_row.count('') == len(temp_row):
            break
        else:
            rows.append(temp_row)
        index += 1

    info["columns"] = columns
    info["rows"] = rows

    print(type(HttpResponseRedirect("/")))

    return HttpResponseRedirect("/")

def edit(request, rowId):
    global info

    context = {}

    col = info["columns"]
    row = info["rows"][int(rowId)]

    cr = []
    for i in range(len(col)):
        cr.append([col[i], row[i]])

    context["rowId"] = rowId
    context["cr"] = cr

    template = loader.get_template("edit.html")
    return HttpResponse(template.render(context, request))

def modify(request):
    global info
    cursheet = info["cursheet"]
    row = int(request.POST["rowId"])
    columns = info["columns"]
    cursheet.insert_rows(row + 3)
    temp = list()
    for coli in range(len(columns)):
        cursheet.cell(row=row + 3, column=coli + 1).value = request.POST[columns[coli]]
        temp.append(request.POST[columns[coli]])
    info["rows"].insert(row + 1, temp)
    # info["workbook"].save("static/" + info["file"])
    return HttpResponseRedirect("/")

def download(request):
    global info
    if not os.path.isdir("temp"):
       os.mkdir("temp")
    info["workbook"].save("temp/modified_output.xlsx")
    file_path = os.path.join("temp/modified_output.xlsx")
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response

    raise "Http404"

