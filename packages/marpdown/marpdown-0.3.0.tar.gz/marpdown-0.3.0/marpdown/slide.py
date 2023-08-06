from .writer import Writer
from . import  utils

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

class BoxlineSlide(BaseSlide):
    def __init__(self, *, title: str,boxlines:list[str] ,backgroundImage: str = None):
        self.__writer__ = Writer()
        self.__writer__.append(f"# {title}")
        self.__writer__.append('<ul class="boxline">')

        for i,box in enumerate(boxlines):
            self.__writer__.append(f'''<li class="boxline-item">
    <div class="boxline-marker">{i+1}</div>
    <div class="boxline-content"><h2>{box}</h2></div>
  </li>''')
        self.__writer__.append('</ul>')
        super().__init__(content=self.__writer__.getValue(), backgroundImage=backgroundImage)

class CardSlide(BaseSlide):
    def __init__(self, *, title: str,cards: list[tuple[str,list[str]]] ,backgroundImage: str = None):
        self.__writer__ = Writer()
        self.__writer__.append(f"# {title}")
        self.__writer__.append('<div class="card-container">')
        for card in cards:
            name,bulletpoints = card
            self.__writer__.append(f'''<div class="card">
    <h2>{name}</h2>
    <p>
      {utils.list_to_html_ul(bulletpoints)}
    </p>
  </div>''')
        self.__writer__.append('</div>')
        super().__init__(content=self.__writer__.getValue(), backgroundImage=backgroundImage)

class ThanksSlide(BaseSlide):
    def __init__(self, backgroundImage:str = None):
        super().__init__(content='''<div style="display: flex; justify-content: center; align-items: center; height: 100vh; text-align: center;padding-left=200px">
  <h1 style="margin: 0 auto;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Thanks for Attention! Any Questions?</h1>
</div>''', backgroundImage=backgroundImage)