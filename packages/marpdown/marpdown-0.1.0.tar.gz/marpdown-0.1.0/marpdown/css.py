BASE = '''footer {
    font-family: 'Arial', sans-serif; /* 设置字体 */
    font-size: 14px; /* 设置字体大小 */
    /* font-weight: bold; 设置字体粗细 */
    color: #333; /* 设置字体颜色 */
  }
  section {
    display: flex;
    justify-content: flex-start;
    align-items: flex-start;
    text-align: left;
    font-size: 14px; /* 设置字体大小 */
  }
  h1 {
    color: #000; /* 设置h1的字体颜色为黑色 */
    font-size: 30px; /* 设置字体大小 */
  }

  h2 {
    color: #0065bd; /* 设置h2的字体颜色为#0065bd */
    font-size: 20px; /* 设置字体大小 */
  }

  h3 {
    color: #0065bd; /* 设置h2的字体颜色为#0065bd */
    font-size: 25px; /* 设置字体大小 */
  }

  h4 {
    color: #000; /* 设置h2的字体颜色为#0065bd */
    font-size: 20px; /* 设置字体大小 */
  }'''
  
TIMELINE = '''.timeline {
  list-style: none;
  padding: 0;
  position: relative;
}

.timeline::before {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  left: 30px;
  width: 4px;
  background: #0065bd;
}

.timeline-item {
  padding: 20px 0;
  position: relative;
}

.timeline-marker {
  position: absolute;
  left: 26px;
  width: 12px;
  height: 12px;
  background: #0065bd;
  border-radius: 50%;
}

.timeline-content {
  padding-left: 60px;
}'''

TOC = '''.highlight-wrapper {
    margin-bottom: 1.25em; /* 添加底部边距，可根据需要调整 */
  }

   .highlight-container {
    position: absolute;
    left: 0;
    right: 0;
    background-color: #0065bd; /* 设置背景颜色为蓝色 */
    padding-left: 3.17em; /* 添加左边距，可根据需要调整 */
    padding-top: 0.2em; /* 添加左边距，可根据需要调整 */
    padding-bottom: 0.2em; /* 添加左边距，可根据需要调整 */
    display: flex; /* 设置为弹性布局 */
    align-items: center; /* 垂直居中 */
    height: 1.5em; /* 设置容器高度 */
  }
  
  .highlight {
    color: #ffffff; /* 设置字体颜色为白色 */
    margin: 0; /* 移除默认的margin */
  }'''

def load_css():
    tmp = [BASE,TOC,TIMELINE]
    return '\n'.join(tmp)