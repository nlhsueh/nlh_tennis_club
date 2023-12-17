# version Static

加上 static files, 例如 .css, .js, images 等靜態檔案。路徑要對，程式才能抓得到

## Steps
* 在專案目錄下新增 [/static](/static) 目錄，裡面再新增 css, js, img 等目錄
  * 放一些圖片，和設定檔到適當的目錄下
* 到 [/my_tennis_club/settings.py](/my_tennis_club/settings.py) 下找到 `STATIC_URL` 的設定，在下方新增：
```python
STATICFILES_DIRS = [BASE_DIR / "static"]
```
* 引用這些檔案：
  * 