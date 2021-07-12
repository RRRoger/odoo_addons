# Api For Downloading Attachment Directly Without Login Odoo

<div align=center>
  <img src="static/description/icon.png" width="80"/>
</div>

### 1. 下载附件免登陆 / Download Attachment Without Login Odoo

```python
attachment_factory_obj = self.env['attachment.factory']

# Or when you use api
# from odoo.http import request
# attachment_factory_obj = request.env['attachment.factory']

model = ""
res_id = ""
model_field = ""
filename_field = ""
note = ""

attachment_factory = attachment_factory_obj.create({
    "model": model,
    "res_id": res_id,
    "model_field": model_field,
    "filename_field": filename_field,
    "note": note,
})

# file url
# like: http://localhost:8069/web/download/attachment/1babc64e-6e99-4934-bc84-28263a0fdd88
file_url = attachment_factory.url

# file name
filename = attachment_factory.filename
```

