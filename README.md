# 

_List all AWS resources in the account for the specified credentials and generate a csv file._

## Starting 🚀

_Helps you filter AWS account resources by comparing stack TAGS with those provided by the console._


### Pre requisites 📋

_Make sure you have the necessary libraries to run it_

```cmd
pip install -r requirements.txt
```

### Set up & Usage 🔧

_To execute the module you must declare the initial statement as follows:_

```cmd
python __main__.py --tags="stage:uat" --aws-access-key-id="
DUMMY_ACCES_KEY" --region="us-east-1"
```

_Then it'll request the secret key as follows:_
```
aws-secret-access-key: **********
```

_At the end of execution you'll get a csv file named "stack_inventory"._

## Built with 🛠️

* [Python]() - Code

## Contributing 🖇️
💤

## Wiki 📖
💤

## Versioning 📌
💤

## Authors ✒️

* **jprugo** - *Owner* - [jprugo]

Look at the people [contributors]() who have participated in this project.