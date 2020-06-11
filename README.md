# Matplotlib_Graph_Editor_GUI
A GUI to make quick fixes to graphs in matplotlib. Uses the pysimplegui package for GUI implementation.

This has a number of common adjustments to pyplot, such as axis labels, title, and legend options. It is continually being updated with new features. The program is completely dynamic and any changes are reflected immediately in the graph.

![GUI](https://github.com/alailink/Matplotlib_Graph_Editor_GUI/blob/master/GUI_image.PNG) 

for usage:
```python
import pyplot_editor as pe

###create fig here

pe.gui(fig)
```

To change the graph theme, it must be done beforehand, which can be accomplished like this:

```python
import pyplot_editor as pe

with plt.style.context('dark_background'):
    #...
    #create fig and axes plots
    #...
    pe.gui(fig)
```
