import os
import json 
from typing import Union, List
import streamlit.components.v1 as components
from utils import get_colors_from_cmap as get_colors 

_RELEASE = True  

if not _RELEASE:
    _wordcloud = components.declare_component(        
        "wordcloud", 
        url="http://localhost:3001",
    )
else:

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _wordcloud = components.declare_component("wordcloud", path=build_dir)


def wordcloud(
        words: List[dict],
        width: str = None,
        height: str =None,
        font_min: int=None,
        font_max: int=None,
        font_scale: float=None,
        max_words: int=None,
        palette: str='viridis',
        paletteColorVer: bool = True,
        normColor: str = "black",
        onWordClick: bool = False,
        rotations: int = 0,
        rotationsAngle: List[int] = [0, 90],
        per_word_coloring: bool= False,
        padding: int=None,
        layout: str='rectangular',
        enable_tooltip: bool= True,
        tooltip_data_fields: dict= {'text':'Word', 'value':'Count'},
        key: str=None,
        ):
    
    """Create a new instance of "wordcloud".

    Parameters
    ----------
    words: list[dict]
        The list of words to be used for wordcloud visualiztion. Each word should be a
        dictionary containing the following keys:
            text: str
                [required] word to be displayed on the wordcloud
            value: int
                [required] size of the word
            color: str
                [optional] color of the word to be discplayed (Hex or RGB format). 
                Please note that these colors will only be used if `per_word_coloring` 
                parameter is set to True.
            <-meta-data->: UNION(str, int)
                [optional] For any additional meta data od interest, you can pass 
                separate keys. These additional keys will be returned in the return 
                `clicked` and `hovered` dictionaries. You can also use them when 
                specifying tooltip fields. For more info, refer to `tooltip_meta_fields` 
                parameter.

    width: str
        The width of wordcloud. By default, the width is '100%', i.e., it will fill the
        whole containing block. If you want the wordcloud to be responsive (to 
        change when window size changes), you should pass its relative size (100%, 
        90%, 80%, ...). Other valid examples: 100px, 200, 1.5em, 300pt, 10mm, ...
    
    height: str
        The height of wordcloud. Default is '100%'. Other valid examples: 100px, 
        200, 1.5em, 300pt, 10mm, ...
    
    font_min: int
        The smallest font size of words in wordcloud.
    
    font_max: int
        The largest font size of words in wordcloud.
    
    font_scale: float
        The scaling factor which will be multiplied by the default font sizes. `font_scale` 
        can only effects if no `font_min` or `font_max` has been passed. In case of passing 
        `font_min` and `font_max`, only their absolute number will be effective.

    max_words: int
        The maximum number of words to be displayed on wordcloud.

    palette: str
        The color palette to be used for the words in the wordcloud. This will only have av effect 
        if no `color` key has been passed in the list of `words`. By default, the color palette is 
        'viridis'. You can pass any valid Matplotlib Colormap (Please refer to the following link 
        for the list of all color palettes: 
            https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html ).
    
    paletteColorVer: bool
        Whether to set the color via palette or via an arbitrary color

    normColor: str
        Arbitrary stringfor color of all text. For example "black". Depends on `paletteColorVer`

    per_word_coloring: bool
        If True, the `color` key in the `words` objects will be used to fill the 
        words in wordcloud.

    onWordClick: bool
        If True, will recieve object of word clicked. 

    rotations: int
        The rotational direction of the word

    rotationsAngle: list[int, int]
        The range of rotations for each each word

    padding: int
        The padding between words in word cloud. Default: `1` .

    layout: str
        The wordcloud layout. Available options: ['rectangular', 'archimedean']

    enable_tooltip: bool
        Whether to show tooltip popover once hover on a word.

    tooltip_data_fields: dict
        A dictionary containing keys (all the fields) and their displayed values to be used 
        in tooltip. These fields can only be selected from the keys passed in the `words` dictionaries.

    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    Dict
        A dictionary containing information of the word that has been hovered or
        has been clicked.

    """

    palette_colors = get_colors(palette, 100) 

    component_value = _wordcloud(
        words=words,
        width=width,
        height=height,
        fontMin=font_min,
        fontMax=font_max,
        fontScale=font_scale,
        maxWords=max_words,
        paletteColorVer=paletteColorVer,
        normColor=normColor,
        paletteColors=palette_colors,
        padding=padding,
        layout=layout,
        enableTooltip=enable_tooltip,
        tooltipDataFields=tooltip_data_fields,
        perWordColoring=per_word_coloring,
        rotations=rotations,
        rotationsAngle=rotationsAngle,
        onWordClick=onWordClick,
        key=key,
        default=None,
    )

    return component_value
