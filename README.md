# Scan-Ember-i18n-tags-usage
It's a tool to scan in all files of a project all the usages of i18n tags. 

It search for instructions like
* i18n.t("key",...): when I should use more than a time, the i18n package inside the same function i make a variable with i18n. 
* this.get("i18n").t("key",...
* {{t "key"...}}
* I18n.translationMacro("key", ...): When initializing some variables, It requires to import ember-i18 as I18n on the file. 

The tool is based on the idea in Xcode tool genstrings to generate a file with all the strings requests in a sourcefile

## Usage
### Scan project
The main feature of this script is to scan all the files in a project, to get all translation keys used in the project 
and generate a json with that. By default, It will throw the output via the stdout, but you can select a file to save 
the generated json. 

The usage was:
```BASH
$PATH_SCRIPT/gen_locales.py -s app 
```

The $PATH_SCRIPT is the path where you put this script, I recommend to put in a folder that was inside your path, to 
call it everywhere. 

It will output something like:

```JSON
{
    "key1":{
        "subkey1": "Found in: app/file1.js line: 12",
        "subkey2": "Found in: app/file1.js line: 6\nFound in: app/templates/form.hbs line: 34"
     },
     "key2": "Found in: app/templates/application.hbs line 5"
}
```

### Reformat json  
As the json was generated automatically, it means the keys were sorted. This is to transform an old json, to a sorted 
json to improve the usage when you have a project with a manual localization file, to ensure the sort of keys was the same 
as the generated file by this tool. To use this simple feature run as:

```BASH
$PATH_SCRIPT/gen_locales.py -f old_translations.json
```


## TO-DO
 * Add the option to generate a ember-cli file with the translations. 