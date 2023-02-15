# news-manager

## Introduction

This is a news management system runs in command prompt. Each user is assigned as an editor or an administrator.
As an editor, he can publish and edit news through the system. On the other hand, as an administrator, 
His job is to approve the news or delete the news. He can also manage the users. 
For example, he can add users, modify users and delete users. This system is programmed in Python and 
implement the DAO Design Pattern.


## Tech stack
### Programming language - Python
### DataBases - MySql
    General information of users and news are stored in MySql.
### DataBases - MongoDB
    Large text, such as the contents of the news are stored in MongoDB.
### DataBases - Redis
    Approved news will be cached in redis. 
    For normal news, it will noly be cached for the first 24 hours.
    While Top news will be cached always.

