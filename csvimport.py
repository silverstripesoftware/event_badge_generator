#
# Unicode CSV import
#
# Source: Silver Catalyst
# 
# This is a wrapper around the csv module in Python's standard library to
# enable reading and parsing of csv files with unicode data. Supports
# basic autodetection of the feed encoding for UTF-8, UTF-16LE, UTF-16BE
# and Latin-1 (fallback default)
#
# Also uses a naive method of determining whether the files is comma 
# separated or tab separated by searching the file for a tab character
#

import csv

def getEncoding(data):
    if data.startswith("\xfe\xff"):
        return "utf-16-be-bom"
    if data.startswith("\xff\xfe"):
        return "utf-16-le-bom"
    if data[0] == "\x00" and data[1] != "\x00":
        return "utf-16-be"
    if data[0] != "\x00" and data[1] == "\x00":
        return "utf-16-le"
    try:
        unicode(data, 'utf-8')
    except UnicodeDecodeError:
        try:
            unicode(data, 'latin-1')
            return "latin-1"
        except UnicodeDecodeError:
            return "unknown"
    return "utf-8"

def convertDataToUtf8(data):
    encoding = getEncoding(data)
    if encoding == "utf-16-be-bom":
        unicodeData = unicode(data[2:], "utf-16-be")
    elif encoding == "utf-16-le-bom":
        unicodeData = unicode(data[2:], "utf-16-le")
    else:
        unicodeData = unicode(data, encoding)
    return unicodeData.encode('utf-8')

def getDelimiter(data):
    if data.find("\t") >= 0:
        return "\t"
    else:
        return ","

class CsvRow(object):
    def __init__(self, data, aliasMap):
        self.data = data
        self.alias = aliasMap
        
    def getData(self):
        return self.data
    
    def __getattr__(self, attr):
        if attr in self.alias:
            return self.data[self.alias[attr]]
        return None

class CsvReader(object):
    def __init__(self, data):
        self.numColumns = 0
        self.data = []
        self.alias = {}
        self.parse(data)

    def parse(self, data):
        data = convertDataToUtf8(data)
        lines = data.split("\n")
        reader = csv.reader(lines, delimiter=getDelimiter(data))
        for row in reader:
            numCols = len(row)
            if numCols > self.numColumns:
                self.numColumns = numCols
            if numCols > 0:
                self.data.append([unicode(cell, "utf-8") for cell in row])
        for row in self.data:
            if len(row) < self.numColumns:
                diff = self.numColumns - len(row)
                row.extend([None] * diff)
        
    def getNumColumns(self):
        return self.numColumns
    
    def getData(self):
        return self.data
    
    def setColumnAlias(self, col, alias):
        self.alias[alias] = col

    def getRow(self, row):
        return CsvRow(self.data[row], self.alias)

    def rows(self):
        for row in self.data:
            yield CsvRow(row, self.alias)
        
    