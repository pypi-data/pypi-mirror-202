
class BaseSlide:
    def __init__(self,*,content:str='',backgroundImage: str = None, ):
        self.content = content
        self.bgimage = backgroundImage

class TOCSlide(BaseSlide):
    def __init__(self, title: str, toc: list[str],focus = -1,backgroundImage: str = None):
        self.toc = toc
        content = f'''# {title}\n\n'''
        if focus == -1:
            tmp = [f'''### {i+1}. {t}''' for i,t in enumerate(toc)]
            content += '\n'.join(tmp)
        else:
            tmp = [f'''### {i + 1}. {t}''' for i, t in enumerate(toc)]
            tmp[focus] = f'''### <div class ="highlight-wrapper"><div class="highlight-container"><div class="highlight"> {focus+1}. {toc[focus]}</div></div></div>'''
            content += '\n'.join(tmp)
        super().__init__(content=content, backgroundImage=backgroundImage)

class TimelineSlide(BaseSlide):
    def __init__(self, title:str,timelines: list[tuple],backgroundImage: str = None,):
        content ="# " + title + "\n"
        content += '''<ul class="timeline">\n'''
        for tl in timelines:
            name, detail = tl
            content+=f'''<li class="timeline-item">
                        <div class="timeline-marker"></div>
                        <div class="timeline-content">
                          <h4>{name}</h4>
                          {detail}
                        </div></li>'''
        content += '</ul>'

        super().__init__(content=content, backgroundImage=backgroundImage)