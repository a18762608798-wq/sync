wget -O Zotero.tar.x2 "https://www.zotero.org/download/client/dl?channel=release&platform=linux-x86_64"

tar -xJf Zotero.tar.xz

DIR="$(find "$HOME" -maxdepth 1 -type d -name 'Zotero*_linux-x86_64' | head -n 1)"

echo "$DIR"

sudo rm -rf /opt/zotero
sudo mv "$DIR" /opt/zotero

cd /opt/zotero
sudo ./set_launcher_icon

mkdir -p ~/.local/share/applications
ln -sf /opt/zotero/zotero.desktop ~/.local/share/applications/zotero.desktop

update-desktop-database ~/.local/share/applications 2>/dev/null || true
