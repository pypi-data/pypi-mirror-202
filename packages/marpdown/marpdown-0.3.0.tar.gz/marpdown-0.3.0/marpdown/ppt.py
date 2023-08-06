from typing import Union, List
from .writer import Writer
from .css import load_css
from .slide import BaseSlide


class PPT:
    def __init__(self,
                 footer:str,
                 paginate:bool,
                 _class = "lead",
                 backgroundImage:str = '''url('https://marp.app/assets/hero-background.svg')''',
                 ) -> None:

        self.writer = Writer()
        self.slides = []
        self.footer = footer
        self.paginate = paginate
        self._class = _class
        self.backgroundImage = backgroundImage



    def __setup__(self):
        self.writer.append(f'''---\nmarp: true\nfooter: "{self.footer}"\npaginate: {self.paginate}''')
        if self._class is not None:
            self.writer.append(f"_class: {self._class}")
        if self.backgroundImage is not None:
            self.writer.append(f"backgroundImage: url('{self.backgroundImage}')")
        self.__start_new_slide__()
        self.writer.append('<style>')
        self.writer.append(load_css())
        self.writer.append('</style>')

    def build(self):
        self.writer.clear()
        self.__setup__()
        s = self.slides[0]
        self.__build_bgimage__(s)
        self.writer.append(s.content)

        for s in self.slides[1:]:
            self.__start_new_slide__()
            self.__build_bgimage__(s)
            self.writer.append(s.content)
        return self.writer.getValue()

    def __build_bgimage__(self, s):
        if s.bgimage is not None:
            self.writer.append(f'![bg]({s.bgimage})')
        else:
            self.writer.append(f'![bg]({self.backgroundImage})')

    def store(self,path:str, overwrite = True):
        self.build()
        self.writer.store(path, overwrite)

    # subscriptable and slice-able
    def __getitem__(self, item):
        return self.slides[item]

    def __start_new_slide__(self):
        self.writer.append('\n')
        self.writer.append('---\n')

    def __str__(self):
        return self.build()
    def __repr__(self):
        return self.build()

    # return an iterator that can be used in for loop etc.
    def __iter__(self):
        return self.slides.__iter__()

    def __len__(self):
        return len(self.slides)

    def addSlides(self, slides: Union[BaseSlide, List[BaseSlide]]):
        if isinstance(slides, BaseSlide):
            self.slides.append(slides)
        elif isinstance(slides, list):
            self.slides += slides

