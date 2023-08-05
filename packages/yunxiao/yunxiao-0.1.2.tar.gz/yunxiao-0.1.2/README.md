# YunXiao API
An API tool for YunXiao Education Institution Management System.

# Copyright Statement
YunXiao software is owned by XiaoGuanJia. This project is for learning purposes only. If there is any infringement, please contact me to delete.

# Contact
admin@sqkkyzx.com

# Usage Example
```
from yunxiao.app improt App, Report

app = App("123456","pwd123456",[])

r = Report(app).find_now_data_report()

pritnt(r["data"])

```