# DDL Maker

A simple Python code to make it easier to create DDL's. This project serves as a training to Git as well.

## Table of contents
* [Introduction](#introduction)
* [Features](#features)
* [Status](#status)
* [Example](#example)

## Introduction

This is a simple code to create DDL's using the field list used in object ingestion. Instead of rewriting everything from the \_config.yml file, all you have to do is copy it and paste it as is, (e.g., "field1", "field2", "field3") and this script will do the rest. Given the variety of different properties a table can have the scope of this script is very limited, at least for now. I'm aiming to make it more dynamic and even able to create the tables themselves instead of only generating the DDL for them.

## Features

- Easily create DDL's
* Reuses what is already written
+ Yes I'm just testing out some Markdown things here

## Status

- Base code already working
- Can already be used to create some basic DDL's

**To Do:**

- Implement more DDL options
- Make the script capable of creating the tables
- A graphical interface just because


## Example

**Example of an input:**

<>![Input example](./images/input_example.png)

___________________________________

**Generated DDL from the input:**
<>![DDL Output Example](./images/DDL_example.png)

___________________________________


**Generated query to transfer data from external to internal table:**
<>![Generated Query Example](./images/query_example.png)

___________________________________
