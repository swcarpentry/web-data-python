---
layout: page
title: Working With Data on the Web
subtitle: Visualization
minutes: 15
---
> ## Learning Objectives {.objectives}
>
> *   Construct a simple visualization.

We now have all the tools we need to visualize the temperature differences between countries:

~~~ {.python}
from matplotlib import pyplot as plt

australia = get_annual_mean_temp_by_country('AUS')
canada = get_annual_mean_temp_by_country('CAN')
diff = diff_records(australia, canada)
plt.plot(diff)
plt.show()
~~~

![First Plot](fig/plot-01.png)

That's not what we want:
the library has interpreted our list of pairs as two corresponding curves rather than as the (x,y) coordinates for one curve.
Let's convert our list of (year, difference) pairs into a NumPy array:

~~~ {.python}
import numpy as np
d = np.array(diff)
~~~

and then plot the first column against the second. Note that, like python arrays the counting starts at 0, not one:

~~~ {.python}
plt.plot(d[:, 0], d[:, 1])
plt.show()
~~~

![Second Plot](fig/plot-02.png)

It looks like the difference is slowly decreasing, but the signal is very noisy.
At this point, if we wanted a real answer, it would be time to break out a curve-fitting library.

> ## Changing Visualizations {.challenge}
>
> Modify the plotting commands so that the Y-axis scale runs from 0 to 32.
> Do you think this gives you a more accurate or less accurate view of this data?

>## Visualisation Libraries {.challenge}
>
> When graphing using python;
>a) only the matplotlib library is available
>b) matplotlib can only be used with the numpy library
>c) it is important to get your data into the correct format for the graph required.
>d) line charts are the best way to illustrate data
> 
