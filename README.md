# Matplotlib_Graph_Editor_GUI
A GUI to make quick fixes to graphs in matplotlib

This has a number of common adjustments to pyplot, such as axis labels, title, and legend options. It is continually being updated with new features as I have time. The program is completely dynamic. Any changes are reflected immediately in the graph.

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
