# set_up

## zotero

```bash
# download
cd ~/下载
wget -O Zotero.tar.x2 "<https://www.zotero.org/download/client/dl?channel=release&platform=linux-x86_64>"
tar -xJf Zotero.tar.xz

# install
DIR="./Zotero_linux-x86_64"
echo "$DIR"
sudo rm -rf /opt/zotero
sudo mv "$DIR" /opt/zotero
cd /opt/zotero
sudo ./set_launcher_icon

# desktop
mkdir -p ~/.local/share/applications
ln -sf /opt/zotero/zotero.desktop ~/.local/share/applications/zotero.desktop
update-desktop-database ~/.local/share/applications 2>/dev/null || true
```

## zotero connector

Ref to the web `https://www.zotero.org/download/`
