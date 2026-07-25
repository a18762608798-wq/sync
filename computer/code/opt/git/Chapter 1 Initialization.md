# 1 the initialization of git

## 1.1 Installation

* config info

Generally, we use apt:

```bash
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:git-core/ppa
sudo apt update
sudo apt install -y \
  git \
  build-essential
```

<https://gitforwindows.org/>

Notice choose main chain name: main.

## 1.2 Git config

* config info

```bash
git config --global user.name "git_usr"
git config --global user.email "a18762608798@petalmail.com"
```

* check

```bash
# 查询全局用户名
git config --global user.name

# 查询全局邮箱
git config --global user.email
```
