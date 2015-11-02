#!/usr/bin/env python

__author__ = 'dracks'
import sys
import re
import os
import argparse
import json


class GenLocales:
    def __init__(self):
        self.list_patterns = [
            re.compile(r"\{\{.*t [\"']([a-zA-Z\-\.]*)[\"']"),
            re.compile(r"I18n\.translationMacro\([\"']([a-zA-Z\-\.]*)[\"']"),
            re.compile(r"i18n\.t\([\"\']([a-zA-Z\-\.]*)[\"']"),
            re.compile(r"\"i18n[\"']\).t\([\"\']([a-zA-Z\-\.]*)[\"']"),
            re.compile(r"\ t\([\"\']([a-zA-Z\-\.]*)[\"']")
        ]
        self.new_line_pattern = re.compile(r"([\n|\r])^", re.MULTILINE)
        self.list_found = []

    def parse(self, filename, contents):
        def info(match):
            index = contents.find(match)
            line = len(self.new_line_pattern.findall(contents[:index])) + 1
            return filename, line, match

        for pattern in self.list_patterns:
            found = pattern.findall(contents)
            self.list_found.extend(map(info, found))

    def get_list(self):
        return self.list_found

    def get_dict(self):
        def set_value(d, filename, line, path, element):
            key = path[0]
            text = "found in: {filename} line: {line}".format(filename=filename, line=line)
            if len(path) == 1:
                old = d.get(key, None)
                if old is None:
                    d[key] = text
                elif isinstance(old, basestring):
                    d[key] = old + "\n" + text
                else:
                    raise Exception("repeated key:" + element)
            else:
                old = d.get(key, None)
                if isinstance(old, basestring):
                    raise Exception("repeated key" + element)
                else:
                    if old is None:
                        old = {}
                        d[key] = old
                    set_value(old, filename, line, path[1:], element)

        ret = {}
        for (filename, line, found) in self.list_found:
            path = found.split(".")
            set_value(ret, filename, line, path, found)

        return ret
        
    def get_plain_dict(self):
        r={}
        for (filename, line, found) in self.list_found:
            text = "found in: {filename} line: {line}".format(filename=filename, line=line)
            v= r.get(found, None)
            if v is None:
                r[found]=text
            else:
                r[found] += "\n"+text
        return r


class JsonOutput():
    def __init__(self, file_output, base=None):
        self.file_output=file_output
        if base is None:
            self.base={}
        else:
            self.base=base
            
    def save(self, data):
        def merge(base, data):
            ret = {}
            for key in data.keys():
                value = data[key]
                if isinstance(value, dict):
                    value=merge(base.get(key, {}), value)
                else:
                    value=base.get(key, value)
                ret[key]=value
            return ret
        output=merge(self.base, data)
        json.dump(output, self.file_output, sort_keys=True, indent=4)


def format(fp, output):
    output.save(json.load(fp))


def scan_folder(folder, output):
    generator = GenLocales()
    list_path = [folder]

    while len(list_path) > 0:
        path = list_path[0]
        list_path = list_path[1:]
        for filename in os.listdir(path):
            if filename[0] == '.':
                continue
            new_path = os.path.join(path, filename)
            if os.path.isdir(new_path):
                list_path.append(new_path)
            else:
                contents = open(new_path, 'r').read()
                generator.parse(new_path, contents)

    output.save(generator.get_plain_dict())


def main():
    parser = argparse.ArgumentParser(description="Tool to retrieve all the ")

    parser.add_argument('-f', default=None, help="format json", metavar=('file.json',))
    parser.add_argument('-m', default=None, help="Merge file", metavar=('origin.json',))
    parser.add_argument('-s', default=None, help="Search/scan for i18n usages on folder", metavar=('folder',))
    parser.add_argument('-o', default=None, help="Output file", metavar=('file.json',))

    args = parser.parse_args()

    if args.f and args.s:
        parser.error("Arguments -f and -s are not valid on the same call")

    elif not args.f and not args.s:
        parser.error('You should use the argument -f or -s')

    output = sys.stdout
    
    base=None
    if args.m:
        base = json.load(open(args.m))
        
    if args.o:
        output = open(args.o, 'w')
        
    output=JsonOutput(output, base)

    if args.f:
        format(open(args.f), output)

    if args.s:
        scan_folder(args.s, output)


if __name__ == '__main__':
    main()
