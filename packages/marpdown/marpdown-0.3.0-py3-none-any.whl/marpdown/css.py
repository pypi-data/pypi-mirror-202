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

TOC = '''
.highlight-wrapper {
    margin-bottom: 1.25em; /* 添加底部边距，可根据需要调整 */
  }

   .highlight-container {
    position: absolute;
    left: 0;
    right: 0;
    background-color: #0065bd; /* 设置背景颜色为蓝色 */
    padding-left: 3.17em; /* 添加左边距，可根据需要调整 */
    padding-bottom: 0.2em; /* 添加左边距，可根据需要调整 */
    display: flex; /* 设置为弹性布局 */
    align-items: center; /* 垂直居中 */
    height: 1.5em; /* 设置容器高度 */
  }
  
  .highlight {
    color: #ffffff; /* 设置字体颜色为白色 */
    margin: 0; /* 移除默认的margin */
  }
'''

BOXLINE = '''
.boxline {
  list-style: none;
  padding: 0;
  position: relative;
}

.boxline-item {
  position: relative;
  margin-top: 5em;
  margin-bottom: 5em;
}

.boxline-marker {
  position: absolute;
  left: 20px;
  width: 40px;
  height: 40px;
  line-height: 40px;
  text-align: center;
  font-weight: bold;
  color: white;
  background: rgb(48, 191, 248);
  border-radius: 4px;
}

.boxline-content {
  padding-left: 70px;
}

.boxline-content h2 {
  color: black !important;
}
'''

CARD = '''.card-container {
  display: flex;
  justify-content: center;
}

.card {
  background-color: #cceeff;
  border-radius: 5px;
  padding: 20px;
  width: 250px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin: 20px 30px; /* 上下边距为 20px，左右边距为 10px */
  display: inline-block;
}

.card h2 {
  margin-top: 0;
  margin-bottom: 10px;
}

.card p {
  margin: 0;
}'''


def load_css():
    tmp = [BASE,TOC,TIMELINE, BOXLINE,CARD]
    return '\n'.join(tmp)