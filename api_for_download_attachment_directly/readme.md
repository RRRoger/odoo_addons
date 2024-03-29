# api_for_download_attachment_directly

> 下载附件免登陆 / Download Attachment Without Login Odoo

<div align=center>
  <img src="static/description/icon.png" width="80"/>
</div>

### 1. Usage / 如何使用?

> Download the avatar of the partner whose id is 999 

```python
# when you use api
from odoo.http import request
attachment_factory_obj = request.env['attachment.factory']

# Or Other
# attachment_factory_obj = self.env['attachment.factory']

model = "res.partner"
res_id = 999
model_field = "avatar"
filename_field = "avatar_name"
note = "download avatar of partner"

af = attachment_factory_obj.create({
    "model": model,
    "res_id": res_id,
    "model_field": model_field,
    "filename_field": filename_field,
    "note": note,
})

# you will get a file_url and a filename

# file url like: http://localhost:8069/web/download/attachment/1babc64e-6e99-4934-bc84-28263a0fdd88
# Open your browser with this URL and download it directly
file_url = af.url

# file name like: xxx.jpg
filename = af.filename
```

### 2. Automatically delete out-of-date data / 删除失效的数据

> code in `api_for_download_attachment_directly/data/data.xml`
>
> delete 7 days ago temporary data

```xml
<record id="cron_delete_expired_data" model="ir.cron">
    <field name="name">[Download Attachment] 删除失效的数据</field>
    ...
</record>
```
