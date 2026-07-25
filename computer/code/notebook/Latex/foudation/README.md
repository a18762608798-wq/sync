## 首选项：

### 中文

```latex
\usepackage{fontspec}
\setmainfont{NotoSerifCJK-Regular.ttc}[
  Path=/usr/share/fonts/opentype/noto/,
  Extension=.ttc
]

% 页面边距
\usepackage[a4paper, margin=2.5cm]{geometry}

% 行间距
\usepackage{setspace}
\onehalfspacing  % 1.5倍行距

% 段落缩进
\setlength{\parindent}{1em}

% 段落间距
\setlength{\parskip}{1ex plus 0.5ex minus 0.2ex}

% 页眉页脚
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhead{} % 清除所有页眉文字
\fancyfoot{} % 清除所有页脚文字
\fancyhead[C]{我的文档标题} % 在页眉中间位置添加文字
\fancyfoot[C]{\thepage} % 页码居中显示在页脚
\renewcommand{\headrulewidth}{0pt} % 页眉下划线宽度
\renewcommand{\footrulewidth}{0pt} % 页脚上划线宽度
```

### 英文

```latex
\usepackage{fontspec}

\setmainfont{Times New Roman}[
  Path = /home/hanyijie/Synchronous_space/computer/fonts/En/Times_New_Roman/, % Ensure the path is correct
  UprightFont = times,  % Specify the regular font
  BoldFont = timesbd,  % Specify the bold font
  ItalicFont = timesi,  % Specify the italic font
  BoldItalicFont = timesbi,  % Specify the bold italic font
  Extension = .ttf  % Specify the file extension
]

\usepackage[a4paper, margin=2.5cm]{geometry}
\usepackage{setspace}
\setlength{\parindent}{1em}
\setlength{\parskip}{1ex plus 0.5ex minus 0.2ex}

\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhead{} % Clear all header text
\fancyfoot{} % Clear all footer text
\fancyhead[C]{My Document Title} % Add text in the center of the header
\fancyfoot[C]{\thepage} % Center the page number in the footer
\renewcommand{\headrulewidth}{0pt} % Header underline width
\renewcommand{\footrulewidth}{0pt} % Footer underline width

```

