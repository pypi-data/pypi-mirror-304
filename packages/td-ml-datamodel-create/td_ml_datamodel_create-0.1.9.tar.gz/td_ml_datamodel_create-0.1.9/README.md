# td-ml-datamodel-create

## Introduction

This Python Library allows you to define the main JSON params of a Treasure Insights Datamodel in a `config.json` file inside a ***Treasure Workflow Project*** and build datamodel automatically via API.


## Inputs

* `config.json`: the file that contains the needed params for Python code to read from and build the TI Datamodel. See below:

```
{
## -- (name of datamodel)
"model_name":  "datamodel_automated" 
,
## -- (list of tables to be added to datamodel)
"model_tables": [
  {"db":"sink_database","name":"table_1"},
  {"db":"sink_database","name":"table_2"}
                ] 
,
## -- (list of users to share datamodel with)
"shared_user_list": ["ENTER EMAIL HERE","ENTER EMAIL HERE"] 
,
## -- (list of columns you want to change datatype from raw table to datamodel. Ex. in "date" you provide column names that will be converted to `datetime`)
"change_schema_cols": {"date": ["ENTER_NAME"], "text": ["ENTER_NAME"], "float": ["ENTER NAME"], "bigint": ["ENTER NAME"]}
, 
## -- (if any joins were required you can add a list of table_name:join_key pairs)
"join_relations": {"pairs":
[ 
  {"db1": "sink_database", "tb1":"table_1","join_key1":"user_id","db2": "sink_database","tb2":"table_2","join_key2":"user_id"},
  {"db1": "sink_database", "tb1":"table_1","join_key1":"date","db2": "sink_database","tb2":"table_2","join_key2":"date"}
]
                  }
}
```

* `input_params.yml`: The `create_datamodel.py` file requires also the four params below, which are being defined in the main workflow `YAML` file and imported into Custom Scripting as `_env variables`.

##### Declare ENV Variables from YML file
- **apikey** = os.environ['TD_API_KEY'] 
- **tdserver** = os.environ['TD_API_SERVER']
- **sink_database** = os.environ['SINK_DB']
- **output_table** = os.environ['OUTPUT_TABLE']

`Copyright © 2022 Treasure Data, Inc. (or its affiliates). All rights reserved`


